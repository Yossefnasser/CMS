
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('dashboard')
		else:
			messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة.')
	return render(request, 'auth/login.html')

def logout_view(request):
	logout(request)
	return redirect('login')
