from django.urls import path
from .views import indexPageView, chartsPageView, newReviewPageView, profilePageView, searchPageView

urlpatterns = [
    path("feed/", indexPageView, name="feed"),
    path("charts/", chartsPageView, name="charts"),
    path("new-review/", newReviewPageView, name="new-review"),
    path("profile/", profilePageView, name="profile"),
    path("search/", searchPageView, name="search"),
    path("", indexPageView, name="index"),
]