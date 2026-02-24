from django.db import models # There, by Default
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# These are the standard base classes that we need to use when Overriding or Customizing the default Django user model.This is described in the Django official documentation.

from django.contrib.auth.models import BaseUserManager
# Importing the Default User Manager Model/Class Above.

from django.conf import settings
# We import the settings.py in the Main Project Folder because we want to use the setting:AUTH_USER_MODEL defined in that file here in the Model for storing Profile Feed items in the DB.


# Create your models here.

# One of the Django commands that we're going to be using in the future is the createsuperuser Command.This is a command that's provided with the Django CLI that makes it really easy to add super users(administrator users) to the system. Now because we've Customized our user model we need to tell Django how to interact with this user model in order to create users because by default when it creates a user it expects a username field and a password field but we've replaced the username field with an email field so we just need to create a Custom Manager that can handle creating users with an email field instead of a username field.
class  UserProfileManager(BaseUserManager):
    '''Manager Model to manage Custom User Model'''
    
    # The First function we need to make is the create_user function.This is what the Django CLI will use when creating users with the command line tool.

    # Because of the way the Django password checking system works a None password won't work because it needs to be a hash. So basically until you set a password you won't be able to authenticate the user.
    def create_user(self, email, name, password=None):
        '''Function for Creating a New User Profile'''
        # So the flow for creating User is: 1. Validate email 2. Normalize email 3.Create user object 4.Set password 
        # 5.Save to database 6. Return user.

        if not email:#email is empty String or Null
            raise ValueError("Users must have a Valid Email Address")
        
        # Now, we Normalize(2nd half of Email is Case-Insensitive, 1st half is Case-Sensitive) the Email Address.
        email = self.normalize_email(email)

        user = self.model(email = email, name = name)
        # self.model Refers to the Model associated with this manager(custom UserProfile Model).
        # Above line is same as writing 'user = UserProfile(email=email, name=name)'. But using self.model makes it dynamic and reusable.

        user.set_password(password) # set_password is Defined in AbstractBaseUser.
        # Above line converts the password to a hash and never stores it as plain text in the database.For Security.

        user.save(using = self._db)
        # Standard Procedure for saving objects to DB in Django which is provided in the Django documentation. Above line ensures that different DBs are supported in Django.

        return user

    def create_superuser(self, email, name, password):
        '''Create New Super(admin) User Profile'''
        user = self.create_user(email=email, name=name, password=password)
        
        user.is_superuser = True # is_superuser is Defined in PermissionsMixin Class.
        user.is_staff = True
        user.save(using=self._db)
        return user


# Below User-defined Class inherits from the Imported Built-in Classes. 
class UserProfile(AbstractBaseUser, PermissionsMixin):
    '''Custom Class for Users in DB Table'''
    email = models.EmailField(max_length=255, unique=True) # Email Data-type
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True) # Boolean Column
    is_staff = models.BooleanField(default=False) 
    # is_staff Column determines which users will have admin Access
    
    # We need to specify the model manager what we're going to use for the objects and this is required for because we need to use our custom user model with the Django CLI so Django needs to have a custom model manager for the user model so it knows how to create users and control users using the Django command line tools.

    objects = UserProfileManager() # We will create a User Profile Manager Class and then work on this line further.

    # By default, the USERNAME_FIELD stores 'username'. We are Overriding that and storing 'email' in this Field. This means that when we authenticate users instead of them providing a username and password they're just going to provide their Email address and password.
    USERNAME_FIELD = 'email' # By default, Required_Field.
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        '''Returns Full Name of User'''
        return self.name

    def get_short_name(self):
        '''Returns Short Name of User'''
        return self.name

    # Converting User Profile Object i.e. Object of the Custom UserProfile Class to String.
    def __str__(self): # Recommended in all Django Models.
        '''Returns String Representation of our User.'''
        return self.email

# We use below Model to allow users to store Status Updates in the system.
class ProfileFeedItems(models.Model):
    '''For Storing User Profile Update Status in DB '''
    # So every time any user creates a new update it's going to create a new Profile Feed Item Object and associate that object with the user that created it.
    # The way you link models to other models in Django is you use what's called a foreign key.The benefit of doing this is that it allows you to ensure that the integrity of the database is maintained so you can never create a profile feed item for a user profile that doesn't exist.

    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE 
        #What is models.CASCADE? models.CASCADE tells Django: "If the referenced object is deleted, also delete this object" It defines what should happen when the related object is deleted. If a particular user Profile is removed, then all the Feed items in the DB that have the Foreign Key Relationsip between them will also be removed.
    )
    #? 1st Argument of ForeignKey() Method:
    # 1st Arg. is the Remote Model we are linking this Model to. Now we could have simply written Name of that Remote Model(UserProfile) in the 1st Arg and it would have worked. But we don't do that. It is Best Practice not to Hardcode(write name of the Remote Model) the Foreign Key Definition. We have used the setting AUTH_USER_MODEL from settings.py FIle as the 1st Arg.. This setting refers to the Model Currently being Used for User Authentication. If we change the model being used for User Auth. at any time, we will have to change all the Code that uses the foreign key if we hardcode it. If we use the setting, only that setting will change and we don't need to make any other modifications in any code. 

    status_text = models.CharField(max_length=255)
    # status_text is going to be used to Contain the text of the feed update.
    
    created_on = models.DateTimeField(auto_now_add = True)
    # Any time a User Profile Feed item is created and stored in DB,the TimeStamp of its creation is also added to the DB as a field of this model through auto_now_add Property

    def __str__():
        '''Defines String Representation of the Model'''
        # String Representation: Suppose I make a object of this Class: obj1. Using default __str__() predefined in Django, print(obj1) will give O/p: ProfileFeedItems object 1. But, using this definition of __str__(), print (obj1) will display the Value of the status_text Attribute of this Class.
        return self.status_text