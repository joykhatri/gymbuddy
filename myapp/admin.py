from django.contrib import admin
from .models import *
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

@admin.register(User)
class ShowUser(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'password', 'user_photo')

    def user_photo(self, obj):
        if obj.profile:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile.url)
        return "No image"
    
    user_photo.short_description = 'Profile'

@admin.register(Country)
class ShowCountry(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(State)
class ShowState(admin.ModelAdmin):
    list_display = ('country', 'name')

@admin.register(City)
class ShowCity(admin.ModelAdmin):
    list_display = ('state', 'name')


@admin.register(WorkoutCategory)
class ShowWorkoutCategory(admin.ModelAdmin):
    list_display = ('name', 'description', 'workoutcatgories_photo')

@admin.register(WorkoutExercise)
class ShowWorkoutExercise(admin.ModelAdmin):
    list_display = ['title', 'description', 'category', 'video_url', 'difficulty', 'duration_in_min', 'workoutexercises_photo', 'created_at']
    search_fields = ['title', 'category__name']

@admin.register(Subscription)
class ShowSubscription(admin.ModelAdmin):
    list_display = ('name', 'description', 'price_per_month', 'is_active')

@admin.register(UserSubscription)
class ShowUserSubscription(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active', 'created_at')

@admin.register(Payment)
class ShowPayment(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_date', 'payment_method', 'status')

@admin.register(UserFeedback)
class ShowUserFeedback(admin.ModelAdmin):
    list_display = ('user', 'email', 'subject', 'message', 'created_at')

@admin.register(ContactUs)
class ShowContactUs(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'message', 'created_at')

@admin.register(Product)
class ShowProduct(ImportExportModelAdmin):
    list_display = ('name','category', 'description', 'price', 'products_photo', 'is_active')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer_name', 'email', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('customer_name', 'email', 'product__name')