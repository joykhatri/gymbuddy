# views.py
import requests
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, UserSubscriptionForm, OrderForm
from .models import *
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from newspaper import Article
import datetime


User = get_user_model()

def home(request):
    return render(request, 'home.html')

@login_required(login_url='/login/')
def workout_categories(request):
    categories = WorkoutCategory.objects.all()
    return render(request, 'workout_categories.html', {'categories': categories})

def exercises_category(request, category_id):
    category = get_object_or_404(WorkoutCategory, id=category_id)
    exercises = category.workoutexercise_set.all()  # or use related_name if you set it
    return render(request, 'exercises_category.html', {
        'category': category,
        'exercises': exercises
    })

def exercise_detail(request, pk):
    exercise = get_object_or_404(WorkoutExercise, pk=pk)
    return render(request, 'exercise_detail.html', {'exercise': exercise})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Signup successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Email is already registered.')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # Check if email exists
        if not User.objects.filter(email=email).exists():
            messages.error(request, "Email not registered. Please sign up first.")
            return redirect('login')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_superuser:
                messages.error(request, "Admins can only log in through the admin panel.")
                return redirect('login')

            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid password. Please try again.")
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')

        # Save to the database
        ContactUs.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message_text
        )

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')  # make sure 'contact' matches your URL name

    return render(request, 'contact.html')

@login_required(login_url='login')  # Redirect to login page if not logged in
def feedback_view(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        feedback = UserFeedback.objects.create(
            user=request.user,
            email=request.user.email,
            subject=subject,
            message=message
        )
        feedback.save()
        messages.success(request, "Thank you for your feedback!")
        return redirect("feedback")

    return render(request, "feedback.html")

SPOONACULAR_API_KEY = "54bc2c496c8f4a9d8e089299a2b9deb2"

@login_required(login_url='/login/')
def diet_plan(request):
    query = request.GET.get('diet') or 'vegetarian'
    calories = request.GET.get('calories') or 2000

    url = f"https://api.spoonacular.com/mealplanner/generate"
    params = {
        "apiKey": "54bc2c496c8f4a9d8e089299a2b9deb2",
        "timeFrame": "week",
        "targetCalories": calories,
        "diet": query,
    }

    response = requests.get(url, params=params)
    data = response.json()

    return render(request, "diet_plan.html", {"week_meals": data.get("week", {}), "query": query, "calories": calories})

def recipe_detail(request, recipe_id):
    api_key = settings.SPOONACULAR_API_KEY
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": "54bc2c496c8f4a9d8e089299a2b9deb2",
        "includeNutrition": True
    }

    response = requests.get(url, params=params)
    data = response.json()

    return render(request, "recipe_detail.html", {
        "recipe": data
    })


NEWS_API_KEY = "f76cc4d89a334794a3b97d4c926ec386"
CONTEXTUAL_API_KEY = "7b7502a257msh2c563db7556d714p103429jsnb8f12f0bdb9b"

def blog(request):
    query = request.GET.get('query', 'gym fitness')

    # Fetch from NewsAPI
    newsapi_url = f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize=6&apiKey={NEWS_API_KEY}"
    newsapi_articles = []
    try:
        r = requests.get(newsapi_url)
        if r.status_code == 200:
            newsapi_articles = r.json().get('articles', [])
    except Exception as e:
        print("NewsAPI error:", e)

    # Fetch from ContextualWeb API
    contextual_url = f"https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/NewsSearchAPI"
    headers = {
        "X-RapidAPI-Key": CONTEXTUAL_API_KEY,
        "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
    }
    contextual_articles = []
    try:
        response = requests.get(contextual_url, headers=headers, params={
            "q": query,
            "pageNumber": 1,
            "pageSize": 6,
            "autoCorrect": True,
            "safeSearch": False,
            "withThumbnails": True
        })
        if response.status_code == 200:
            contextual_articles = response.json().get("value", [])
    except Exception as e:
        print("Contextual API error:", e)

    # Combine and render
    combined_articles = newsapi_articles + contextual_articles

    return render(request, "blog.html", {"articles": combined_articles})



def blog_detail(request):
    index = request.GET.get('index')
    if index is None:
        return redirect('blog')

    try:
        index = int(index)
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "fitness OR gym OR workout OR protein OR health",
            "apiKey": settings.NEWS_API_KEY,
            "pageSize": 50,
        }
        response = requests.get(url, params=params)
        data = response.json()

        if "articles" in data and 0 <= index < len(data["articles"]):
            article_data = data["articles"][index]

            # Use newspaper3k to extract full content
            article_url = article_data["url"]
            article = Article(article_url)
            article.download()
            article.parse()

            # Send data to template
            return render(request, "blog_detail.html", {
                "article": {
                    "title": article_data["title"],
                    "author": article_data.get("author"),
                    "publishedAt": article_data.get("publishedAt"),
                    "description": article_data.get("description"),
                    "urlToImage": article_data.get("urlToImage"),
                    "url": article_data.get("url"),
                    "full_content": article.text,
                }
            })
        else:
            return redirect('blog')

    except Exception as e:
        print(f"Error: {e}")
        return redirect('blog')
    
@login_required
def subscribe_plan(request):
    plans = Subscription.objects.filter(is_active=True)

    if request.method == 'POST':
        form = UserSubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.start_date = datetime.date.today()
            subscription.end_date = subscription.start_date + datetime.timedelta(days=30)  # 1 month plan
            subscription.is_active = True
            subscription.save()
            messages.success(request, f"Subscribed to {subscription.plan.name} successfully!")
            return redirect('home')
    else:
        form = UserSubscriptionForm()

    return render(request, 'subscribe_plan.html', {'plans': plans})

def store(request):
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category, is_active=True)
    else:
        products = Product.objects.filter(is_active=True)
    return render(request, 'store.html', {'products': products})


@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Order.objects.create(user=request.user, product=product)
    return redirect('store')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})


@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.product = product
            purchase.save()
            return redirect('my_orders')
    else:
        form = OrderForm()

    return render(request, 'buy_now.html', {'product': product, 'form': form})

@login_required
# Process Order
def process_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        payment_method = request.POST['payment_method']
        
        # Save order to database
        order = Order.objects.create(
            user=request.user,
            product=product,
            customer_name=name,
            email=email,
            address=address,
            payment_method=payment_method,
            status='Pending'
        )
        order.save()
        return redirect('order_success', order_id=order.id)
    return redirect('store')

# Order Success page
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})