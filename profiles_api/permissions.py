from rest_framework import permissions
# We're going to Import the permissions Modelu from the Django REST framework.This is going to provide us with the Base/Parent class that we can use to create a custom permissions class(Child Class).

#This BasePermission class that Django REST framework provides is for making our own custom permissions classes.
class UpdateOwnProfile(permissions.BasePermission):
    '''Allow Users to edit ONLY their Own Profile'''
    
    # The way you define permission classes is you define a has_object_permission function in the class. This Function gets called Every time a request is made to the API that we assign our permission to.
    # This Function will return True or False to determine whether the authenticated user has the permission to do the change they're trying to do or not.
    def has_object_permission(self, request, view, obj):
        '''Check if User is trying to Edit his own Profile Only'''
        
        # So what happens here is every time a request is made the Django rest framework will call this function and it will pass the request object, the view and the actual Object that we're checking the permissions against.
        # We need to check whether we should allow or deny the change the user is attempting and add the rules pertaining to whether a type of Change is allowed or not in the logic of this Function.
        # What we're going to do is we're going to check the HTTP method that is being generated according to the request and we're going to see whether that is in the safe methods list. The safe methods are methods that don't require or don't make any changes to the object.So a safe method would be for example HTTP GET.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Now we need to handle what happens if the request is not in the safe methods for example if they are trying to do a HTTP put to update an object. What we're going to do is we're going to check whether the object they're updating matches their authenticated user profile that is added to the authentication of the request.When you authenticate a request in Django rest framework it will assign the authenticated user profile to the request and we can use this to compare it to the object(obj) that is being updated and make sure they have the same ID.
        return obj.id == request.user.id
        # obj.id refers to id of object being updated and request.user.id refers to id of authenticated User Profile

class UpdateOnlyOwnStatus(permissions.BasePermission):
    '''Allow Auth. Users to Update Status of Profile Feed Items only when they are related to that User"s Profile. '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user_profile.id == request.user.id
        # Authenticated Users should be able to Update ONLY those Profile Feed items that are Associated with that Authenticated User’s profile.