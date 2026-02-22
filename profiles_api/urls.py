from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

# Make an instance of the DefaultRouter Class.
router = DefaultRouter()

# Register our Viewset with the Default Router using router.register() Method. router() here is the Instance of the Default Router we made previously.
router.register('Hello-ViewSet', views.HelloViewSet, base_name = 'hello_viewset')
# 1st Argument: Name of the URL we want to create.
# 2nd Arg: ViewSet that we wanna Register to specified Router. This viewset is the one we created in views.py.
# 3rd Arg: We need to specify the Base_Name for our ViewSet. The Base Name is used for retrieving the URLs in the router if needed using the URL retrieving function provided by Django.

urlpatterns = [
    path('hello-api-view/', views.HelloApiView.as_view()),
    # as_view() standard function that we call to convert our APIView class to be rendered by our urls.Django rest framework will call the get() function inside the Class-based View passed to the path() Method if a HTTP GET request is made to our URL.
    
    path('', include(router.urls))
    #As you register new routes with our router it generates a list of URLs that are associated for our ViewSet.It figures out the URLs that are required for all of the functions that we add to our ViewSet and then it generates this list of URLs  which we can pass in to using the path function and the include function to our URL patterns.

    # The reason we specify a blank string in the 1st Arg. of 2nd path function call is because we don't want to put a prefix to this URL. We just want to include all of the URLs in the base of this URLs file 
]