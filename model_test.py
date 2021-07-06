from app.models import Question, User
from django.utils import timezone
from essential_generators import DocumentGenerator
from random_word import RandomWords

r = RandomWords()
gen = DocumentGenerator()

for i in range(50):
    word1 = r.get_random_word()
    word2 = r.get_random_word()

    q = Question(question_name=word1, question_text=word2, time=timezone.now())
    q.save()

    u1 = User(phone_number=gen.phone())
    u1.save()
    u2 = User(phone_number=gen.phone())
    u2.save()
    q.users.add(u1)
    q.users.add(u2)


#Question.objects.all()
#Question.objects.filter(id=1)
#Question.objects.get(id=1)
#Question.objects.filter(question_text__startswith='What')
#q.users.all()
#User.objects.all()[0].question_set.all()
#current_year = timezone.now().year
#Question.objects.get(pub_date__year=current_year)
