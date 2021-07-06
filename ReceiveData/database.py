from app.models import Question, User, Group
from .models import UserResponse
from datetime import datetime, timedelta, date
from twilio.rest import Client
from . import utils
import pandas

account_sid = "AC1d37c7271533a60f99b10e4b684c4910"
auth_token = "877b7993822320131b74bc707e7ae9bd"
client = Client(account_sid, auth_token)


def database_connect(survey):
    df = pandas.DataFrame(list(UserResponse.objects.filter(question_id=survey).order_by('response_time').values('question_id', 'user_id', 'response_time', 'response_feeling', 'response_summary')))
    return df


# Get the user object associated with this phone number
def associatedUser(fromPhone):
    for u in User.objects.all():
        phone_number = ''.join(e for e in u.phone_number if e.isalnum())
        if phone_number == fromPhone:
            return u

# Get the question object associated iwth what they're answering
def associatedQuestion(fromPhone):
    eniac_messages = client.messages.list(limit=10, from_="+13174838532", to=f'+1{fromPhone}') # most recent message that Eniac sent

    q_id = None
    for message in eniac_messages:
        text = message.body
        if utils.is_int(text.split(":")[0]): # if this is a question with ID
            q_id = int(text.split(":")[0])
            break
    q = Question.objects.get(id=q_id)
    return q

def userHasFeeling(fromPhone):
    user = associatedUser(fromPhone)
    question = associatedQuestion(fromPhone)

    # Looop through this user's and this question's UserResponses and check if any of them fall on this day
    for user_response in UserResponse.objects.filter(user_id=user.name, question_id=question.id):
        if (user_response.response_time.date() == date.today()): # if any do fall on this day, then overwrite that user response
            return [True, user_response]
    return [False, None]


def addFeeling(fromPhone, feeling):
    # Create or replace the UserResponse object for this question, user, and day
    hasFeeling, user_response = userHasFeeling(fromPhone)
    if(hasFeeling is True):
        user_response.response_feeling = feeling
        user_response.save(update_fields=['response_feeling'])
    else:
        user = associatedUser(fromPhone)
        question = associatedQuestion(fromPhone)
        ur = UserResponse(user=user, question=question, response_feeling=feeling, response_summary="")
        ur.save()

def addSummary(fromPhone, summary):
    user = associatedUser(fromPhone)
    question = associatedQuestion(fromPhone)

    hasFeeling, user_response = userHasFeeling(fromPhone)
    # Create or replace the UserResponse object for this question, user, and day
    user_response.response_summary = user_response.response_summary + "\n" + summary if user_response.response_summary != "" else summary
    user_response.save(update_fields=['response_summary'])
