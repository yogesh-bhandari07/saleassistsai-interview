from functools import partial
from tkinter import image_names
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from management.serializers import *
from django.contrib.auth import authenticate
from management.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import os
from .models import *
import json

# Generate Token Manually


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# auth


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            print(user.name)
            token = get_tokens_for_user(user)
            # userData=json.dumps({'name':user.name,'email':user.email})
            return Response({'token': token, 'msg': 'Login Success', 'user': {'name': user.name, 'email': user.email}}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response({'user':serializer.data,"msg":"User fetched"}, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)





class ProductsView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ProductsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response({"msg": 'Product has been created', "data": serializer.data}, status=status.HTTP_200_OK)

    def get(self, request, pk=None, format=None):
        id = pk

        if id is not None:
            module = Products.objects.get(id=id)
            serializer = ProductsSerializer(module)
            return Response(serializer.data)

        modules = Products.objects.filter(status=True)
        serializer = ProductsSerializer(modules, many=True)
        return Response({"msg": 'Data Fetched', "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        id = pk
        module = Products.objects.get(id=id)
        serializer = ProductsSerializer(module, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": 'Data updated', "data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        id = pk
        module = Products.objects.get(id=id)
        serializer = ProductsSerializer(module, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": 'Data updated partially', "data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        id = pk
        module = Products.objects.get(id=id)
        module.delete()
        return Response({
            "msg": "Data has been deleted"
        }, status=status.HTTP_200_OK)

