from django.urls import include, path

from . import views

urlpatterns = [
    path('', include(([
        path('rooms/join/', views.join_room, name='join'),
        path('api/rooms/', views.room_collection, name='collection'),
        path('rooms/', views.index, name="index"),
        path('rooms/<str:url>/', views.room, name='details'),
        
    ], 'rooms')))
]
