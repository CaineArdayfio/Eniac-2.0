from math import isnan
import pandas as pd
emoji_key = {
    b'\xf0\x9f\x98\x83': 5, # 😃
    b'\xF0\x9F\x98\x84': 5, # 😄
    b'\xF0\x9F\x98\x81': 5, # 😁
    b'\xF0\x9F\x98\x86': 5, # 😆
    b'\xf0\x9f\x98\x80': 5, # 😀
    b'\xf0\x9f\x98\x84': 5, # 😄
    b'\xf0\x9f\x99\x82': 4, # 🙂
    b'\xf0\x9f\x98\x8a': 4, # 😊
    b'\xf0\x9f\x98\x90': 3, # 😐
    b'\xf0\x9f\x98\x91': 3, # 😑
    b'\xf0\x9f\x99\x81': 2, # 🙁
    b'\xe2\x98\xb9\xef\xb8\x8f': 2, # ☹️
    b'\xf0\x9f\x98\x95': 2, # 😕
    b'\xf0\x9f\x98\xad': 1, # 😭
}

num_key = {
    1: "😭",
    2: "🙁",
    3: "😐",
    4: "🙂",
    5: "😃"
}

def add_emojis(df):
    emojis = []
    for index, row in df.iterrows():
        this_feeling = row['response_feeling']
        emojis.append(num_key[this_feeling])

    df.insert(0, "Emoji", emojis)
    return df

def assign_days(df):
    # assign each date a day... so if the first entry is january 3rd and the next is january 5th, then their day values would be 1 and 3
    days = [((df.iloc[day]['response_time'] -  df.iloc[0]['response_time']).days + 1) for day in range(df.shape[0])]

    df.insert(0,"Day",days)
    df.set_index('Day', inplace=True, drop=False)
    return df

def add_moving_avg(df):
    """Given a dataframe, returns the 7-day average of the data
    if you have feeling data at day 2, 5, and 9,
    but you have entires for day=1,2,3,4,5,9,10, (the person didn't enter data for 3 days in a row between what would be day 6-8)
    then the df is days 2,3,4,5,9 where all of 2,5, and 9 each have a feeling. daysnan will then become 2,3,4,5,6,7,8,9
    and feelingsnan will be all the feelings on 2,5,and 9 with nan for the 3,4,6,7,8
    """
    minDay = 1
    maxDay = df["Day"].max() # the last day (may or may not have feeling data)
    feelingDays = df["Day"].tolist() # days with feelings
    allDays = list(range(minDay, maxDay+1)) # every single day (including those in between)
    allFeelings = [] # every single feeling (filling blank days in with nan)

    for day in allDays:
        if day in feelingDays:
            rows_that_day = df.loc[df["Day"] == day]
            feeling_that_day = rows_that_day['response_feeling'].mean()
            allFeelings.append(feeling_that_day)
        else:
            allFeelings.append(float('nan'))

    allFeelings = pd.Series(allFeelings)
    feeling_7day_avg = pd.DataFrame(allFeelings)[0].rolling(7, min_periods=1).mean().tolist()

    return feeling_7day_avg

def is_start(body):
    """Returns whether a given text includes the word 'start'"""
    if "start" == body.lower().replace(" ", ""): return True
    else: return False

def is_int(body):
    """Returns whether a given value is an integer"""
    try:
        num = int(body)
    except ValueError:
        return False
    return True

def is_emoji(body):
    """Returns whether a given character is one of the 5 pre-set emojis"""
    if body.encode() in emoji_key.keys(): return True
    else: return False

def is_data_request(body):
    """Returns whether a given text includes the word 'data'"""
    if "data" == body.lower().replace(" ", ""): return True
    else: return False
