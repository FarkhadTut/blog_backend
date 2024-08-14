from rest_framework import viewsets
from .models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404, redirect

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import requests
import datetime
import secrets
from transliterate import translit
from .permissions import UserPermission
import jwt, datetime
from django.utils import timezone

def createUsername(first,last):
    first = first.strip().replace(' ', '')
    last = last.strip().replace(' ', '')

    first = "".join([c for c in translit(first, "ru", reversed=True) if c.isalpha()])
    last = "".join([c for c in translit(last, "ru", reversed=True) if c.isalpha()])

    username = None
    if len(first)+len(last)<15:
        username = first + last
    else:
        username = first+last[:15]
    if not User.objects.filter(username=username).exists():
        return username
    else:
        while True:
            username_with_time = username + str(int(datetime.datetime.now()))
            if not User.objects.filter(username=username_with_time).exists():
                return username_with_time


def create_token(user):
    now = datetime.datetime.now(tz=datetime.UTC)
    expiration = (now + datetime.timedelta(minutes=60)).timestamp()
    iat = now.timestamp()

    payload = { 
        'id': user.id,
        'exp': expiration,
        'iat': iat
    }
    print(payload)

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get('token')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class LoginView(APIView):
    
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(username=request.data['username'])
        if user.exists():
            user = user.first()
        else:
            user = get_object_or_404(User, email=request.data['username'])
        
        if not user.check_password(request.data['password']):
            return Response({
                "detail": "Not found.",
            }, status=status.HTTP_404_NOT_FOUND)
        
        
        token = create_token(user)

        serializer = UserSerializer(instance=user)
        response = Response()
        response.data = {
            "user": serializer.data,
        }

        return response




class Signup(APIView):
    def post(self, request, *args, **kwargs):
        print("registering...")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = create_token(user)
            response = Response()
            response.data = {
                "user": serializer.data,
            }
            response.set_cookie(key="token", value=token, httponly=True)
            return response
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 


class TestToken(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication] 
    def get(self, request, *args, **kwargs):
        return Response("Passed for {}".format(request.user.email))


class Google(APIView):
    def post(self, request, *args, **kwargs):
        auth_code = request.data['code']
        client_secret = settings.GOOGLE_CLIENT_SECRET
        client_id = settings.GOOGLE_CLIENT_ID
        redirect_url = settings.GOOGLE_REDIRECT_URL
        result = requests.post(
            url=settings.GOOGLE_OAUTH_ENDPOINT,
            data={
                "code": auth_code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_url,
                "grant_type": "authorization_code"
            }
        )
        
        
        if result.ok:
            auth_data = result.json()
            access_token = auth_data['access_token']
            result = requests.get(
                url=settings.GOOGLE_USERINFO_URL,
                params={
                    "access_token": access_token,
                })
            
            if result.ok:
                userinfo = result.json()
                email = userinfo['email']
                if not User.objects.filter(email=email).exists():
                    first_name = userinfo['given_name']
                    last_name = userinfo['family_name']
                    username = createUsername(first_name, last_name)
                    password_length = 13
                    password = secrets.token_urlsafe(password_length)

                    user_data = {
                        'email': email,
                        'first_name': first_name,
                        'last_name': last_name,
                        'username': username,
                        'password': password
                    }

                    serializer = UserSerializer(data=user_data)
                    if serializer.is_valid():
                        serializer.save()
                        user = User.objects.get(username=username)
                        user.set_password(password)
                        user.save()
                        token, created = Token.objects.get_or_create(user=user)
                        serializer = UserSerializer(instance=user)
                        return Response({'token': token.key, 'user': serializer.data})
                    
                    error = {'error': 'Serializer error.'}
                    return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                else:
                    user = User.objects.get(email=email)
                    token, created = Token.objects.get_or_create(user=user)
                    serializer = UserSerializer(instance=user)
                    return Response({'token':token.key, "user": serializer.data}, status=status.HTTP_200_OK)

            
            else:
                error = {'error': result}
            
        else:
            error = {'error': result}


        return Response(error, status=result.status_code)


class LogoutView(APIView):

    def get(self, request, *args, **kwargs):
        response = Response()
        response.delete_cookie('token')
        response.data = {'message: success'}
        return response