from django.shortcuts import render
from django.views import generic
from .models import Currency


class Main(generic.ListView):
    template_name = 'exchangeRate/main.html'
    context_object_name = 'currency_list'

    def get_queryset(self):
        return Currency.objects.all()


class DetailView(generic.DetailView):
    model = Currency
    template_name = 'exchangeRate/detail.html'
