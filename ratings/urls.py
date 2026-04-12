from django.urls import path

from .views import ReviewListCreateView, SentimentListView

urlpatterns = [
    path("reviews/", ReviewListCreateView.as_view(), name="rating_reviews"),
    path("sentiments/", SentimentListView.as_view(), name="rating_sentiments"),
]
