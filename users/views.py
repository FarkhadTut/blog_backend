from rest_framework import viewsets
from .models import Profile

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProfileSerializer, UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import requests



@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({
            "detail": "Not found.",
        }, status=status.HTTP_404_NOT_FOUND)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({
            "token":token.key,
            "user": serializer.data
        })


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({
            "token":token.key,
            "user": serializer.data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("Passed for {}".format(request.user.email))


@api_view(['POST'])
def google(request):
    auth_code = request.data['code']
    client_secret = settings.GOOGLE_CLIENT_SECRET
    client_id = settings.GOOGLE_CLIENT_ID
    result = requests.post(
        url=settings.GOOGLE_OAUTH_ENDPOINT,
        data={
            "code": auth_code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": "http://localhost:8080",
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
            given_name = userinfo['given_name']
            family_name = userinfo['family_name']

            return redirect("http://localhost:8080")
        
        else:
            error = {'status': result.status_code,
                     'error': result}
        
    else:
        error = {'status': result.status_code,
                 'error': result}


    return redirect("http://localhost:8080/login", error=error)
