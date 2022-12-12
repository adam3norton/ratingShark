from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Create your views here.
def indexPageView(request):
    context = {
        'post' : {
            'User': 'Trey Jackson',
            'ConnectionToUser' : 'Friend',
            'Album': '2014 Forest Hills Drive',
            'Stars': 4.5,
            'DateTime': '12-13-2014',
        }
    }
    return render(request,'homePages/feed.html', context)

def chartsPageView(request):

    # Pritam: 'spotify:artist:4YRxDV8wJFPHPTeXepOstw'
    # SZA: '7tYKF4w9nC0nq9CsPZTHyP?si=2wlYmg4dS0OIyh0dWpdxeg'
    # BRUNO: 'https://open.spotify.com/artist/0du5cEVh5yTK9QJze8zA0C?si=LVMf2KsoSSidVm7gsmHN1Q
    artist_uri = 'spotify:artist:0du5cEVh5yTK9QJze8zA0C'
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='3396d07feb1b47d2bfe027c51e261c82',
                                                                                  client_secret='7b684d65fe35451db6b21f4efeb2bd93'))
    results = spotify.artist_top_tracks(artist_uri)
    final_result = results['tracks'][:10]

    context = {
        'results' : final_result
    }
    return render(request,'homePages/charts.html', context)

def newReviewPageView(request):

    # if 'name' in request.GET:
        # name = request.GET['name']
        # response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={name}&dataType=&pageSize=8&pageNumber=1&sortBy=dataType.keyword&sortOrder=desc&api_key={settings.API_KEY}')
        # data = response.json()
        # searchedFoods = data['foods']
    results = {}
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='3396d07feb1b47d2bfe027c51e261c82',
                                                                                  client_secret='7b684d65fe35451db6b21f4efeb2bd93'))
    if 'name' in request.GET:
        name = request.GET['name']
        results = spotify.search(q='artist:' + name, type='artist')


    context = {
        'results': results
    }
    return render(request,'homePages/new-review.html', context)


def profilePageView(request):
    context = {}
    return render(request,'homePages/profile.html', context)

def searchPageView(request):
    context = {}
    return render(request,'homePages/search.html', context)