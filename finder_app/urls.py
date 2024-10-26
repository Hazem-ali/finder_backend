from django.urls import path
from .views import (
    ContactListCreateView,
    ContactRetrieveUpdateDestroyAPIView,
    ContactSearchView,
    ContactImageSearchView,
    ContactStatusListAPIView
)

urlpatterns = [
    path("", ContactListCreateView.as_view(), name="contact-create"),
    path(
        "<int:pk>/",
        ContactRetrieveUpdateDestroyAPIView.as_view(),
        name="contact-retrieve",
    ),
    path("<int:pk>/history", ContactStatusListAPIView.as_view(), name="contact-status-history"),
    path("search/", ContactSearchView.as_view(), name="contact-search"),
    path("search/image/", ContactImageSearchView.as_view(), name="contact-image-search"),
]
