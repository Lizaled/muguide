from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Place, Review
from .forms import RegistrationForm, ReviewForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import logout
from .forms import ReviewForm
from .forms import CustomPasswordChangeForm
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import PermissionDenied


def check_username(request):
    username = request.GET.get('username', None)
    if username:
        exists = User.objects.filter(username=username).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})

def places(request):
    query = request.GET.get('q')  # Получаем параметр поиска из URL
    category = request.GET.get('category')  # Получаем параметр категории

    # Фильтрация мест
    if query:
        all_places = Place.objects.filter(
            Q(title__icontains=query) | Q(address__icontains=query)
        )  # Ищем совпадения в названии или адресе
    elif category:
        all_places = Place.objects.filter(category=category)  # Фильтруем по категории
    else:
        all_places = Place.objects.all()  # Если нет поиска и категории, показываем все места

    paginator = Paginator(all_places, 6)  # 6 мест на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'places/places.html', {'page_obj': page_obj, 'current_category': category, 'query': query})

def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.place = place
            review.user = request.user
            review.save()
            return redirect('place_detail', place_id=place.id)
    else:
        form = ReviewForm()

    return render(request, 'places/place_detail.html', {
        'place': place,
        'review_form': form,
    })

def search_places(request):
    query = request.GET.get('q', '')
    if query:
        places = Place.objects.filter(
            Q(title__icontains=query) | Q(address__icontains=query)
        ).values('id', 'title', 'address')[:10]  # Ограничиваем количество результатов до 10
        results = list(places)
    else:
        results = []
    return JsonResponse(results, safe=False)

@login_required
def add_review(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.place = place
            review.user = request.user
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('place_detail', place_id=place_id)
    
    return redirect('place_detail', place_id=place_id)

def profile_view(request):
    return render(request, 'places/profile.html', {'user': request.user})

# В функции register (после успешной регистрации)
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Аккаунт {username} успешно создан!')
            return redirect('places')
    else:
        form = RegistrationForm()
    return render(request, 'places/register.html', {'form': form})

# В функции add_review (после успешного добавления отзыва)
@login_required
def add_review(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.place = place
            review.user = request.user
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('place_detail', place_id=place_id)
    return redirect('place_detail', place_id=place_id)

# Для удаления комментария (новая функция)
@login_required
def delete_review(request, place_id, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user.is_staff or request.user == review.user:
        review.delete()
        messages.success(request, 'Отзыв успешно удален')
    else:
        messages.error(request, 'У вас нет прав для удаления этого отзыва')
    return redirect('place_detail', place_id=place_id)

def logout_view(request):
    logout(request)  # Завершаем сессию пользователя
    return redirect('places')  # Перенаправляем на главную страницу после выхода

def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')  # Перенаправление после успешного изменения пароля
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'places/change_password.html', {'form': form})

def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Выходим из учетной записи
        user.delete()  # Удаляем пользователя из базы данных
        messages.success(request, 'Ваш аккаунт был успешно удален.')
        return redirect('places')  # Перенаправляем на главную страницу
    return render(request, 'places/delete_account.html')

def places(request):
    all_places = Place.objects.all()
    paginator = Paginator(all_places, 6)  # 6 мест на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'places/places.html', {'page_obj': page_obj})

def check_email(request):
    email = request.GET.get('email', None)
    if email:
        exists = User.objects.filter(email__iexact=email).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})