from django.shortcuts import render # By default there. Used For Templates(html files)

from rest_framework.views import APIView
from rest_framework.response import Response
#Above line imports the Response object which is used to return responses from the API view. It's a standard Response object that when you call the API view or when Django rest framework calls our API view it's expecting it to return this standard Response object.


# Create your views here.

# Below line creates a new Class inheriting from the APIView Class that Django rest framework provides and it allows us to define the application logic for our endpoint(URL: domain/endpoint) that we're going to assign to this View.
class HelloApiView(APIView):
    '''To Show How we work with APIViews'''

    #The way API views are broken up is it expects a Function for the different HTTP requests(CRUD operations) that can be made to the View.The HTTP GET request is typically used to retrieve a list of objects or a specific object. So, whenever you make a HTTP GET request to the URL which  will be assigned to this APIView, it will Call the get function and it will execute the logic that we write in the get function.

    def get(self, request, format=None):
        '''Returns a List of APIView Features.'''
        apiview_features = ['Uses HTTP methods as Functions(get, put, patch, delete, post).',
                            'Is Similar to a Traditional Django View. Just used with APIs.',
                            'Gives you the most control over your application logic',
                            'Is mapped manually to URLs'
                            ]

        # Django rest framework expects functions for the different HTTP requests(CRUD operations) to return a Response Object which it will then output when the API is called. Response Object needs to contain a dictionary or a list because when the API is called, it converts the Response object to json and in order to convert it to json it needs to be Contain either a list or a dictionary
        return Response( {'Message':'Hello, Sagnik', 'APIView_Features':apiview_features} )

