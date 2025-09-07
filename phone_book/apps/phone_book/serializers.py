from rest_framework import serializers
from .models import PhoneBook

class PhoneBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneBook
        fields = ['id', 'name', 'phone_number', 'email']
