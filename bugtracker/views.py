from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from bugtracker.models import Ticket, CustomUser
from bugtracker.forms import LoginForm, TicketForm
# Create your views here.

@login_required
def index(request):
    html = 'index.html'
    data = Ticket.objects.all()
    return render(request, html, {'data':data})


def loginUser(request):
    html = 'form.html'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('homepage'))
    form = LoginForm
    return render(request, html, {'form': form})


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))

@login_required
def CreateTicket(request, id):
    html = 'form.html'
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        user = CustomUser.objects.get(id=id)
        Ticket.objects.create(
            title=data['title'],
            description=data['description'],
            submitted_by=user
        )
        return HttpResponseRedirect(reverse('homepage'))
    form = TicketForm()
    return render(request, html, {'form': form})


def singleTicket(request,id):
    html = 'ticket.html'
    data = Ticket.objects.get(id=id)
    return render(request,html,{'data':data})

def assignTicket(request,ticketid,userid):
    html = 'ticket.html'
    data = Ticket.objects.get(id=ticketid)
    user = CustomUser.objects.get(id=userid)
    data.assigned_user = user
    data.status= 'in_progress'
    data.save()
    return render(request, html, {'data':data})

def completeTicket(request,ticketid,userid):
    html = 'ticket.html'
    data = Ticket.objects.get(id=ticketid)
    user = CustomUser.objects.get(id=userid)
    data.completed_by = user
    data.assigned_user = None
    data.status = 'done'
    data.save()
    return render(request, html, {'data': data})

def invalidateTicket(request,ticketid):
    html = 'ticket.html'
    data = Ticket.objects.get(id=ticketid)
    data.status='invalid'
    data.assigned_user = None
    data.completed_by = None
    data.save()
    return render(request, html, {'data': data})

@login_required
def userPage(request, id):
    html = 'user.html'
    data = CustomUser.objects.get(id=id)
    assignedTickets = Ticket.objects.filter(assigned_user = id)
    createdTickets = Ticket.objects.filter(submitted_by = id)
    completedTickets = Ticket.objects.filter(completed_by = id)
    return render(request, html, {'assignedTickets': assignedTickets, 
    'createdTickets': createdTickets,
    'completedTickets': completedTickets,
    'data':data})

def editTicket(request, ticketid):
    html = 'form.html'
    ticket = Ticket.objects.get(id=ticketid)
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ticket.title = data['title']
            ticket.description = data['description']
            ticket.save()
        return HttpResponseRedirect(reverse('homepage'))
    form = TicketForm()
    return render(request, html, {'form': form})