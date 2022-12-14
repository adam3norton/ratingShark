from multiprocessing import context
import re
from django.shortcuts import render, redirect
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

from homePages.models import Album, Review, User, User_Favorite_Album

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
    if request.method == 'GET':
        topArtistName = ''
        query = "Travis Scott"
        results = {}
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='3396d07feb1b47d2bfe027c51e261c82',
                                                                                    client_secret='7b684d65fe35451db6b21f4efeb2bd93'))
        if 'name' in request.GET:
            query = request.GET['name']
            artists = spotify.search(q=query, type='artist')

            topArtistName = artists
        
        artistID = topArtistName["artists"]["items"][0]["id"]
        artist_uri = f'spotify:artist:{artistID}'
        results = spotify.artist_top_tracks(artist_uri)
    
        final_result = results['tracks'][:10]
        recommedation_seed = spotify.recommendation_genre_seeds
        recommendation  = spotify.recommendations(seed_artists=[artistID],
                                            seed_tracks=['2Q3tt5F2QrB5Qbvz8W7EuL', '3RiF3X9MqLW6GtL6oDZGJc'],
                                            target_pop=1,
                                            target_energy=0.5,
                                            limit=10)
        

        context = {
            'results' : final_result,
            'loggedin': loggedIn,
            'recommendation_seed' : recommedation_seed,
            'recommendations': recommendation,
            'topArtist' : topArtistName,

        }
        return render(request,'homePages/charts.html', context) 
    else:
        return render(request, 'homePages/charts.html')


# def chartsPageView(request):

#     # Pritam: 'spotify:artist:4YRxDV8wJFPHPTeXepOstw'
#     # SZA: '7tYKF4w9nC0nq9CsPZTHyP?si=2wlYmg4dS0OIyh0dWpdxeg'
#     # BRUNO: 'https://open.spotify.com/artist/0du5cEVh5yTK9QJze8zA0C?si=LVMf2KsoSSidVm7gsmHN1Q
#     artist_uri = 'spotify:artist:0du5cEVh5yTK9QJze8zA0C'
#     spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='3396d07feb1b47d2bfe027c51e261c82',
#                                                                                   client_secret='7b684d65fe35451db6b21f4efeb2bd93'))
#     results = spotify.artist_top_tracks(artist_uri)
#     final_result = results['tracks'][:10]
#     recommedation_seed = spotify.recommendation_genre_seeds

#     recommendation = spotify.recommendation_
    

#     context = {
#         'results' : final_result,
#         'recommendations' : recommedation_seed
#     }
#     return render(request,'homePages/charts.html', context)

def newReviewPageView(request):
    if loggedInUserId == None:
        return loginPageView(request, {'method': "signin"})
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
        'loggedin': loggedIn,
        # 'uri': uri
    }
    return render(request,'homePages/new-review.html', context)

def artistAlbumsPageView(request, name):
    if loggedInUserId == None:
        return loginPageView(request, {'method': "signin"})
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
        return loginPageView(request, {'method': "signin"})
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
                uri = album_uri,
            )
            album_object.save()

            reviewObject = Review(
                user = User.objects.get(username = loggedInUsername),
                album = album_object,
                stars = stars,
                album_image = results["images"][0]["url"]
            )
            reviewObject.save()
            return redirect(indexPageView)

        context = {
            'results': results
        }
        return render(request, 'homePages/create-review.html', context)

def profilePageView(request, method):

    if not loggedIn:
        return redirect(loginPageView, method = 'signin')
    elif request.method == 'POST' and method == "editUserForm":
        user = User.objects.get(id = loggedInUserId)

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.age = request.POST['age']
        user.email = request.POST['email']
        user.phone = request.POST['phone']

        user.save()
        
        return redirect(profilePageView, method = 'homeAccount')

    elif request.method == 'POST' and method == "editUandP":
        user = User.objects.get(id=loggedInUserId)

        user.username = request.POST['username']
        user.password = request.POST['password']

        user.save()
        
        return redirect(profilePageView, method = 'homeAccount')
    else:
        userData = User.objects.get(id = loggedInUserId)
        userReviews = Review.objects.filter(user_id = loggedInUserId)
        userFavorites = User_Favorite_Album.objects.filter(user_id = loggedInUserId)


        if method == "homeAccount":
            context = {
                'loggedin': loggedIn,
                'userData': userData,
                'display': "homeAccount",
                'userReviews': userReviews,
                'userFavorites': userFavorites,
            }
            return render(request,'homePages/profile.html', context)
        elif method == "editUser":
            context = {
                'loggedin': loggedIn,
                'userData': userData,
                'display': "editUser",
                'userReviews': userReviews,
                'userFavorites': userFavorites,
            }
            return render(request,'homePages/profile.html', context)
        else :
            context = {
                'loggedin': loggedIn,
                'userData': userData,
                'display': "editUandP",
                'userReviews': userReviews,
                'userFavorites': userFavorites,
            }
            return render(request,'homePages/profile.html', context)

def deleteReviewPageView(request, review_id):
    review = Review.objects.get(id = review_id)
    review.delete()

    return redirect(profilePageView, method= "homeAccount")

def editReviewPageView(request, review_id):
    
    if request.method == "POST":
        review = Review.objects.get(id = review_id)

        review.stars = request.POST['stars']

        review.save()

        return redirect(profilePageView, method="homeAccount")

    else:
        review = Review.objects.get(id = review_id)

        context = {
            'review': review,
            'display': "editReview",
        }

        return render(request,'homePages/profile.html', context)

def searchPageView(request):
    context = {
        'loggedin': loggedIn,
    }
    return render(request,'homePages/search.html', context)

def loginPageView(request, method = 'signin'):
    global loggedIn
    global loggedInUserId
    global loggedInUsername
    errors = []
    errors.clear()
    context = {}
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
            user.age = request.POST['age']
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

        if context == {}:
            context = {
                'display': 'signin'
            }

        return render(request, 'homepages/login.html', context)

def SignOutPageView(request):
    global loggedIn
    global loggedInUserId
    loggedIn = False
    loggedInUserId = None
    return redirect(indexPageView)

def explorePageView(request):
    query = "Justin Beiber"
    results = {}
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='3396d07feb1b47d2bfe027c51e261c82',
                                                                                  client_secret='7b684d65fe35451db6b21f4efeb2bd93'))

    if 'name' in request.GET:
        query = request.GET['name']
        results = spotify.search(q=query, type='track,artist,album')


    context = {
        'results': results
    }
    return render(request,'homePages/explore.html', context)
