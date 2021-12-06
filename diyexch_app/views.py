from django.shortcuts import render, redirect
from .models import Profile, Tool, Borrow_tx
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, ToolForm, UserUpdateForm, ProfileUpdateForm
from random import sample

# Create your views here.


def rate_user(request, id):
    # create a user rating system
    pass


@login_required()
def account_home(request):
    context = {}
    my_tools = Tool.objects.filter(owner=request.user)

    if my_tools.exists():
        context['my_tool_list'] = my_tools

    pending_txs = Borrow_tx.objects.filter(
        borrowed_tool__owner=request.user, 
        owner_approval=False,
        )

    if pending_txs.exists():
        pending_req_list = pending_tx_helper(pending_txs)
        context['req_list'] = pending_req_list

    return render(request, 'diyexch_app/account_home.html', context)


@login_required()
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/app/account_home')   
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'user_form':user_form, 'profile_form':profile_form}
    return render(request, 'diyexch_app/profile.html', context)


@login_required()
def create_tool(request):
    if request.method == 'GET':
        form = ToolForm()
        context = {
            'form': form
            }
        return render (request, 'diyexch_app/tool_form.html', context)
    
    if request.method == 'POST':
        form = ToolForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            rd_url = f'/app/tool_home/{obj.id}/'
            return redirect(rd_url)
        else:
            print('Form is not valid')
            context = {'form': form}
        
        
@login_required()
def tool_home(request, t_id):
    tool = Tool.objects.get(id=t_id)
    return render(request, 'diyexch_app/tool_home.html', {'tool': tool})


@login_required()
def delete_tool(request, t_id):
    tool = Tool.objects.get(id=t_id)
    if tool.owner != request.user:
        return redirect('/app/account_home/')
    else:
        tool.delete()
        msg = f'{tool.name} was successfully deleted.'
        context = {'success_msg': [ msg ]}
        return render(request, 'diyexch_app/success.html', context)


@login_required()
def borrow_tool(request, t_id):
    borrower = request.user
    tool = Tool.objects.get(id=t_id)
    owner = tool.owner
    context = {'tool': tool}

    # validating
    if borrower.profile.cc_number is None:
        context.update({'err_msgs': ["Sorry, you need a credit card on file to borrow a tool!"]})
        return render(request, 'diyexch_app/tool_home.html', context)

    else:
        Borrow_tx.objects.create(
            borrowed_tool=tool,
            borrowerID=borrower.id,
        )
        tool.visible = False
        tool.save()
        context = {
            'succ_msgs':'Please wait for the tool owner to contact you.',
            'tool': tool,
        }
        return render(request, 'diyexch_app/borrow_success.html', context)


@login_required()
def contact(request, id):
    # contact the user 
    return render(request, 'diyexch_app/conact.html', other_stuff)


@login_required()
def search(request):
    if request.method == "POST":
        query_name = request.POST.get('name', None)
        if query_name:
            results = Tool.objects.filter(name__icontains=query_name, visible=True)
            if not results:
                return render(request, 'diyexch_app/search.html', {"srch_error":["Sorry, no matching results found."]})
            else:
                return render(request, 'diyexch_app/search.html', {"tool_list":results, "title":"Search Results"})
        else:
            return render(request, 'diyexch_app/search.html', {"srch_error":["Sorry, could you please try that again?"]})
    else:
        # provide some random preview tools on the initial search (filler)
        id_list = Tool.objects.all().values_list('id', flat=True)
        sample_size = 4
        if id_list:
            if len(id_list) < sample_size:
                sample_size = len(id_list)
            random_id_list = sample(list(id_list), sample_size)
            qs = Tool.objects.filter(id__in=random_id_list)
            context = {'tool_list': qs, "title":"Sample Tools"}
        else:
            context = {}
        return render(request, 'diyexch_app/search.html', context) 


def pending_tx_helper(pending_txs):
    request_list = []
    req = {}
    for pend_tx in pending_txs:
        req['borrower'] = User.objects.get(id=pend_tx.borrowerID)
        req['tool'] = Tool.objects.get(id=pend_tx.borrowed_tool.id)
        request_list.append(req)
    return request_list


# @login_required()
# def first_login(request):
#     """ Runs after registration. When a user is saved, a user profile is created.
#         The profile requires more info than the AUTH USER allows. This should only
#         run once after the user is created.
#     """
#     if request.method == 'GET':
#         form = ProfileForm()
#         name = "First Time Login"
#         context = {
#             'name': name,
#             'form': form
#             }
#         return render (request, 'diyexch_app/first_login.html', context)

#     if request.method == 'POST':
#         user = request.user  # currently logged in user
#         form = ProfileForm(request.POST, request.FILES, instance=user.profile) # User.profile is the same as Profile, but updates all
#         if form.is_valid():
#             form.save()
#             return redirect('/app/account_home/')
#         else:
#             context = {'form': form}
#             return render(request, 'diyexch_app/first_login.html', context)

#     return render(request, 'diyexch_app/first_login.html', {})