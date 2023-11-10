from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views import View

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Profile


def user_login(reqeust):
    if reqeust.method == "POST":
        form = LoginForm(reqeust.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            user = authenticate(reqeust,
                                username=data['username'],
                                password=data['password'])
            if user is not None:
                if user.is_active:
                    login(reqeust, user)
                    return HttpResponse('Muvaggaqiyatli login amalga oshirildi')
                else:
                    return HttpResponse('siznign profilingiz faol holatda emas')
            else:
                return HttpResponse('login va parolda xatolik bor')
    else:
        form = LoginForm()
        context = {
            'form': form
        }
    return render(reqeust, 'registration/login.html', {'form': form})


@login_required
def dashboard_view(request):
    user = request.user
    profil_info = Profile.objects.filter(user=user)

    context = {
        'user': user,
        'profile': profil_info

    }

    return render(request, 'pages/user_profile.html', context)


# views.py


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html')
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy
    template_name = 'account/register.html'


@login_required
def profile(request):
    return render(request, 'registration/profile.html')


@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})


class EditUserView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
