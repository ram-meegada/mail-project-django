from . import views
from django.urls import path
from .views import *

urlpatterns = [
    #mail
    path('sendmail/', SendMailView.as_view()),
    path('sendmail1/', SendMailView1.as_view()),

    #Token-amount 
    path('adminuser/create-token-amount/', CreateTokenAmountView.as_view(),name = "create-token-amount"),
    path('adminuser/update/token-amount/<int:id>/', AdminUpdateTokenAmountView.as_view()),
    path('adminuser/all-tokenamounts/', GetAllTokenAmountsView.as_view()),
    path('adminuser/tokenamountbyid/<int:id>/', GetTokenAmountByIdView.as_view()),

    #Email Filtering
    path('api/email-filtering/', EmailFilteringView.as_view()),
    path('api/all-records/', GetAllRecords.as_view()),
    path('api/send-otp/', SendOtp.as_view()),
    #############

    path('api/signup/', VerifyOtpView.as_view()),
    path('api/verify-otp/<int:user_id>/', VerifyOtpView.as_view()),

    path('mail/checking/', MailCheckingApi.as_view()),

]