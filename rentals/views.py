from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'rentals/home.html')


# --------------------------------REGISTER VIEW--------------------------------


from .forms import UserRegistrationForm, RentalUserForm
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        rental_form = RentalUserForm(request.POST)

        if user_form.is_valid() and rental_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()

            rental_user = rental_form.save(commit=False)
            rental_user.user = user
            rental_user.email = user.email
            rental_user.save()

            # login(request, user)  # auto-login
            return redirect('login')

    else:
        user_form = UserRegistrationForm()
        rental_form = RentalUserForm()

    return render(
        request,
        'auth/register.html',
        {
            'user_form': user_form,
            'rental_form': rental_form
        }
    )


 
# --------------------------------LOGIN  AND LOGOUT VIEW---------------------------------

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')



