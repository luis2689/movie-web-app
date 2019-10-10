from django.shortcuts import render
from django.contrib import messages
from airtable import Airtable
import os


AT = Airtable('app5QtQpPBXACNwJh',
              'Movies',
              api_key='keya0UMt5Z4iaNNbC')

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)
