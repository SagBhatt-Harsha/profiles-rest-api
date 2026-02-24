from rest_framework import serializers
#We're going to create a new class called hello_serializer(Child Class) and we're going to base it on the serializers(Parent) class from the Django rest framework.

from . import models # For linking UserProfileSerializer with our UserProfile Model

class HelloSerializer(serializers.Serializer):
    '''Serializes a Name Field for testing the APIView'''
    #We define the serializer and then you specify the fields that you want to accept in your serializer input. We're going to create a field called name and this is a value that can be passed into the request that will be validated by the serializer.
    
    # So serializers also take care of Validation Rules so if you want to say you want to accept a certain field of a certain type, serializers will make sure that the content passed to the API is of the correct type for that field.

    name = serializers.CharField(max_length=10)
    #? This tells Django that whenever you're making a or whenever you're sending a post put or patch request, expect an input with name and we're going to validate that input to a maximum length of 10


# Made to deal with our User Profile Objects for the planned User Profile.
class UserProfileSerializer(serializers.ModelSerializer):
    '''Serializes User Profile Object'''
    # The way that you work with model serializers is you use a meta class to configure the serializer to point to a specific model in our project.
    class Meta:
        model = models.UserProfile
        # UserProfile is the Django model we made for User Profile in models.py in same APP Folder.Above line sets our serializer up to point to our UserProfile model.

        # Next, we need to specify a list of fields in our model that we want to manage through our serializer so this is a list of all the fields that you want to either make accessible in our API or you want to use to create new models with our serializer
    
        fields = ('id', 'email', 'name', 'password')
        # We want to make an Exception to the 'password' as we don't want password of a User Profile to be shown when data regarding profile of said User is being retrieved.

        # We want to make this password field write-only.The way you do that is you use the extra keyword args variable which is extra_kwargs. 
        # This is going to be a dictionary and the keys of the dictionary are the fields that you want to add the custom configuration to.

        extra_kwargs = {
            'password':{
                'write_only':True, #? Can write(For New Objects) & Update Objects, but can't read(during retrieve Objects)
                'style':{ 'input_type':'password' }
                # Added our custom style to the password Field. This style makes the letters of the password invisible while typing.
            } 

        }  # Upto here, we have done field and Model Configuration.
        
    '''
    By default the model serializer allows you to create simple objects in the database.It uses the default create function of the object manager to create the object. We want to override this functionality for this particular serializer so that it uses the create_user function defined in our Custom object manager class:UserProfileManager. In the create_user method we defined, the password Field gets created as a hash and never gets stored in the DB as plain text.
    '''
    # If we do not override the default create function that the Model Serializer will use while creating objects,password will be stored in DB as plaintext which will compromise Security.

    def create(self, validated_data):
        '''Handles Creating User Account with Password as Hash.'''
        # ModelName:UserProfile Model Manager:objects create_user:Method we defined in Custom Model Manager Class:UserProfileManager
        user = models.UserProfile.objects.create_user( 
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']
            )
        return user

    # Similarly, we need to override the Default update() Method the Model Serializer will use to update User profile Objects.Otherwise, after updation, password will be stored in DB as Plain Text.

    def update(self, instance, validated_data):
        """Handle updating user account/profile Object"""
        if 'password' in validated_data:
            # If the field exists, we will "pop" (which means assign the value and remove from the dictionary) the password from the validated data and set it using set_password() (which saves the password as a hash).
            password = validated_data.pop('password')
            instance.set_password(password)

        # Once that's done, we use super().update() to pass the values to the existing DRF update() method, to handle updating the remaining fields.
        return super().update(instance, validated_data)
    
class ProfileFeedItemSerializer(serializers.ModelSerializer):
    '''Serializes User Profile Feed Item Objects i.e. Converts Objects to JSON Format'''
    class Meta:
        model = models.ProfileFeedItems #? Assigning this Serializer to ProfileFeedItems Model.
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        # Jab Object ko JSON format ke convert karenga, tab usme kaunse Fields honge is def. by above Line.

        # We don't want the users to be able to Set the user_profile Forein Key when they create a new feed item. We want to set the user profile based on the user that is AUTHENTICATED. I don't want one user to be able to create a new profile feed item and assign that to another user because that would be a security flaw in the system.

        # So we want to set user_profile to the Authenticated user and therefore we're going to make the user profile field read-only.So that means that when we list the objects we can see which users created which feed items but when we create an object it can only be assigned to the current user that is authenticated.

        #? For this, we use the extra_kwargs Variable.
        extra_kwargs = {'user_profile':{
            'read_only' : 'True'} 
            } 


   