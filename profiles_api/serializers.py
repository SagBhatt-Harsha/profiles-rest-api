from rest_framework import serializers
#We're going to create a new class called hello_serializer(Child Class) and we're going to base it on the serializers(Parent) class from the Django rest framework.

class HelloSerializer(serializers.Serializer):
    '''Serializes a Name Field for testing the APIView'''
    #We define the serializer and then you specify the fields that you want to accept in your serializer input. We're going to create a field called name and this is a value that can be passed into the request that will be validated by the serializer.
    
    # So serializers also take care of Validation Rules so if you want to say you want to accept a certain field of a certain type, serializers will make sure that the content passed to the API is of the correct type for that field.

    name = serializers.CharField(max_length=10)
    # This tells Django that whenever you're making a or whenever you're sending a post put or patch request expect an input with name and we're going to validate that input to a maximum length of 10