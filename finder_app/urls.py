from django.urls import path
from .views import ContactListCreateView, ContactRetrieveUpdateDestroyAPIView, ContactSearchView

urlpatterns = [
    path('', ContactListCreateView.as_view(), name='contact-create'),
    path('<int:pk>', ContactRetrieveUpdateDestroyAPIView.as_view(), name='contact-retrieve'),
    path('search/', ContactSearchView.as_view(), name='contact-search'),
]