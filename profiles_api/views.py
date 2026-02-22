from django.shortcuts import render # By default there. Used For Templates(html files)

from rest_framework.views import APIView
from rest_framework.response import Response
#Above line imports the Response object which is used to return responses from the API view. It's a standard Response object that when you call the API view or when Django rest framework calls our API view it's expecting it to return this standard Response object.

from rest_framework import status
# The status Object from the rest framework is a list of handy HTTP status codes that you can use when returning Responses from your API. We're going to be using these status codes in our post function handler

from . import serializers 
# Import serializers.py File we made in current App folder. We use it to tell our API view what data to expect when making post,put & patch requests to our API.

from rest_framework import viewsets

# Create your views here.

# Below line creates a new Class inheriting from the APIView Class that Django rest framework provides and it allows us to define the application logic for our endpoint(URL: domain/endpoint) that we're going to assign to this View.
class HelloApiView(APIView):
    '''To Show How we work with APIViews'''

    # Setting the Serializer
    serializer_class = serializers.HelloSerializer
    # This configures our APIView to have the serializer class HelloSerializer that we created in the imported file serializers.py in same App Folder. 


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
    
    def post(self, request):
        '''Create a Hello Message with our name'''
        #When we receive a post request to our hello API, first we'll Retrieve the serializer and pass in the data that was sent in the request.That is done in below line.

        '''1. Retrieving the Serializer Class for our view.'''
        serializer = self.serializer_class(data = request.data)
        # The self.serializer_class() is a function that comes with the APIView. It retrieves the configured serializer class(HelloSerializer) for our view.It's the standard way that you should retrieve the serializer class when working with serializers in a view.
        # The second part assigns the data. When you make a post request to our APIView the data is part of the request Object that's passed to our post request. We assign this data to our serializer class and then we create a new Object for our serializer class called serializer. 

        '''2. Validating the Serializer by calling the serializer"s is_valid() Method'''
        if serializer.is_valid(): # When input is Valid
            name = serializer.validated_data.get('name')
            # This is the Way to Retrieve any field we defined in the Serializer Class.
            message = f"Hello!.Amar Nam {name}"
            return Response( {'Message':message} )
        else: 
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            # serializer.errors will give you a dictionary of all the errors based on the validation rules that were applied to the serializer so it's a good idea to return this so the person that's using the API knows what went wrong when they tried to submit an invalid response. 

            #By default the response returns HTTP 200 Okay request.Since this was an error we need to change this to a 400 bad request. We do so using the status parameter.

    def put(self, request, pk=None):
        '''Handle Updating an Object'''
        
        # You make a request with HTTP put and it will update the entire object with what you've provided in the request.
        
        # When you're doing HTTP put you typically do it to a specific URL primary key.That's why we have this ok but we default it to none in case we don't want to support the PK in this particular APIView.Usually what you would do a put request to the URL with the ID of the object that you're updating and that's what we use this pk for. pk is used to take the ID of the object to be updated with the put request. 
        return Response({'method':'PUT'})

    def patch(self, request, pk=None):
        '''Handle Partial Update of an Object'''
        # Only update the fields of the Object provided in the Request
        return Response({'method':'PATCH'})

    def delete(self, request, pk=None):
        '''Delete an Object'''
        return Response({'method':'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    '''To see the working of ViewSet'''
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        ''''Returns a Hello Message '''
        viewset_features = [
            'Uses Actions(list,create,retrieve,update,partial_update)',
            'Automatically maps to URLs through Routers',
            'Provides More functionality with less code']

        return Response({'Mssg':'Hello, Mate', 'ViewSet_features' :viewset_features })
    
    def create(self, request):
        '''Create a New Hello Message'''
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.validated_data.get('name')
            message = f"Namaste, {name}"
            return Response({'Message' : message})
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        '''Handle getting an Object by its id'''
        return Response({'method':'RETRIEVE'})

    def update(self, request, pk=None):
        '''Handle updating an Object'''
        return Response({'method':'UPDATE'})

    def partial_update(self, request, pk=None):
        '''Handle Partially updating an Object'''
        return Response({'method':'PARTIAL_UPDATE'})

    def destroy(self, request, pk=None):
        '''Handle REMOVING an Object'''
        return Response({'method':'DESTROY'})