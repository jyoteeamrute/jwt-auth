from django.db import models
# from django.contrib.auth.models import User

# Create your models here.
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class MyUserManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, name, phone and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, password=None):
        """
        Creates and saves a superuser with the given email, name, phone and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            phone=phone,
            is_staff=True,
            is_admin=True
        )
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

class MyBlogPost(models.Model):     
    title=models.CharField(max_length=255,null=True,blank=True)
    content=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class Comment(models.Model):
    post=models.ForeignKey(MyBlogPost,on_delete=models.CASCADE,related_name='comment') 
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post=models.ForeignKey(MyBlogPost,on_delete=models.CASCADE,related_name='likes')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together=('post','user')
    def __str__(self):
        return f"{self.user.name} likes {self.post.title}"    
