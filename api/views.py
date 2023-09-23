from django.shortcuts import render
from .models import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from mail_project import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from rest_framework.permissions import IsAdminUser
from django.template.loader import render_to_string
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializer import *
from .utils import sending_mail_to_recipients, email_filtering_func
# Create your views here.
import smtplib, random
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from .producer import publish_message

class MailCheckingApi(APIView):
    def get(self, request):
        publish_message('done successfully')
        return Response({'data':'done'})

class SendMailView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('subject', openapi.IN_QUERY, description="subject", type=openapi.TYPE_STRING),
            openapi.Parameter('content', openapi.IN_QUERY, description="content", type=openapi.TYPE_STRING),
            openapi.Parameter('email', openapi.IN_QUERY, description="email", type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
        ]
    )
    def post(self, request):
        subject = request.query_params.get('subject')
        content = request.query_params.get('content')
        email = request.query_params.get('email')
        response_data = {
            "subject": subject,
            "content": content,
            "email": email,
        }   
        self.send_mail_func(subject, content, email)
        crt = SendMail.objects.create(subject=subject, content=content, email=email)
        return Response(response_data)
    def send_mail_func(self, subject, content, email):
        email = email.split(',')
        context = {"subject":subject,"content":content}
        body_msg = render_to_string ('email/contentmail.html', context)
        msg = EmailMultiAlternatives ("Checking purpose", body_msg, settings.DEFAULT_FROM_EMAIL, email)
        msg.content_subtype = "html"
        msg.send()

class SendMailView1(APIView):
    def post(self, request):
        serializer = SendMailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            sending_mail_to_recipients(serialized_data)
            return Response({"data":serialized_data, "code":status.HTTP_200_OK, "message":"mail sent successfully to recipients"})
        return Response({"data":serializer.errors, "code":status.HTTP_400_BAD_REQUEST, "message":"Oops! Something went wrong. Please try again"})




############################### Token-amount ##########################################        

class CreateTokenAmountView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = TokenAmountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            return Response({"data":serialized_data, "code":status.HTTP_201_CREATED, "message":"successfull"})
        return Response({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":"Oops! Something went wrong"})
    
class AdminUpdateTokenAmountView(APIView):
    permission_classes = (IsAdminUser,)
    def get_object(self, id):
        try:
            return TokenAmountModel.objects.get(id=id)
        except:
            return None
    def get(self, request, id):
        token_amount = self.get_object(id)
        serializer = TokenAmountSerializer(token_amount)
        serialized_data = serializer.data
        return Response({"data":serialized_data, "code":status.HTTP_200_OK, "message":"Details"})
    def put(self, request, id):
        tokenamount = self.get_object(id)
        serializer = TokenAmountSerializer(tokenamount, data=request.data)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            return Response({"data":serialized_data, "code":status.HTTP_201_CREATED, "message":"updated successfull"})
        return Response({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":"Oops! Something went wrong"})
    
class GetAllTokenAmountsView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self, request):
        token_amounts = TokenAmountModel.objects.all()
        serializer = TokenAmountSerializer(token_amounts, many=True)
        serialized_data = serializer.data
        return Response({"data":serialized_data, "code":status.HTTP_200_OK, "message":"All records"})
    
class GetTokenAmountByIdView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self, request, id):
        token_amount = TokenAmountModel.objects.get(id=id)
        serializer = TokenAmountSerializer(token_amount)
        serialized_data = serializer.data
        return Response({"data": serialized_data, "code": status.HTTP_200_OK, "message": "Details"})
    
##########################################- Email Filtering -##################################################

class EmailFilteringView(APIView):
    def post(self, request):
        subject = request.data.get('subject')
        body = request.data.get('body')
        serializer = EmailFilteringSerializer(data=request.data)
        if serializer.is_valid():
            x = serializer.save()
            category_of_email = email_filtering_func(subject, body)
            x.category = category_of_email
            x.save()
            serialized_data = serializer.data
            return Response({"data":serialized_data, "code":status.HTTP_201_CREATED, "message": "!!!!!!!!!"})
        return Response({"data": None, "code": status.HTTP_400_BAD_REQUEST, "message": "Oops! Something went wrong"})    
    
class GetAllRecords(APIView):
    def get(self, request):
        records = EmailFilteringModel.objects.all()
        serializer = EmailFilteringSerializer(records, many=True)
        serialized_data = serializer.data
        return Response({'data': serialized_data, 'code':status.HTTP_200_OK, 'message': 'Successfully fetched all records'})

class SendOtp(APIView):
    def get(self, request):
        subject = "iam here"
        content = "this is content"
        email = "ramu9014@yopmail.com"
        self.send_mail_func(subject, content, email)
        return Response({"data":"sent"})
    def send_mail_func(self, subject, content, email):
        email_id = 'stefenwarner13@gmail.com'
        email_pass = 'iyutbwcpmhehhmuc'
        msg = EmailMessage()
        msg['Subject'] = 'Activation otp'
        msg['From'] = email_id
        msg['To'] = email
        token = "83982173"
        msg.set_content(f"{token}")
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as mail:
            mail.login(email_id, email_pass)
            mail.send_message(msg)   
        print('sent successfully')    
    def send_mail_func(self, subject, content, email):
        email = email.split(',')
        context = {"subject":subject,"content":content}
        body_msg = render_to_string ('email/contentmail.html', context)
        msg = EmailMultiAlternatives ("Checking purpose", body_msg, settings.DEFAULT_FROM_EMAIL, email)
        msg.content_subtype = "html"
        msg.send()

class SignUpView(APIView):
    serializer_class = UserSerializer
    def post(self, request):
        data = {
            "email" : request.data.get('email'),
            "username" : request.data.get('username'),
            "first_name"  : request.data.get('firstname'),
            "last_name"  : request.data.get('lastname')
            }
        password = request.data['password']
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.validated_data
            x = serializer.save()
            x.set_password(password)
            serialized_data = serializer.data
            x.otp = self.send_otp_to_mail(serialized_data)
            x.save()
            return Response({"data":serialized_data,"message": "Account activation link sent to mail"},status=status.HTTP_201_CREATED)
        return Response({"message": serializer.errors},status=status.HTTP_401_UNAUTHORIZED)
    def send_otp_to_mail(self, serialized_data):
        body_msg = self.otp_func()
        context = {"otp":body_msg}
        temp = render_to_string('email/otp.html', context)
        msg = EmailMultiAlternatives("Checking purpose", temp, settings.DEFAULT_FROM_EMAIL, [serialized_data["email"]])
        msg.content_subtype = 'html'
        msg.send()
        print('mail sent opt')
        return body_msg
    def otp_func(self):
        otp = ''
        for i in range(4):
            otp += str(random.randint(0,9))
        return otp
    
class VerifyOtp(APIView):
    def post(self,request):
        email=request.data.get('email')
        otp=request.data.get('otp')

class VerifyOtpView(APIView):
    def post(self, request, user_id):
        otp = request.data.get("otp")
        user_obj = User.objects.get(id=user_id)
        if user_obj:
            if otp == user_obj.otp:
                user_obj.is_verified = True
                user_obj.save()
                return Response({"data": "Your account is successfully verified"})
            else:
                return Response({"data":"wrong otp"})
        else:
            return Response({"data":"User not found"})
                