from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import template
from .models import Question, User, Group
from ReceiveData.models import UserResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
import dateutil.parser
from datetime import datetime, timezone, timedelta
from django_celery_beat.models import PeriodicTask, CrontabSchedule



def all_user_responses(request):
    result_list = list(UserResponse.objects.order_by('response_time').values('question_id', 'user_id', 'response_feeling', 'response_summary', 'response_time'))

    return HttpResponse(
        json.dumps(result_list, cls=DjangoJSONEncoder),
        content_type="application/json"
    )




def all_groups(request):
    groups = list(Group.objects.all())
    response_data = {"results": []}
    count = 1
    for g in groups:
        response_data["results"].append({"id": count, "text": g.group_name})
        count += 1
    return HttpResponse(
        json.dumps(response_data, cls=DjangoJSONEncoder),
        content_type="application/json"
    )




def delete_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        u = User.objects.get(name=name)
        u.delete()

        response_data = {}
        response_data['result'] = 'Delete user successful'
        response_data['name'] = name
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    update_tasks()
    return HttpResponseRedirect(reverse("home"))

def all_users(request):
    users = list(User.objects.all())
    response_data = {"data": []}
    for u in users:
        if u.group_set.all().exists(): # If this user belongs to a group
            groups = u.group_set.values('group_name') #<QuerySet [{'group_name': 'first group'}, {'group_name': 'second group'}]>
            group_names_list = []
            for group_dict in list(groups):
                group_names_list.append(group_dict['group_name'])
            group = group_names_list
        else:
            group = ""

        response_data["data"].append({"name": u.name, "phone_number": u.phone_number, "group": group})

    return HttpResponse(
        json.dumps(response_data, cls=DjangoJSONEncoder),
        content_type="application/json"
    )

def edit_user(request):
    original_name = request.POST.get('original_name')
    name = request.POST.get('name')
    phone_number = request.POST.get('phone_number')
    groups = json.loads(request.POST.get('groups'))

    User.objects.get(name=original_name).delete()

    u = User(name=name, phone_number=phone_number)
    u.save()

    for group_name in groups:
        group = Group.objects.filter(group_name=group_name)
        if group.exists(): # if a group exists with the specified group name...
            group[0].users.add(u)
        else:
            g = Group(group_name=group_name)
            g.save()
            g.users.add(u)
    update_tasks()
    return HttpResponse('Successfully edited question ' + name)

def user_details(request):
    username = request.POST.get('username')
    u = User.objects.get(name=username)

    response_data = {}

    response_data['name'] = u.name
    response_data['phone_number'] = u.phone_number

    groups = u.group_set.values('group_name') #<QuerySet [{'group_name': 'first group'}, {'group_name': 'second group'}]>
    group_names_list = []
    for group_dict in list(groups):
        group_names_list.append(group_dict['group_name'])

    response_data['group'] = group_names_list

    return HttpResponse(
        json.dumps(response_data, cls=DjangoJSONEncoder),
        content_type="application/json"
    )

def new_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        groups = json.loads(request.POST.get('groups'))

        u = User(name=name, phone_number=phone_number)
        u.save()

        for group_name in groups:
            group = Group.objects.filter(group_name=group_name)
            if group.exists(): # if a group exists with the specified group name...
                group[0].users.add(u)
            else:
                g = Group(group_name=group_name)
                g.save()
                g.users.add(u)
        update_tasks()
        return HttpResponse('Successfully added user ' + name)

    return HttpResponseRedirect(reverse("home"))







def update_tasks():
    PeriodicTask.objects.exclude(name="celery.backend_cleanup").delete()
    for q in Question.objects.all():
        if q.status == "finished":
            continue

        hr = q.time.hour
        m = q.time.minute

        if q.frequency == 'Daily':
            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute=m, hour=hr, day_of_week="*", day_of_month="*", month_of_year="*",
            )
        elif q.frequency == 'Weekly':
            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute=m, hour=hr, day_of_week=str(q.start_date.weekday()+1), day_of_month="*", month_of_year="*",
            )
        elif q.frequency == 'Monthly':
            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute=m, hour=hr, day_of_week="*", day_of_month=str(q.start_date.day), month_of_year="*",
            )

        phones = []

        for q_group in q.groups.all(): # get the groups associated with this question (theoretically just 1 group)
            for user in q_group.users.all(): # go through the users associated with that group
                phones.append(''.join(e for e in user.phone_number if e.isalnum())) # add that users phone number

        PeriodicTask.objects.update_or_create(
            name=q.question_name,
            task='app.celery.send_sms',
            start_time=q.start_date, # set to start sending out text messages 12:00am of this day #datetime.combine(q.start_date, q.time),
            args=json.dumps([q.id, q.question_name, q.question_text, phones]),
            defaults=dict(
                crontab=schedule,
            ),
        )


def all_questions(request):
    if request.method == 'POST':
        questions = list(Question.objects.all())
        response_data = {}
        for q in questions:
            response_data[q.id] = {"name": q.question_name, "text": q.question_text, "creation_date": q.creation_date, "time": q.time, "start_date": q.start_date, "end_date": q.end_date}

        return HttpResponse(
            json.dumps(response_data, cls=DjangoJSONEncoder),
            content_type="application/json"
        )
    return HttpResponseRedirect(reverse("home"))

def survey_details(request):
    if request.method == 'POST':
        q_id = request.POST.get('id')
        q = Question.objects.get(id=q_id)

        response_data = {}

        response_data['name'] = q.question_name
        response_data['text'] = q.question_text
        response_data['creation_date'] = q.creation_date
        response_data['time'] = q.time
        response_data['start_date'] = q.start_date
        response_data['end_date'] = q.end_date
        response_data['frequency'] = q.frequency

        responses = UserResponse.objects.filter(question_id=q_id)
        response_data['responses'] = {
            'length': len(responses),
            'user_id': [],
            'response_feeling': [],
            'response_time': [],
            'response_summary': []
        }

        for response in responses:
            response_data['responses']['user_id'].append(response.user_id)
            response_data['responses']['response_feeling'].append(response.response_feeling)
            response_data['responses']['response_time'].append(response.response_time)
            response_data['responses']['response_summary'].append(response.response_summary)


        return HttpResponse(
            json.dumps(response_data, cls=DjangoJSONEncoder),
            content_type="application/json"
        )
    return HttpResponseRedirect(reverse("home"))

def delete_survey(request):
    q_id = request.POST.get('id')

    q = Question.objects.get(id=q_id)
    q.delete()

    response_data = {}
    response_data['result'] = 'Delete survey successful'
    response_data['id'] = q_id
    update_tasks()
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

def finish_survey(request):
    q_id = request.POST.get('id')
    status = request.POST.get('status')

    q = Question.objects.get(id=q_id)
    q.status = status
    q.save(update_fields=['status'])
    update_tasks()
    response_data = {}
    response_data['result'] = 'Status change was successful'
    response_data['id'] = q_id
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


def edit_survey(request):
    if request.method == 'POST':
        q_id = request.POST.get('id')
        question_name = request.POST.get('name')
        question_text = request.POST.get('question')
        group_name = request.POST.get('group')
        time = request.POST.get('time') # an ISO string in UTC from frontend
        time = dateutil.parser.parse(time) # the ISO string as a datetime object (timezone included)
        frequency = request.POST.get('frequency')
        start_date = dateutil.parser.parse(request.POST.get('start_date')).date()
        end_date = dateutil.parser.parse(request.POST.get('end_date')).date()

        q = Question.objects.get(id=q_id)
        q.question_name = question_name
        q.question_text = question_text
        q.time = time
        q.frequency = frequency
        q.start_date = start_date
        q.end_date = end_date
        q.save()

        if q.groups.exists(): # if this question has an associated group, remove that group
            old_g = q.groups.all()[0]
            q.groups.remove(old_g)
        if group_name is not "": # if they enter a group for the question
            group = Group.objects.filter(group_name=group_name)
            if group.exists(): # if a group exists with the specified group name...
                q.groups.add(group[0])
            else:
                g = Group(group_name=group_name)
                g.save()
                q.groups.add(g)
        update_tasks()
        return HttpResponse('Successfully edited question ' + q_id)
    return HttpResponseRedirect(reverse("home"))

def new_survey(request):
    if request.method == 'POST':
        question_name = request.POST.get('name')
        question_text = request.POST.get('question')
        time = request.POST.get('time') # an ISO string in UTC from frontend
        time = dateutil.parser.parse(time) # the ISO string as a datetime object (timezone included)
        frequency = request.POST.get('frequency')
        start_date = dateutil.parser.parse(request.POST.get('start_date')).date()
        end_date = dateutil.parser.parse(request.POST.get('end_date')).date()
        q = Question(question_name=question_name, question_text=question_text, time=time, frequency=frequency, start_date=start_date, end_date=end_date, status="active")
        q.save()

        group_name = request.POST.get('group')

        if group_name is not "": # if they enter a group for the question
            group = Group.objects.filter(group_name=group_name)
            if group.exists(): # if a group exists with the specified group name...
                q.groups.add(group[0])
            else:
                g = Group(group_name=group_name)
                g.save()
                q.groups.add(g)



        update_tasks()
        return HttpResponse('Successfully added question ' + question_name)
    return HttpResponseRedirect(reverse("home"))




@login_required(login_url="/login/")
def surveys(request):
    context = {}
    context['surveys'] = {
        "active_surveys": Question.objects.filter(status='active').order_by('-creation_date'), #Question.objects.all()
        "finished_surveys": Question.objects.filter(status='finished').order_by('-creation_date'),
        "all_surveys": Question.objects.all().order_by('-creation_date'),
    }
    
    context['segment'] = 'index'

    html_template = loader.get_template( 'surveys.html' )

    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def overview(request):
    now = datetime.now(timezone.utc).date() # gets the date in UTC
    year = now.year
    month = now.month

    now_last_month = (datetime.now(timezone.utc).replace(day=1) - timedelta(days=1)).date()
    now_last_year = now_last_month.year
    now_last_month = now_last_month.month
    context = {}

    responses_yesterday = list()
    for response in UserResponse.objects.all():
        if response.response_time.date() == now - timedelta(days=1): # if the response's UTC date equals the UTC date yesterday
            responses_yesterday.append(response.id)

    responses_today = list()
    for response in UserResponse.objects.all():
        if response.response_time.date() == now: # if the response's UTC date equals the UTC date now
            responses_today.append(response.id)

    responses_week = list()
    for response in UserResponse.objects.all():
        # IMPORTANT response.response_time.date() is in UTC
        if response.response_time.date() >= now - timedelta(days=7):
            responses_week.append(response.id)
    responses_last_week = list()
    for response in UserResponse.objects.all():
        # IMPORTANT response.response_time.date() is in UTC
        if (now - timedelta(days=14) <= response.response_time.date()) and (response.response_time.date() <= now - timedelta(days=7)):
            responses_last_week.append(response.id)

    responses_this_month = list()
    for response in UserResponse.objects.all():
        if response.response_time.year == year and response.response_time.month == month:
            responses_this_month.append(response.id)

    responses_last_month = list()
    for response in UserResponse.objects.all():
        if response.response_time.year == now_last_year and response.response_time.month == now_last_month:
            responses_last_month.append(response.id)

    questions_this_month = list()
    for question in Question.objects.all():
        if question.creation_date.year == year and question.creation_date.month == month:
            questions_this_month.append(question.id)

    questions_last_month = list()
    for question in Question.objects.all():
        if question.creation_date.year == now_last_year and question.creation_date.month == now_last_month:
            questions_last_month.append(question.id)

    active_questions = Question.objects.filter(status="active")
    total_questions = Question.objects.all()
    percent_active = round(len(active_questions)/len(total_questions)*100) if len(total_questions) is not 0 else 0
    months_questions = Question.objects.filter(pk__in=questions_this_month)
    last_months_questions = Question.objects.filter(pk__in=questions_last_month)

    total_responses = UserResponse.objects.all()
    last_months_responses = UserResponse.objects.filter(pk__in=responses_last_month)
    months_responses = UserResponse.objects.filter(pk__in=responses_this_month)
    weeks_responses = UserResponse.objects.filter(pk__in=responses_week)
    weeks_responses_avg = weeks_responses.aggregate(Avg('response_feeling'))['response_feeling__avg']
    weeks_responses_avg = 0 if weeks_responses_avg == None else round(weeks_responses_avg, 1)

    last_weeks_responses = UserResponse.objects.filter(pk__in=responses_last_week)
    last_weeks_responses_avg = last_weeks_responses.aggregate(Avg('response_feeling'))['response_feeling__avg']
    last_weeks_responses_avg = 0 if last_weeks_responses_avg == None else round(last_weeks_responses_avg, 1)

    todays_responses = UserResponse.objects.filter(pk__in=responses_today)
    yesterdays_responses = UserResponse.objects.filter(pk__in=responses_yesterday)
    distinct_responses_month = months_responses.values('question_id').distinct() # how many questions had at least one response this month
    distinct_responses_last_month = last_months_responses.values('question_id').distinct() # how many questions had at least one response last month
    distinct_responses_total = total_responses.values('question_id').distinct() # how many questions have at least one response

    percent_responses_this_month = round(len(months_responses)/len(total_responses)*100) if len(total_responses) is not 0 else 0

    total_users = User.objects.all()
    active_users = UserResponse.objects.values('user_id').distinct()
    percent_users_active = round(len(active_users)/len(total_users)*100) if len(total_users) is not 0 else 0
    if len(total_questions) >= 1:
        percentResponseTotal = round(len(distinct_responses_total)/len(total_questions)*100)  # the percent of uqerstions with at least one response
    else:
        percentResponseTotal = 0
    if len(months_questions) >= 1:
        percentResponseMonth = round(len(distinct_responses_month)/len(months_questions) * 100) # percent of questions created this month with a response
    else:
        percentResponseMonth = 0
    if len(last_months_questions) >= 1:
        percentResponseLastMonth = round(len(distinct_responses_last_month)/len(last_months_questions) * 100)
    else:
        percentResponseLastMonth = 0

    percentDifference = percentResponseMonth - percentResponseLastMonth
    percentDifference = ["", "+"][percentDifference > 0] + str(percentDifference)

    responseRateToday = len(todays_responses)/len(active_questions) if len(active_questions) >= 1 else 0 # the number of responses today/the number of active questions
    responseRateYesterday = len(yesterdays_responses)/len(active_questions) if len(active_questions) >= 1 else 0 # the number of responses yesterday/the number of active questions
    context['questions'] = { # number of questions
        'total': total_questions,
        'active': active_questions,
        'percent': percent_active
    }
    context['user_responses'] = { # number of responses in the past n days
        "total": total_responses,
        "year": UserResponse.objects.filter(response_time__year=year),
        "month": months_responses,
        "today": todays_responses,
        "yesterday": yesterdays_responses,
        "response_increment": "up" if len(todays_responses) >= len(yesterdays_responses) else "down",
        "response_color": "green" if len(todays_responses) >= len(yesterdays_responses) else "red",
        "percent_this_month": percent_responses_this_month,
        "weeks_responses_avg": weeks_responses_avg,
        "last_weeks_responses_avg": last_weeks_responses_avg,
        "avg_color": "green" if weeks_responses_avg >= last_weeks_responses_avg else "red",
        "avg_increment": "up" if weeks_responses_avg >= last_weeks_responses_avg else "down",
        "responseRateToday": round(responseRateToday*100, 1),
        "responseRate_increment": "up" if responseRateToday - responseRateYesterday >= 0 else "down",
        "responseRate_color": "green" if responseRateToday - responseRateYesterday >= 0 else "red",
    }
    context['percent_response'] = { # percent of questions in past n days that have at least one response
        "total": percentResponseTotal,
        "month": percentResponseMonth,
        "last_month": percentResponseLastMonth,
        "percent_difference": percentDifference
    }
    context['users'] = { # number of users
        "total": len(total_users),
        "active_users": len(active_users), # Number of users that have responded to question
        "active_percent": percent_users_active # Number of users that have responded to question
    }
    context['moving_graph'] = {
        "responses_today": "3"
    }
    context['segment'] = 'index'

    html_template = loader.get_template( 'overview.html' )

    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def users(request):
    context = {}

    html_template = loader.get_template( 'users.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def results(request, survey_id):
    context = {}
    context['survey'] = Question.objects.get(id=survey_id)
    context['segment'] = 'index'

    html_template = loader.get_template( 'results.html' )

    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:


        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
