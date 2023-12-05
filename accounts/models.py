from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

# -- Create dabase for account super admin with some functions -- #
class MyAccountManager(BaseUserManager):
    
    # -- Function to create a new user -- #
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email: # if not add the email will raise the error
            raise ValueError('User musth have an email address')

        if not username: # if not add username will raise the error
            raise ValueError('User must have an username')

        # -- User model -- #
        user = self.model(
            email = self.normalize_email(email), # chuẩn hóa về dạng email
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password) # set password for user
        user.save(using=self._db) # save user into db
        return user
    
    # -- Function to create a new superuser -- #
    def create_superuser(self, first_name, last_name, email, username, password):
        # -- Superuser model -- #
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )

        # -- Permission -- #
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    

# -- Create dabase for account user with some fields -- #
class Account(AbstractBaseUser):
    
    # -- field to contain first name of user -- #
    first_name = models.CharField(max_length=50)
    
    # -- field to contain last name of user -- #
    last_name = models.CharField(max_length=50)
    
    # -- field to contain the username which user want -- #
    username = models.CharField(max_length=50, unique=True) # unique = True, chỉ một duy nhất
    
    # -- field to contain the email of user -- #
    email = models.EmailField(max_length=100, unique=True) # unique = True, chỉ một duy nhất
    
    # -- field to contain phone number of user -- #
    phone_number = models.CharField(max_length=50)
    
    
    # -- Some Required for fields above -- #  
     
    date_joned = models.DateTimeField(auto_now_add=True) # auto_now_add = True, tự động thêm thời gian lúc tạo khi tạo xong accout user
    
    last_login = models.DateTimeField(auto_now_add=True) # auto_now_add = True, tự động thêm thời gian lần cuối đăng nhập
    
    is_admin = models.BooleanField(default=False) # default = False, mặc định là user không phải là admin
    
    is_staff = models.BooleanField(default=False) # default = False, mặc định là user không phải là staff
    
    is_active = models.BooleanField(default=False) 
    
    is_superadmin = models.BooleanField(default=False) # default = False, mặc định là user không phải là super admin
    
    # ------------------------------------ #
    
    
    # -- Login Field -- #   
    USERNAME_FIELD = 'email' # login with email
    
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name'] # required some fields
    
    
    # -- Using function from MyAccoutManage to create new user and superuser -- #
    
    objects = MyAccountManager()
    
    # ------------------------------------------------------------------------- #
    
    
    # -- Display the email -- #
    def __str__(self):
        return self.email
     
    def has_perm(self, perm, obj=None):
        return self.is_admin  # if user is admin, user get permision for changing
    
    def has_module_perms(self, add_label):
        return True
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    



# -- Create a Model for User Profile edit inside Dashboard -- #
class UserProfile(models.Model):
    
    # Field contain user #
    user = models.OneToOneField(Account, on_delete=models.CASCADE) # OnetoOneField : only have one profile user unique
    
    # Field contain address
    address_line_1 = models.CharField(blank=True, max_length=100)
    
    address_line_2 = models.CharField(blank=True, max_length=100)
    
    # Field contain picture prodfile of user #
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    
    # Field city
    city = models.CharField(blank=True, max_length=20)
    # Field state
    state = models.CharField(blank=True, max_length=20)
    # Field country
    country = models.CharField(blank=True, max_length=20)
    
    # -- Display first_name of user -- #
    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    
    