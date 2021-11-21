from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import ProfileForm, ToolForm

# Create your views here.

# might be able to replace these two with built-in
#####
def nologin_home(request):
    # The home page for users not logged in
    return render(request, 'diyexch_app/login.html' )
#####


# db queries


def rate_user(request, id):
    pass


def first_login(request):
    """ Runs after registration. When a user is saved, a user profile is created.
        The profile requires more info than the AUTH USER allows. This should only
        run once after the user is created.
    """
    if request.method == 'GET':
        form = ProfileForm()
        name = "First Time Login"
        context = {
            'name': name,
            'form': form
            }
        return render (request, 'diyexch_app/first_login.html', context)

    if request.method == 'POST':
        user = request.user  # currently logged in user
        form = ProfileForm(request.POST, instance=user.profile) # User.profile is the same as Profile, but updates all
        if form.is_valid():
            form.save()
            return redirect('/app/account_home/')
        else:
            print('Form is not valid')
            context = {'form': form}
            return render(request, 'diyexch_app/first_login.html', context)

    return render(request, 'diyexch_app/first_login.html', {})


# @login_required
def account_home(request):
    # ... GET account info from db
    name = {'name':'Account Home'}
    return render(request, 'diyexch_app/account_home.html', name )


# @login_required
def profile(request):
    name = {'name':'User Profile'}
    return render(request, 'diyexch_app/profile.html', name)
    

# @login_required
def user(request, id):
    if request.method == 'DELETE':
        # delete the user
        return render(request, 'diyexch_app/success.html', other_stuff)

    elif request.method == 'PUT':
        # updatr the user
        return render(request, 'diyexch_app/success.html', other_stuff)


# @login_required
def tool(request, id):
    
    if request.method == 'GET':
        # get the tool from db
        return render(request, 'diyexch_app/tool_home.html')

    elif request.method == 'DELETE':
        # delete the tool
        return render(request, 'diyexch_app/success.html')

    elif request.method == 'PUT':
        # update the tool
        return render(request, 'diyexch_app/success.html')


# @login_required
def create_tool(request):
    if request.method == 'GET':
        form = ToolForm()
        name = "Add a Tool"
        context = {
            'name': name,
            'form': form
            }
        return render (request, 'diyexch_app/tool_form.html', context)
    
    if request.method == 'POST':
        form = ToolForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.ownerID = request.user
            obj.save()
            return redirect('/app/account_home/')
        else:
            print('Form is not valid')
            messages.error(request, 'Error Processing Your Request')
            context = {'form': form}
            return render(request, 'diyexch_app/tool_form.html', context)


# @login_required
def borrow_tool(request, tool_id):
    # logic to update the db
    return render(request, 'diyexch_app/success.html')


# @login_required
def search_by_name(request, name):
    # ... lookup list by name, return the search results
    return render(request, 'diyexch_app/search.html', {})


# @login_required
def contact(request, id):
    # contact the user 
    return render(request, 'diyexch_app/conact.html', other_stuff)


# @login_required
def search(request):
    # provide some random preview tools on the initial search (filler)
    return render(request, 'diyexch_app/search.html', {}) 


# strictly page routes

# @login_required
def tool_form(request):
    # displays the form used to create a new tool
    return render(request, 'diyexch_app/tool_form.html', {})


# @login_required
def preview_tool(request, other_stuff):
    # displays the preview of a tool before keeping it
    return render(request, 'diyexch_app/tool_preview.html', {})


def test_function(request):
    test_output = get_user_model() 
    print(test_output.objects.all())
    userList = User.objects.values()
    print(userList)
    return render(request, 'diyexch_app/test_output.html',{'context':test_output})