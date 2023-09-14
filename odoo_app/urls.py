"""odoo_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from odoo_app.views import Company, Contact, Project, Task, Lookups, User

urlpatterns = [
    # for CRUD Operation for Company
    path("company", Company.as_view()),
    path("company/<int:id>", Company.as_view()),
    # for CRUD Operation for Company
    path("contact", Contact.as_view()),
    path("contact/<int:id>", Contact.as_view()),
    # for CRUD Operation for Project
    path("project", Project.as_view()),
    path("project/<int:id>", Project.as_view()),
    # for CRUD Operation for Task
    path("task", Task.as_view()),
    path("task/<int:id>", Task.as_view()),
    # for CRUD Operation for Task
    path("user", User.as_view()),
    path("user/<int:id>", User.as_view()),
    # for get fileds for model
    path("get_fields", Lookups.as_view()),
]
