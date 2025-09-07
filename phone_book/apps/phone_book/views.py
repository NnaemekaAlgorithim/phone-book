from django.http import JsonResponse
from django.db.models import Q
from django.views import View
class PhoneBookSearchSuggestionsView(View):
	def get(self, request, *args, **kwargs):
		query = request.GET.get('q', '').strip()
		suggestions = []
		if query:
			qs = PhoneBook.objects.filter(
				Q(name__icontains=query) | Q(phone_number__icontains=query)
			).order_by('name')[:10]
			for contact in qs:
				suggestions.append({
					'id': contact.id,
					'name': contact.name,
					'phone_number': contact.phone_number,
					'email': contact.email,
				})
		return JsonResponse({'results': suggestions})
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import PhoneBook
from .forms import PhoneBookForm

class PhoneBookListView(ListView):
	model = PhoneBook
	template_name = 'phone_book/list.html'
	context_object_name = 'contacts'
	paginate_by = 20

	def get_queryset(self):
		queryset = super().get_queryset()
		query = self.request.GET.get('q', '').strip()
		if query:
			queryset = queryset.filter(
				Q(name__icontains=query) | Q(phone_number__icontains=query)
			)
		return queryset

class PhoneBookCreateView(CreateView):
	model = PhoneBook
	form_class = PhoneBookForm
	template_name = 'phone_book/form.html'
	success_url = reverse_lazy('phonebook-list')

class PhoneBookUpdateView(UpdateView):
	model = PhoneBook
	form_class = PhoneBookForm
	template_name = 'phone_book/form.html'
	success_url = reverse_lazy('phonebook-list')

class PhoneBookDeleteView(DeleteView):
	model = PhoneBook
	template_name = 'phone_book/confirm_delete.html'
	success_url = reverse_lazy('phonebook-list')
	context_object_name = 'contact'
