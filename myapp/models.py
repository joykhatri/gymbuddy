from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    
    def get_by_natural_key(self, email):
        return self.get(email=email)


class User(AbstractBaseUser, PermissionsMixin):
    # name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    profile = models.ImageField(upload_to="Users", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    

    def user_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.profile.url))
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class WorkoutCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="workout_categories", blank=True, null=True)

    def workoutcatgories_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))

    def __str__(self):
        return self.name

class WorkoutExercise(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.ForeignKey(WorkoutCategory, on_delete=models.CASCADE)
    video_url = models.URLField(blank=True, null=True)
    difficulty = models.CharField(max_length=20, choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ])
    duration_in_min = models.IntegerField()
    image = models.ImageField(upload_to="workout_exercises")
    created_at = models.DateTimeField(auto_now_add=True)

    def embed_url(self):
        if self.video_url and "watch?v=" in self.video_url:
            return self.video_url.replace("watch?v=", "embed/")
        return self.video_url

    def workoutexercises_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))

    def __str__(self):
        return self.title

class Subscription(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price_per_month = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_date = models.DateTimeField()
    payment_method = models.CharField(max_length=20, choices=[
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('other', 'Other'),
    ])
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')

    def __str__(self):
        return self.user

class UserFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.subject}"

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.BigIntegerField()
    subject = models.CharField(max_length=100, default='General')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=[
        ('protein', 'Protein Powder'),
        ('creatine', 'Creatine'),
        ('preworkout', 'Pre Workout'),
        ('bcaa', 'BCAA'),
    ], default='protein')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    is_active = models.BooleanField(default=True)

    def products_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))

    def __str__(self):  
        return self.name
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # link order to user
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.TextField()
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"