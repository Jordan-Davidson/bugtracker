from django.urls import path
from bugtracker import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('login/', views.loginUser),
    path('user/<int:id>/', views.userPage),
    path('createTicket/<int:id>/', views.CreateTicket),
    path('ticket/<int:id>/', views.singleTicket),
    path('assign/<int:ticketid>/<int:userid>/', views.assignTicket),
    path('complete/<int:ticketid>/<int:userid>/', views.completeTicket),
    path('invalid/<int:ticketid>/', views.invalidateTicket),
    path('edit/<int:ticketid>/', views.editTicket)
]
