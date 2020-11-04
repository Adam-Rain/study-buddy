from django.urls import path
# from .views.mango_views import Mangos, MangoDetail
from .views.question_set_views import QuestionSets, QuestionSetDetail
from .views.question_views import Question, QuestionDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    # path('mangos/', Mangos.as_view(), name='mangos'),
    # path('mangos/<int:pk>/', MangoDetail.as_view(), name='mango_detail'),
    path('question_sets/', QuestionSets.as_view(), name='question_sets'),
    path('question_sets/<int:pk>', QuestionSetDetail.as_view(), name='question_set_detail'),
    path('questions/', Question.as_view(), name='questions'),
    path('question/<int:pk>', QuestionDetail.as_view(), name='question'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
