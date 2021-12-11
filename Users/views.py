from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import auth
from .forms import RegisterForm

# Create your views here.

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'register.html', context)

    if request.method == 'POST':
        form  = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.cc_fullname = form.cleaned_data.get('cc_fullname')
            user.profile.cc_number = form.cleaned_data.get('cc_number')
            user.profile.cc_exp = form.cleaned_data.get('cc_exp')
            user.profile.zip_code = form.cleaned_data.get('zip_code')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.profile_pic = form.cleaned_data.get('profile_pic')
            # For DRY, put in a blank image if the user didnt provide one
            if user.profile.profile_pic == None:
                user.profile.profile_pic = 'default_no_img.jpg'
            user.profile.terms_and_cond = form.cleaned_data.get('terms_and_cond')
            user.save()
            # log the new usser in, so they can finish signing up
            user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, user)
            return redirect('/app/account_home/')
        else:
            print('Form is not valid')
            messages.error(request, 'Error Processing Your Request')
            context = {'form': form}
            return render(request, 'register.html', context)

    return render(request, 'register.html', {})
