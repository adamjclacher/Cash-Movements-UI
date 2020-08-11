from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # imports form
from django.contrib.auth.models import User # imports user model
from django.db import IntegrityError # imports IntegrityError to check usernames awready taken
from django.contrib.auth import login, logout, authenticate # imports login and Logout function
from .forms import TodoForm, ListForm, cashMovementRequestForm, deleteCashMovementRequestForm
from .models import Todo, clientAccount, cashMovementRequest, action
from django.utils import timezone
from django.contrib.auth.decorators import login_required # import code to restrict code to only logged in users
import string
import re
from django.contrib import messages
import datetime as dt
from datetime import date
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime

#User Permissions

createClientAccounts = ["John Simm","Steve Jobs","Tim Cook","Rosa Parks","Steve Wozniak","Gillian McLelland", "David Brown", "Adam Clacher"]
createCashMovemement = ["John Simm","Steve Jobs","Tim Cook","Rosa Parks", "Adam Clacher"]
verifyClientAccounts = ["John Simm","Steve Jobs","Steve Wozniak", "Adam Clacher"]
asuraAccounts = ["Gillian McLelland","David Brown","Steve Wozniak", "Adam Clacher"]

#Sending emails testroom

def sendEmail():
    #send_mail(subject, message, from_email,to_list,fail_silently=True)
    subject = "IBP Cash Movement Request"
    message = "Hello there,\n\nA new cash movement request has been added, please fill in the Asura details and process the request.\n\n www.thisisalink.com \n\nThank you."
    from_email = settings.EMAIL_HOST_USER
    to_list = ["adam.clacher@asurafin.com",]
    send_mail(subject, message, from_email,to_list,fail_silently=True)

def sendCancellationEmail(accountName, cancellationMessage, amount, currency):
    #send_mail(subject, message, from_email,to_list,fail_silently=True)
    subject = "IBP Cash Movement Request"
    message = f"Hello there,\n\nA cash movement request for {accountName} has been cancelled. The reason for the cancellation is written below:\n\n{cancellationMessage} \n\n www.thisisalink.com \n\nThank you."
    from_email = settings.EMAIL_HOST_USER
    to_list = ["adam.clacher@asurafin.com",]
    send_mail(subject, message, from_email,to_list,fail_silently=True)




# Create your views here.

def home(request):
    return render(request, "todo/home1.html")

def signupuser(request):
    if request.method == "GET":
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':"Someone has already taken that username. Try another..."})
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':"Passwords did not match"})

def loginuser(request):
    if request.method == "GET":
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match...'})
        else:
            login(request, user)
            return redirect('home')

@login_required
def logoutuser(request):
    if request.method =="POST":
        logout(request)
        return redirect('home')






_country2length = dict(
    AL=28, AD=24, AT=20, AZ=28, BE=16, BH=22, BA=20, BR=29,
    BG=22, CR=21, HR=21, CY=28, CZ=24, DK=18, DO=28, EE=20,
    FO=18, FI=18, FR=27, GE=22, DE=22, GI=23, GR=27, GL=18,
    GT=28, HU=28, IS=26, IE=22, IL=23, IT=27, KZ=20, KW=30,
    LV=21, LB=28, LI=21, LT=20, LU=20, MK=19, MT=31, MR=27,
    MU=30, MC=27, MD=24, ME=22, NL=18, NO=15, PK=24, PS=29,
    PL=28, PT=25, RO=24, SM=27, SA=24, RS=22, SK=24, SI=19,
    ES=24, SE=24, CH=21, TN=24, TR=26, AE=23, GB=22, VG=24 )

testVar = str(1)

orderVar = "provider"


def about(request):
	my_name = "Adam Clacher"
	version = 4.0
	context = {
	'name': my_name,
	'version': version,
	}
	return render(request, 'todo/about.html', context)

def delete(request, list_id):
    username = request.user.username
    username = str(username)
    if username in asuraAccounts:
        item = clientAccount.objects.get(pk=list_id)
        actionDescription = f"Deleted {item.accountName}'s client account"
        createAction(request, actionDescription)
        item.delete()
        return redirect("home")
    else:
        messages.success(request, (f"You aren't authorised to delete client accounts."))
        return redirect("home")

def cross_off(request, list_id):
    username = request.user.username
    username = str(username)
    if username in verifyClientAccounts:
        item = clientAccount.objects.get(pk=list_id)
        if item.presentOnDrive == True:
            userCreated = str(item.user)
            if userCreated == username:
                messages.success(request,(f"You cannot verify clients added by yourself, please ask someone else to verify."))
                return redirect("home")
            else:
                item.completed = True
                item.dateVerified = date.today()
                actionDescription = f"Verified {item.accountName}'s client account"
                createAction(request, actionDescription)
                item.save()
                return redirect("home")
        else:
            messages.success(request,(f"This client account is not marked as present on drive."))
            return redirect("home")
    else:
        messages.success(request,(f"You aren't authorised to verify client accounts."))
        return redirect("home")

def uncross(request, list_id):
    username = request.user.username
    if username in verifyClientAccounts:
        item = clientAccount.objects.get(pk=list_id)
        userCreated = str(item.user)
        if userCreated == username:
            messages.success(request,(f"You cannot unverify clients added by yourself, please ask someone else to unverify."))
            return redirect("home")
        else:
            item.completed = False
            item.dateVerified = None
            actionDescription = f"Unverified {item.accountName}'s client account"
            createAction(request, actionDescription)
            item.save()
            return redirect("home")
    else:
        messages.success(request, (f"You aren't authorised to do that."))
        return redirect("home")

def edit(request, list_id):
    if request.method == "POST":
        item = clientAccount.objects.get(pk=list_id)
        iban = request.POST.get("IBAN")
        form = ListForm(request.POST or None, instance = item)
        if valid_iban(iban):
            if form.is_valid():
                form.save()
                actionDescription = f"Edited {item.accountName}'s client account"
                createAction(request, actionDescription)
                messages.success(request, (f"Item has been edited successfuly"))
                return redirect("home")
            else:
                messages.sucess(request, ("Cannot edit account - One or more required fields have been left blank."))
                item = clientAccount.objects.get(pk=list_id)
                return render(request, 'todo/edit.html', {'item':item} )
        else:
            messages.success(request, (f"Cannot edit account - IBAN {iban} has not passed validation"))
            item = clientAccount.objects.get(pk=list_id)
            return render(request, 'todo/edit.html', {'item':item})
    else:
        item = item = clientAccount.objects.get(pk=list_id)
        return render(request, 'todo/edit.html', {'item':item})

def editRequest(request, list_id):
    if request.method == "POST":
        item = cashMovementRequest.objects.get(pk=list_id)
        form = cashMovementRequestForm(request.POST or None, instance=item)
        if form.is_valid():
            form.save()
            actionDescription = f"Edited a cash movement request for {item.accountName}'s client account"
            createAction(request, actionDescription)
            messages.success(request, (f"Item has been edited successfuly"))
            return redirect('home')
        else:
            messages.success(request, (f"Cannot edit account - One more more fields was left blank"))
            item = cashMovementRequest.objects.get(pk=list_id)
            return render(request, 'todo/editRequest.html', {'item':item})
    else:
        item = cashMovementRequest.objects.get(pk=list_id)
        return render(request, 'todo/editRequest.html', {'item':item})

def changePassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.success(request, (f"Password change unsuccessful - Please try again"))
            return redirect('changePassword')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request, 'todo/password_change_form.html', args)

def addClient(request):

    if request.method == "POST":
        iban = request.POST.get('IBAN')
        form = ListForm(request.POST or None)
        if form.is_valid():
            if valid_iban(iban):
                newClient = form.save(commit=False)
                newClient.user = request.user
                actionDescription = f"Created a new client account, {newClient.accountName}"
                createAction(request, actionDescription)
                newClient.save()
                all_items = clientAccount.objects.all#queerying the database
                messages.success(request, (f"Account has been added to the list!"))
                return redirect('home')
            else:
                messages.success(request, (f"IBAN did not pass validation tests."))
                all_items = clientAccount.objects.all
                return render(request, 'todo/addClient.html', {'all_items':all_items})
        else:
            messages.success(request, ("Cannot add account - One or more required fields had been left blank."))
            all_items = clientAccount.objects.all#queerying the database
            return render(request, 'todo/addClient.html', {'all_items':all_items})
    else:
        username = request.user
        username = str(username)
        if username in createClientAccounts:
            all_items = clientAccount.objects.all#queerying the database
            return render(request, 'todo/addClient.html', {'all_items':all_items})
        else:
            messages.success(request, (f"{username}, you aren't authorised to create client accounts."))
            return redirect('home')



def valid_iban(iban):
    # Ensure upper alphanumeric input.
    iban = iban.replace(' ','').replace('\t','')
    if not re.match(r'^[\dA-Z]+$', iban):
        return False
    # Validate country code against expected length.
    if len(iban) != _country2length[iban[:2]]:
        return False
    # Shift and convert.
    iban = iban[4:] + iban[:4]
    digits = int(''.join(str(int(ch, 36)) for ch in iban)) #BASE 36: 0..9,A..Z -> 0..35
    return digits % 97 == 1



@login_required
def home(request):
    search_term = ""
    if request.method =="POST":
        form=ListForm(request.POST or None)
        if form.is_valid():
            form.save()
            all_items=clientAccount.objects.order_by(orderVar)
            cashMovementRequests=cashMovementRequest.objects.order_by('-dateRequested')
            cashMovementRequestsComplete=cashMovementRequest.objects.order_by('-dateRequested')
            messages.success(request,("Item has been added to the list!"))
            return render(request, "todo/home.html", {'all_items':all_items, 'cashMovementRequests':cashMovementRequests, 'cashMovementRequestsComplete':cashMovementRequestsComplete})
    else:
        all_items=clientAccount.objects.order_by(orderVar)
        cashMovementRequestsComplete=cashMovementRequest.objects.order_by('-dateRequested')
        cashMovementRequests=cashMovementRequest.objects.order_by('-dateRequested')

        if "search" in request.GET:
            search_term = request.GET['search']
            all_items= all_items.filter(
            Q(accountName__icontains=search_term) |
            Q(provider__icontains=search_term) |
            Q(currency__icontains=search_term) |
            Q(sortCodeABACA__icontains=search_term) |
            Q(IBAN__icontains=search_term) |
            Q(SWIFT__icontains=search_term) |
            Q(bankAccountNumber__icontains=search_term) |
            Q(accountNumber__icontains=search_term) )
        elif "searchRequests" in request.GET:
            search_term = request.GET['searchRequests']
            cashMovementRequests = cashMovementRequests.filter(
            Q(withdrawlOrDeposit__icontains=search_term) |
            Q(amount__icontains=search_term) |
            Q(currency__icontains=search_term) |
            Q(provider__icontains=search_term) |
            Q(accountNumber__icontains=search_term) |
            Q(accountName__icontains=search_term) |
            Q(sortCodeABACA__icontains=search_term) |
            Q(bankAccountNumber__icontains=search_term) |
            Q(IBAN__icontains=search_term) |
            Q(asuraInternalNarrative__icontains=search_term) |
            Q(asuraPaymentIDLloyds__icontains=search_term) |
            Q(asuraPaymentIDProvider__icontains=search_term))
        elif "searchCompletedRequests" in request.GET:
            search_term = request.GET['searchCompletedRequests']
            cashMovementRequestsComplete = cashMovementRequestsComplete.filter(
            Q(withdrawlOrDeposit__icontains=search_term) |
            Q(amount__icontains=search_term) |
            Q(currency__icontains=search_term) |
            Q(provider__icontains=search_term) |
            Q(accountNumber__icontains=search_term) |
            Q(accountName__icontains=search_term) |
            Q(sortCodeABACA__icontains=search_term) |
            Q(bankAccountNumber__icontains=search_term) |
            Q(IBAN__icontains=search_term) |
            Q(asuraInternalNarrative__icontains=search_term) |
            Q(asuraPaymentIDLloyds__icontains=search_term) |
            Q(asuraPaymentIDProvider__icontains=search_term))

        return render(request, 'todo/home.html', {'all_items':all_items, 'cashMovementRequests':cashMovementRequests, 'cashMovementRequestsComplete':cashMovementRequestsComplete,})



@login_required
def orderBy(request, order):
    global orderVar
    orderVar = order
    return redirect('home')

def orderBySelect(request, order):
    all_items=clientAccount.objects.order_by(order)
    global orderVar
    orderVar = order
    return render(request, 'todo/selectAccount.html', {'all_items':all_items,})

def viewRequest(request, list_id):
	item = cashMovementRequest.objects.get(pk=list_id)#queerying the database
	return render(request, 'todo/viewRequest.html', {'item':item})

def viewAccount(request, list_id):
	item = clientAccount.objects.get(pk=list_id)#queerying the database
	return render(request, 'todo/viewAccount.html', {'item':item})

def selectAccount(request):
    if request.method =="GET":
        username = request.user
        username = str(username)
        if username in createCashMovemement:
            all_items=clientAccount.objects.order_by(orderVar)
            cashMovementRequests=cashMovementRequest.objects.order_by('-dateRequested')

            if "search" in request.GET:
                search_term = request.GET['search']
                all_items= all_items.filter(
                Q(accountName__icontains=search_term) |
                Q(provider__icontains=search_term) |
                Q(currency__icontains=search_term) |
                Q(sortCodeABACA__icontains=search_term) |
                Q(IBAN__icontains=search_term) |
                Q(SWIFT__icontains=search_term) |
                Q(bankAccountNumber__icontains=search_term) |
                Q(accountNumber__icontains=search_term) )
            return render(request, 'todo/selectAccount.html', {'all_items':all_items,})
        else:
            messages.success(request, (f"{username}, you aren't authorised to request cash movements."))
            return redirect('home')

def addCashMovementRequest(request, list_id):

    if request.method == "POST":
        form = cashMovementRequestForm(request.POST or None)
        if form.is_valid():
            newMovement = form.save(commit=False)
            newMovement.user = request.user
            newMovement.save()
            sendEmail()
            actionDescription = "Added cash movement request"
            createAction(request, actionDescription)
            messages.success(request, (f"An e-mail has been sent to Asura to notify them of your new request."))
            return redirect('home')
        else:
            item = clientAccount.objects.get(pk=list_id)
            messages.success(request,("Could not request cash movement - One or more fields was left blank"))
            return render(request, 'todo/addNewRequest.html', {'account':item})
    else:
        username = request.user
        username = str(username)
        if username in createCashMovemement:
            item = clientAccount.objects.get(pk=list_id)
            return render(request, 'todo/addNewRequest.html', {'account':item})
        else:
            messages.success(request, (f"{username}, you aren't authorised to request cash movements."))
            return redirect('home')



def createAction(request, actionDescription):
    actionModel = action(user = request.user, description = actionDescription, created=datetime.now())
    time = datetime.now()
    actionModel.save()


def deleteRequest(request, list_id):
    username = request.user.username
    username = str(username)
    if username in asuraAccounts:
        if request.method == "POST":
            item = cashMovementRequest.objects.get(pk=list_id)
            form = deleteCashMovementRequestForm(request.POST or None, instance=item)
            form.save()
            actionDescription = f"Deleted a cash movement request of {item.amount} {item.currency} for {item.accountName}'s client account"
            createAction(request, actionDescription)
            messages.success(request, (f"Item has been deleted successfuly, an email has been sent to IBP to notify them of this."))
            sendCancellationEmail(item.accountName, item.cancellationMessage, item.amount, item.currency)
            item.delete()
            return redirect('home')
        else:
            item = cashMovementRequest.objects.get(pk=list_id)
            if item.completed == False:
                return render(request, 'todo/deleteRequest.html', {'item':item})
            else:
                actionDescription = f"Deleted a completed cash movement request of {item.amount} {item.currency} for {item.accountName}'s client account"
                createAction(request, actionDescription)
                item.delete()
                messages.success(request, (f"Cash movement sucessfully deleted."))
                return redirect('home')
    else:
        messages.success(request, (f"You aren't authorised to delete cash movement requests."))
        return redirect('home')

def complete(request, list_id):
    username = request.user.username
    username = str(username)
    if username in asuraAccounts:
        item = cashMovementRequest.objects.get(pk=list_id)
        item.dateCompleted = dt.datetime.today()
        item.completed = True
        item.userCompleted = str(username)
        actionDescription = f"Marked cash movement request for {item.accountName} as complete"
        createAction(request, actionDescription)
        item.save()
        return redirect("home")
    else:
        messages.success(request, (f"You aren't authorised to mark cash movement requests as complete."))
        return redirect('home')

def activityLog(request):
    return render(request, 'todo/activityLog.html')

months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def activityLogMonth(request, month_id):
    search_term = ""
    month_id = int(month_id)
    actions=action.objects.order_by('-created')
    if "search" in request.GET:
        search_term = request.GET['search']
        actions= actions.filter(
        Q(description__icontains=search_term) )
    return render(request, 'todo/activityLogMonth.html',{'actions':actions, 'monthSelectedNumber':month_id+1, 'monthSelected':months[month_id]})
