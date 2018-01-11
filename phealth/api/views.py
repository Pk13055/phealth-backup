from django.shortcuts import render
from . serializers import *
from rest_framework import viewsets

# Create your views here.


class AddressViewSet(viewsets.ModelViewSet):
	queryset = Address.objects.all()
	serializer_class = AddressSerializer
	

