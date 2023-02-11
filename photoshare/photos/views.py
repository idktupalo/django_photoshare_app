from django.shortcuts import render, redirect
from .models import Category, Photo

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm


# Create your views here.

def login_user(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('gallery')
    return render(request, 'photos/login_register.html', {'page': page})


def logout_user(request):
    logout(request)
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            user = authenticate(request, username=user.username, password=request.POST['password1'])
            if user is not None:
                login(request, user)
                return redirect('gallery')
    context = {'form': form, 'page': page}
    return render(request, 'photos/login_register.html', context)


@login_required(login_url='login')
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category is None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(category__user=user, category__name__contains=category)
    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)


@login_required(login_url='login')
def view_photo(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})


@login_required(login_url='login')
def add_photo(request):
    user = request.user
    categories_set = user.category_set.all()
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(user=user, name=data['category_new'])
        else:
            category = None
        photo = Photo.objects.create(category=category, image=image, description=data['description'])
        return redirect('gallery')
    return render(request, 'photos/add.html', {'categories': categories_set})


@login_required(login_url='login')
def del_photo(request, pk):
    photo = Photo.objects.get(id=pk)
    photo.delete()
    return redirect('gallery')
