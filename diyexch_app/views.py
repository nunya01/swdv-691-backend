from django.shortcuts import render, redirect
from .models import Profile, Tool, Borrow_tx
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import ProfileForm, ToolForm
from random import sample

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
        form = ProfileForm(request.POST, request.FILES, instance=user.profile) # User.profile is the same as Profile, but updates all
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
    result = Tool.objects.filter(ownerID=request.user)
    context = {"tool_list": result}
    return render(request, 'diyexch_app/account_home.html', context)


# @login_required
def profile(request):
    name = {'name':'User Profile'}
    return render(request, 'diyexch_app/profile.html', name)


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
        form = ToolForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.ownerID = request.user
            obj.save()
            rd_url = f'/app/tool_home/{obj.id}/'
            return redirect(rd_url)
        else:
            print('Form is not valid')
            context = {'form': form}
            return render(request, 'diyexch_app/tool_form.html', context)


def tool_home(request, t_id):
    tool = Tool.objects.get(id=t_id)
    return render(request, 'diyexch_app/tool_home.html', {'tool': tool})


def delete_tool(request, t_id):
    tool = Tool.objects.get(id=t_id)
    if tool.ownerID != request.user:
        return redirect('/app/account_home/')
    else:
        tool.delete()
        msg = f'{tool.name} was deleted.'
        context = {'success_msg': msg}
        return render(request, 'diyexch_app/success.html', context)


def borrow_tool(request, t_id):
    borrower = request.user
    tool = Tool.objects.get(id=t_id)
    context = {'tool': tool}

    # validating
    if borrower.id == tool.ownerID.id:
        context.update({'err_msgs': ["You already own that tool!"]})
        return render(request, 'diyexch_app/tool_home.html', context)

    elif borrower.profile.cc_number is None:
        context.update({'err_msgs': ["Sorry, you need a credit card on file to borrow a tool!"]})
        return render(request, 'diyexch_app/tool_home.html', context)

    else:
        Borrow_tx.objects.create(
            borrowed_tool=tool,
            borrowerID=borrower.id,
        )
        tool.objects.visible = False
        tool.save()
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
    if request.method == "POST":
        query_name = request.POST.get('name', None)
        if query_name:
            results = Tool.objects.filter(name__icontains=query_name)
            if not results:
                return render(request, 'diyexch_app/search.html', {"srch_error":["Sorry, no matching results found."]})
            else:
                return render(request, 'diyexch_app/search.html', {"tool_list":results})
        else:
            return render(request, 'diyexch_app/search.html', {"srch_error":["Sorry, could you please try that again?"]})
    else:
        # provide some random preview tools on the initial search (filler)
        id_list = Tool.objects.all().values_list('id', flat=True)
        random_id_list = sample(list(id_list), 5)
        qs = Tool.objects.filter(id__in=random_id_list)
        context = {'tool_list': qs}
        return render(request, 'diyexch_app/search.html', context) 


def test_function(request):
    test_output = get_user_model() 
    print(test_output.objects.all())
    userList = User.objects.values()
    print(userList)
    return render(request, 'diyexch_app/test_output.html',{'context':test_output})