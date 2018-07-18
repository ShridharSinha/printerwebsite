"""InnovationHubWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #admin
    path('admin/', admin.site.urls),

    #HomePage
    path('', views.HomePage),
    path('home/', views.HomePage),

    #Schedule
    path('schedule/', views.Schedule),
    path('printData/<int:jobid>', views.PrintData),

    #Submit
    path('submit/', views.Submission),
    path('submit/request/', views.Submission),
    path('submit/preview/', views.Preview),
    path('submit/form/', views.SubmissionForm),
    path('submit/success/', views.Success),
    path('submit/fail/', views.Fail),

    #Account
    path('account/', views.AccountData),
    path('account/data/', views.AccountData),
    path('account/edit/', views.EditAccount),
    path('account/login/', views.Login),

    #CarlSegment
    path('carlSegment/', views.CarlPage),

    #FeaturedPrints
    path('featuredPrints/', views.Featured),

    #Layout
    path('layout/', views.Layout),
]
