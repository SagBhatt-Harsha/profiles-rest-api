from django.urls import path
from . import views

urlpatterns = [
    path('hello-api-view/', views.HelloApiView.as_view())
    # as_view() standard function that we call to convert our APIView class to be rendered by our urls.Django rest framework will call the get() function inside the Class-based View passed to the path() Method if a HTTP GET request is made to our URL.

]