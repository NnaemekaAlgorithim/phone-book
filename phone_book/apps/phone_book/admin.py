from django.contrib import admin
from .models import PhoneBook

@admin.register(PhoneBook)
class PhoneBookAdmin(admin.ModelAdmin):
	list_display = ("name", "phone_number", "email")
	search_fields = ("name", "phone_number", "email")
