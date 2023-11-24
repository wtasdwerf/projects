from .models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from rest_framework.decorators import api_view

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'POST':
        user.username = request.data.get('username')
        user.email = request.data.get('email')
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.nickname = request.data.get('nickname')
        user.age = request.data.get('age')
        user.money = request.data.get('money')
        user.salary = request.data.get('salary')
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_cart(request):
    productId = request.data.get('productId')
    user = request.user
    if user.financial_products is None:
        user.financial_products = []
        
    if productId not in user.financial_products:
        user.financial_products.append(productId)
    user.save()
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_cart(request):
    productId = request.data.get('productId')
    user = request.user
    if user.financial_products is None:
        user.financial_products = []
        
    if productId in user.financial_products:
        user.financial_products.remove(productId)
    user.save()
    serializer = UserSerializer(user)
    return Response(serializer.data)