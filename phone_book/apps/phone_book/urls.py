from django.urls import path
from .views import (
    PhoneBookListView, PhoneBookCreateView, PhoneBookUpdateView, PhoneBookDeleteView, PhoneBookSearchSuggestionsView
)

urlpatterns = [
    path('', PhoneBookListView.as_view(), name='phonebook-list'),
    path('add/', PhoneBookCreateView.as_view(), name='phonebook-add'),
    path('edit/<int:pk>/', PhoneBookUpdateView.as_view(), name='phonebook-edit'),
    path('delete/<int:pk>/', PhoneBookDeleteView.as_view(), name='phonebook-delete'),
    path('search-suggestions/', PhoneBookSearchSuggestionsView.as_view(), name='phonebook-search-suggestions'),
]
