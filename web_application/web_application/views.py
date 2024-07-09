from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index2.html')

def some_view(request):
    current_user = request.user
    if current_user.is_authenticated:
        print(f"Текущий пользователь: {current_user.username}")
    else:
        print("Пользователь не вошёл в систему")
    return render(request, 'index2.html')
