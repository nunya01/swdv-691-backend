from django.shortcuts import render

# Create your views here.

# might be able to replace these two with built-in
#####
def nologin_home(request):
    # The home page for users not logged in
    return render(request, 'diyexch_app/login.html' )
#####


# db queries

def create_user(request):
    # ...insert user in the db
    return render(request, 'diyexch_app/success.html', other_stuff)


# @login_required
def view_account(request, id):
    # ... GET account info from db
    return render(request, 'diyexch_app/account.html', other_stuff)


# @login_required
def user(request, id):
    if request.method == 'GET':
        # get the user
        return render(request, 'diyexch_app/user_home.html', other_stuff)

    elif request.method == 'DELETE':
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
def create_tool(request,):
    # ... insert the tool into the db
    return render(request, 'diyexch_app/success.html')


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

def register(request):
    # ...register a user
    return render(request, 'diyexch_app/user_form.html' )


# @login_required
def tool_form(request):
    # displays the form used to create a new tool
    return render(request, 'diyexch_app/tool_form.html', {})


# @login_required
def preview_tool(request, other_stuff):
    # displays the preview of a tool before keeping it
    return render(request, 'diyexch_app/tool_preview.html', {})

