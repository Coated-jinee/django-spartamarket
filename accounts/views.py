from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from products.models import Product


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:signup')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form }) 


def login_view(request):
    if request.user.is_authenticated:
        return redirect("products:product_list")
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("products:product_list")
    else:
        form = AuthenticationForm(request)
    return render(request, 'accounts/login.html', {'form':form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')
    
@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    
    # 등록한 물품
    registered_products = Product.objects.filter(user=profile_user)

    # 찜한 물품
    liked_products = profile_user.liked_products.all()  # Product와 ManyToMany 관계

    # 팔로잉 여부
    is_following = request.user.follows.filter(pk=profile_user.pk).exists()

    context = {
        'profile_user': profile_user,
        'registered_products': registered_products,
        'liked_products': liked_products,
        'is_following': is_following,
    }

    return render(request, 'accounts/profile.html', context)

@login_required
def profile_edit(request, username):
    if request.user.username != username:
        return redirect('accounts:profile', username=username)
    
    user = get_object_or_404(User, username=username)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', username=username)
    else:
        form = ProfileForm(instance=user)  # GET 요청에서 폼 초기화
    
    # 모든 경우에서 form 변수를 반환
    return render(request, 'accounts/profile_edit.html', {'form': form})



def follow_view(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user != request.user:
        # 팔로우가 되어 있는 상태 -> 1
        if request.user.follows.filter(pk=target_user.pk).exists():
            # 취소하는 버튼 생성
            request.user.follows.remove(target_user)
        else:
            request.user.follows.add(target_user)
    return redirect('accounts:profile', username=username)



@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    
    # 등록한 물품 (해당 프로필 유저 기준)
    registered_products = Product.objects.filter(user=profile_user)

    # 찜한 물품
    liked_products = profile_user.liked_products.all()

    # 팔로잉 여부
    is_following = request.user.follows.filter(pk=profile_user.pk).exists()

    context = {
        'profile_user': profile_user,
        'registered_products': registered_products,
        'liked_products': liked_products,
        'is_following': is_following,
    }

    return render(request, 'accounts/profile.html', context)