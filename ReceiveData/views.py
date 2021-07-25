from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import template
from app.models import Question, User, Group
from .models import UserResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import Body, Message, MessagingResponse
from . import utils
from . import database
from datetime import datetime, timedelta
import pandas as pd
import math


@csrf_exempt
def get_data(request):
    survey = int(request.POST.get('survey'))
    df = database.database_connect(survey)
    df = utils.add_emojis(df)
    df = utils.assign_days(df)
    feeling_7day_avg = utils.add_moving_avg(df)

    my_list_of_dicts = list()
    firstDay = df.iloc[[0]]["response_time"].iloc[0]
    lastDay = df.iloc[[-1]]["response_time"].iloc[0]

    totalDays = (lastDay-firstDay).days + 1

    df_aggregate = pd.DataFrame(columns=["Feeling", "Summary", "Day", "Date", "All_Feelings"])
    df_aggregate["Day"] = df['Day'].unique()
    df_aggregate.set_index('Day', inplace=True)
    for day in df['Day'].unique():
        responses_on_day = df.loc[df['Day'] == day] # get all responses that ocurred on the specified day
        days_mean = responses_on_day['response_feeling'].mean() # the mean response on that day
        df_aggregate['Feeling'][day] = days_mean
        df_aggregate['All_Feelings'][day] = list(responses_on_day['response_feeling'])
        df_aggregate['Summary'][day] = '\n'.join(list(responses_on_day['response_summary']))
        df_aggregate['Date'][day] = list(responses_on_day['response_time'])[0].date()

    for day in range(totalDays):
        this_date = firstDay.date() + timedelta(days=day)
        this_dict = {"Date": this_date.strftime('%Y-%m-%d'), "Day": day+1}
        if (df_aggregate['Date'] == this_date).any(): # (if this day has a row (i.e. if it has any data at all))
            this_row = df_aggregate.loc[df_aggregate['Date'] == this_date].iloc[0]
            this_dict["Feeling"] = this_row["Feeling"]
            this_dict["All_Feelings"] = this_row["All_Feelings"]
            if this_row["Summary"] is not None: # (if this row has a summary)
                this_dict["Summary"] = this_row["Summary"]
                this_dict["Summary Length"] = len(this_row["Summary"])

        if math.isnan(feeling_7day_avg[day]) == False: # if this day has a moving average
            this_dict["Moving Average"] = feeling_7day_avg[day]
        # if none of the if statements are met, then no data point needed
        my_list_of_dicts.append(this_dict)

    return HttpResponse(
        json.dumps(my_list_of_dicts, cls=DjangoJSONEncoder),
        content_type="application/json"
    )


@csrf_exempt
def receive(request):
    body = request.POST.get('Body')
    fromNum = str(request.POST.get('From'))[2:]
    response = MessagingResponse()

    if utils.is_int(body) or utils.is_emoji(body):
        feeling_num = body
        if utils.is_emoji(body):
            feeling_num = utils.emoji_key[body.encode()]

        database.addFeeling(fromNum, feeling_num)
        message = Message()
        message.body("Good job! Your response of " + str(body) + " has been recorded. Reply to this message to add a text response. ")
        response.append(message)
    else:
        if database.userHasFeeling(fromNum)[0]:
            database.addSummary(fromNum, body)
            message = Message()
            message.body("Thank you! Your text entry has been recorded.")
            response.append(message)
        else:
            message = Message()
            message.body("In order to add a text entry, you must first respond with an emoji.")
            response.append(message)


    return HttpResponse(str(response))
