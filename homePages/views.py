from django.shortcuts import render, redirect
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from homePages.models import Album, Review, User

loggedIn = False
loggedInUsername = ""
loggedInUserId = None

# Create your views here.
def indexPageView(request):
    reviewData = Review.objects.all()
    print("\nReviews:")
    print(reviewData)

    if loggedInUserId != None:
        userData = User.objects.get(id = loggedInUserId)
        context = {
            'reviews' : reviewData,
            'loggedin': loggedIn,
            'userData': userData,
        }
        return render(request,'homePages/feed.html', context)
    else:
        context = {
            'reviews' : reviewData,
            'loggedin': loggedIn,
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
    if loggedInUserId == None:
        return loginPageView(request, {'method': "signinform"})
    else:

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

        # uri = results.artists.items[0].external_urls.spotify.split('/')[-1]


        context = {
            'results': results,
            # 'uri': uri
        }
        return render(request,'homePages/new-review.html', context)

def artistAlbumsPageView(request, name):
    if loggedInUserId == None:
        return loginPageView(request, {'method': "signinform"})
    else:
        results = {}
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='3396d07feb1b47d2bfe027c51e261c82',
                                                                                    client_secret='7b684d65fe35451db6b21f4efeb2bd93'))
        results = spotify.search(q='artist:' + name, type='album')
        context = {
            'results': results
        }
        return render(request, 'homePages/artist-albums.html', context)

def createReviewPageView(request, id):
    if loggedInUserId == None:
        return loginPageView(request, {'method': "signinform"})
    else:
        results = {}
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='3396d07feb1b47d2bfe027c51e261c82',
                                                                                    client_secret='7b684d65fe35451db6b21f4efeb2bd93'))
        results = spotify.album(id)
        album_name = results['name']
        album_uri = results['id']

        if request.method == 'POST':
            stars = request.POST['stars']

            print('Username: ', loggedInUsername)
            print('Album_Name: ', album_name)

            album_object = Album(
                name = album_name,
                uri = album_uri
            )
            album_object.save()

            reviewObject = Review(
                user = User.objects.get(username = loggedInUsername),
                album = album_object,
                stars = stars
            )
            reviewObject.save()
            return redirect(indexPageView)

        context = {
            'results': results
        }
        return render(request, 'homePages/create-review.html', context)

def profilePageView(request):
    context = {}
    return render(request,'homePages/profile.html', context)

def searchPageView(request):
    context = {}
    return render(request,'homePages/search.html', context)

def loginPageView(request, method):
    global loggedIn
    global loggedInUserId
    global loggedInUsername
    errors = []
    errors.clear()
    # signin, signup, signout

    if request.method == 'POST' and method == "signupform":
        errors.clear()
        email = request.POST['email']
        username = request.POST['username']

        data = User.objects.all()

        if len(data) > 0:
            for user in data:
                if email == user.email:
                    errors.append("This email has already been registered") 
                if username == user.username:
                    errors.append("This username is already taken")

        if len(errors) != 0:
            context = {
                    "display" : "signup",
                    "errors" : errors,
                }
            return render(request, 'homepages/login.html', context)
        else:
            user = User()

            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.username = request.POST['username']
            user.password = request.POST['password']
            user.email = request.POST['email']
            user.phone = request.POST['phone']

            user.save()

            loggedIn = True
            loggedInUserId = user.id
            loggedInUsername = user.username

            return redirect(indexPageView)

    elif request.method == 'POST' and method == "signinform":
        
        username = request.POST['username']
        password = request.POST['password']
        notFound = False

        data = User.objects.all()

        for user in data:
            if username == user.username and password == user.password:
                loggedIn = True
                loggedInUserId = user.id
                loggedInUsername = user.username
                return redirect(indexPageView)
            else :
                notFound = True
            
        if notFound:
            context = {
                "display" : "signin",
                "errors" : "The username or password is incorrect"
            }
            return render(request, 'homepages/login.html', context)

    else:
        if method == 'signin':
            context = {
                "display": "signin",
            }
        elif method == 'signup':


            context = {
                "display": 'signup',
            }

        return render(request, 'homepages/login.html', context)

def SignOutPageView(request):
    global loggedIn
    global loggedInUserId
    loggedIn = False
    loggedInUserId = None
    return redirect(indexPageView)