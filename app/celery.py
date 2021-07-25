import os
from celery import Celery
from twilio.rest import Client

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

#app = Celery('app',  broker='redis://localhost')
app = Celery('app',  broker='redis://redis:c7Nh5MtASVhlMIdTRhxEc0M4stmPQRyyVqoipymdCKU=@eniac.redis.cache.windows.net:6379/0')
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task
def send_sms(q_id, q_name, q_text, phones):
    account_sid = "AC1d37c7271533a60f99b10e4b684c4910"
    auth_token = "877b7993822320131b74bc707e7ae9bd"
    client = Client(account_sid, auth_token)

    q_append = 'Reply with one of five emojis to rate your response: 😭, 🙁, 😐, 🙂, 😃!'
    for phone in phones:
        try:
            message = client.messages.create(
                                    body=f'{q_id}: {q_name} \n{q_text}\n\n{q_append}',
                                    from_='+13174838532',
                                    to=f'+1{phone}'
                                )
        except:
            pass
