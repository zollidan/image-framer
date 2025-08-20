from django.urls import path
from .views import AddWhiteBgView, AddFrameView, ImagesList

urlpatterns = [
    path('add-white-bg/', AddWhiteBgView.as_view(), name='add-white-bg'),
    path('add-frame/', AddFrameView.as_view(), name='add-frame'),
    path('images/list/', ImagesList.as_view(), name='images-list'),
]