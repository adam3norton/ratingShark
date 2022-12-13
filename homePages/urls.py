from django.urls import path
from .views import indexPageView, chartsPageView, newReviewPageView, profilePageView, searchPageView, loginPageView, SignOutPageView, explorePageView, artistAlbumsPageView, createReviewPageView


urlpatterns = [
    path("explore", explorePageView, name="explore"),
    path("feed/", indexPageView, name="feed"),
    path("charts/", chartsPageView, name="charts"),
    path("new-review/", newReviewPageView, name="new-review"),
    path("artist-albums/<str:name>", artistAlbumsPageView, name="artist-albums"),
    path("create-review/<str:id>", createReviewPageView, name="create-review"),
    path("profile/", profilePageView, name="profile"),
    path("search/", searchPageView, name="search"),
    path("login/<str:method>/", loginPageView, name="login"),
    path("signout/", SignOutPageView, name="signout" ),
    path("", indexPageView, name="index"),
]