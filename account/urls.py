from django.urls import path
from .views import AccountView, SignIn
urlpatterns = [ 
		path('', AccountView.as_view()),
		path('sign-in', SignIn.as_view()),
]
