"""
URL configuration for newproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from tkinter.font import names

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.conf import settings
from myapp import views
from myapp.views import home

urlpatterns = [
    #  path('', lambda request: redirect('categories/')),
   path('admin/', admin.site.urls),
   path('', home, name='home'),
path('categories/', views.workout_categories, name='workout_categories'),
 path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('workouts/<int:category_id>/', views.exercises_category, name='exercises_category'),
    path('exercise/<int:pk>/', views.exercise_detail, name='exercise_detail'),
    path('logout/', views.logout_view, name='logout'),
    path('feedback/', views.feedback_view, name='feedback'),
    path("diet_plan/", views.diet_plan, name="diet_plan"),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog_detail/', views.blog_detail, name='blog_detail'),
    path('subscribe_plan/', views.subscribe_plan, name='subscribe_plan'),
    path('store/', views.store, name='store'),
    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('process-order/<int:product_id>/', views.process_order, name='process_order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),

# path('categories/', include('workouts.urls')), 
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)