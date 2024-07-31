from django.urls import path
from .views import SuspectCreateView, SuspectRetrieveUpdateDestroyAPIView, SuspectPhotoAPIView

urlpatterns = [
    path('', SuspectCreateView.as_view(), name='suspect-create'),
    path('<int:pk>', SuspectRetrieveUpdateDestroyAPIView.as_view(), name='suspect-retrieve'),
    path('photo/', SuspectPhotoAPIView.as_view(), name='suspect-retrieve'),
]