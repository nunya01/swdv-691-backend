from django.shortcuts import render, redirect
from .models import Profile, Tool, Borrow_tx
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, ToolForm, UserUpdateForm, ProfileUpdateForm
from random import sample

# Create your views here.

def rate_user(request, id):
    """Todo, ratings """
    # create a user rating system
    pass


@login_required()
def account_home(request):
    """Gets data lists for users home page
    """

    context = {}
    my_tools = Tool.objects.filter(owner=request.user)

    # list of owned tools
    if my_tools.exists():
        context['my_tool_list'] = my_tools

    # list of borrow_tx's tthat need ot be approved.
    pending_txs = Borrow_tx.objects.filter(
        borrowed_tool__owner=request.user, 
        owner_approval=False,
        canceled=False,
        )

    if pending_txs.exists():
        context['req_list'] = pending_txs

    # list of loaned out tools
    loaned_tools = Borrow_tx.objects.filter(
        borrowed_tool__owner=request.user, 
        owner_approval=True,
        returned=False,
        )

    if loaned_tools.exists():
        context['loaned_list'] = loaned_tools

    # list of tools user is borrowing
    borrowed_tools = Borrow_tx.objects.filter(
        borrower=request.user,
        owner_approval=True,
        returned=False,
        )

    if borrowed_tools.exists():
        context['borrowed_list'] = borrowed_tools    

    return render(request, 'diyexch_app/account_home.html', context)


@login_required()
def profile(request):
    """Updates user's profile
    """

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
    """Creates a tool object
        Args:
            t_id <int>: id of Tool
    """

    if request.method == 'GET':
        form = ToolForm()
        return render (request, 'diyexch_app/tool_form.html', {'form': form})
    
    if request.method == 'POST':
        form = ToolForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            rd_url = f'/app/tool_home/{obj.id}/'
            return redirect(rd_url)
        else:
            context = {
                'err_msgs':['Please try that again.'],
                'form': form,
            }
            return render (request, 'diyexch_app/tool_form.html', context)


@login_required()
def update_tool(request, t_id):
    """Updates a tool object
        Args:
            t_id <int>: id of Tool
    """

    # pretest, not allowed to modify tool why a pending action exists
    tool = Tool.objects.get(id=t_id)
    current_borrow = Borrow_tx.objects.filter(borrowed_tool=tool, returned=False, canceled=False)
    if current_borrow.exists(): 
        context = {
            'tool': tool,
            'err_msgs':['Unable to modify tools on loan or with pending requests.']
        }
        return render(request, 'diyexch_app/tool_home.html', context)

    if request.method == 'GET':
        form = ToolForm(instance=tool)
        return render (request, 'diyexch_app/tool_form.html', {'form': form})  
    
    if request.method == 'POST':
        form = ToolForm(request.POST, request.FILES, instance=tool)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            rd_url = f'/app/tool_home/{obj.id}/'
            return redirect(rd_url)
        else:
            context = {
                'err_msgs':['Please try that again.'],
                'form': form,
            }
            return render (request, 'diyexch_app/tool_form.html', context)

        
@login_required()
def tool_home(request, t_id):
    """Home page of a tool
    Args:
        t_id <int>: id of Tool
    """

    tool = Tool.objects.get(id=t_id)
    context = {'tool':tool}
    borrow_tx = Borrow_tx.objects.filter(borrowed_tool=tool, owner_approval=True, returned=False)

    if borrow_tx.exists():
        context.update({'borrow_tx':borrow_tx[0]})

    return render(request, 'diyexch_app/tool_home.html', context)


@login_required()
def delete_tool(request, t_id):
    """Removes tool from the database
        Args:
            t_id <int>: tool id
    """

    tool = Tool.objects.get(id=t_id)
    # extra check to make certain the tool owner is the deleter
    if tool.owner != request.user:
        return redirect('/app/account_home/')

    # make sure the tool isn't out on loan before deleting
    current_borrow = Borrow_tx.objects.filter(borrowed_tool=tool, returned=False)
    if current_borrow.exists():
        context = {
            'tool': tool,
            'err_msgs':['Unable to delete tools on loan or with pending requests.']
        }
        return render(request, 'diyexch_app/tool_home.html', context)

    else:
        tool.delete()
        msg = f'{tool.name} was successfully deleted.'
        context = {
            'success_msg':msg,
            'title':'Success!'
        }
        return render(request, 'diyexch_app/info.html', context)


@login_required()
def borrow_tool(request, t_id):
    """Creates a Borrow_tx (borrow transaction)
        Args:
            t_id <int>: int id of the tool
    """

    borrower = request.user
    tool = Tool.objects.get(id=t_id)
    owner = tool.owner
    context = {'tool': tool}

    # validating, user without cc cant borrow a tool
    if borrower.profile.cc_number is None:
        context.update({'err_msgs': ["Sorry, you need a credit card on file to borrow a tool!"]})
        return render(request, 'diyexch_app/tool_home.html', context)

    # create the borrow transaction in the database
    else:
        Borrow_tx.objects.create(
            borrowed_tool=tool,
            borrower=borrower,
        )
        tool.visible = False
        tool.save()
        context = {
            'succ_msgs':['Please wait for the tool owner to contact you.'],
            'tool': tool,
        }
        return render(request, 'diyexch_app/borrow_success.html', context)


@login_required()
def return_tool(request, b_id):
    """Allows tool owner to mark a borrowed tool as returned
        Args:
            b_id <int>: id of Borrow_tx
    """

    borrow_tx = Borrow_tx.objects.get(id=b_id)
    borrow_tx.returned = True
    borrow_tx.save()
    tool = Tool.objects.get(id=borrow_tx.borrowed_tool.id)
    # make tool visible again for searches
    tool.visible = True
    tool.save()
    context = {
        'tool':tool,
        'succ_msgs':['Tool has been marked as returned.']
    }
    return render(request, 'diyexch_app/tool_home.html', context)


@login_required()
def cancel_borrow(request, b_id):
    """Allows tool owner to cancel a borrow request if it hasn't been approved
        Args:
            b_id <int>: Borrow_tx id
    """

    borrow_tx = Borrow_tx.objects.get(id=b_id)

    if borrow_tx.owner_approval == False or request.user == borrow_tx.borrowed_tool.owner:
        # tool owner has not approved the loan yet or
        # the tool owner is the one canceling the request
        borrow_tx.canceled = True
        borrow_tx.save()
        tool = Tool.objects.get(id=borrow_tx.borrowed_tool.id)
        tool.visible = True
        tool.save()
        context = {
            'success_msg':'Borrow request was canceled!',
            'title':'Success!'
        }
        return render(request, 'diyexch_app/info.html', context)
    else:
        return render(
            request, 
            'diyexch_app/account_home.html',
            {'err_msgs':['Unable to cancel an owner approved transaction']}
        )


@login_required()
def approve_borrow(request, b_id):
    """Allows tool owner to approve a borrow request
        Args:
            b_id <int>: Borrow_tx id
    """

    borrow_req = Borrow_tx.objects.get(id=b_id)

    if borrow_req.borrowed_tool.owner == request.user:
        # validate authorized user
        borrow_req.owner_approval = True
        borrow_req.save()
        context = {
            'success_msg':'Borrow request was approved!',
            'title':'Success!'
        }
        return render(request, 'diyexch_app/info.html', context)


@login_required()
def req_confirm(request, b_id):
    """Builds the borrow_tx onfirmation page
        Args:
            b_id <int>: Borrow_tx id
    """

    borrow_req = Borrow_tx.objects.get(id=b_id)
    return render(request, 'diyexch_app/req_confirm.html', {'req':borrow_req})


@login_required()
def search(request):
    """Search for a tool by name
    """

    # do a name search on the DB
    if request.method == "POST":
        query_by_name = request.POST.get('name', None)
        if query_by_name:
            results = Tool.objects.filter(name__icontains=query_by_name, visible=True)
            if not results:
                return render(request, 'diyexch_app/search.html', {"srch_error":["Sorry, no matching results found."]})
            else:
                return render(request, 'diyexch_app/search.html', {"tool_list":results, "title":"Search Results"})
        else:
            return render(request, 'diyexch_app/search.html', {"srch_error":["Sorry, could you please try that again?"]})
    else:
    # provide some random preview tools on the initial search (filler)
        id_list = Tool.objects.filter(visible=True).values_list('id', flat=True)
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


