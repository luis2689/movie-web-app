from django.shortcuts import render, redirect
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


def create(request):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftestament.co.uk%2Fmedia%2Fcatalog%2Fproduct%2Fcache%2F1%2Fsmall_image%2F300x%2F17f82f742ffe127f42dca9de82fb58b1%2Fplaceholder%2Fdefault%2Fno_image_available_300x300_1.jpg&f=1&nofb=1'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }

        try:
            response = AT.insert(data)
            messages.success(request, 'New movie added: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Got an error when trying to create a movie: {}'.format(e))

    return redirect('/')


def edit(request, movie_id):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftestament.co.uk%2Fmedia%2Fcatalog%2Fproduct%2Fcache%2F1%2Fsmall_image%2F300x%2F17f82f742ffe127f42dca9de82fb58b1%2Fplaceholder%2Fdefault%2Fno_image_available_300x300_1.jpg&f=1&nofb=1'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }

        try:
            response = AT.update(movie_id, data)
            messages.success(request, 'Updated movie: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Got an error when trying to update a movie: {}'.format(e))

    return redirect('/')

def delete(request, movie_id):
    try:
        movie_name = AT.get(movie_id)['fields'].get('Name')
        response = AT.delete(movie_id)
        messages.warning(request, 'Deleted movie: {}'.format(movie_name))
    except Exception as e:
        messages.warning(request, 'Got an error when trying to delete a movie: {}'.format(e))

    return redirect('/')
