from django.shortcuts import render, redirect
from django.http import HttpResponse
from application.models import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .serializers import enquiry_tableSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import JsonResponse
# import openai

import requests
from django.shortcuts import render
from django.http import JsonResponse

from django.contrib.auth.models import User




# Create your views here.

def home(request):
    return render(request, 'index.html')

def aboutus(request):
    
    return render(request, 'about.html')

def problem_statement(request):
    return render(request, 'problem-statement.html')

def reg(request):
    
    if request.method == "POST":
        a = request.POST.get('name')
        b = request.POST.get('email')
        c = request.POST.get('phone')
        d = request.POST.get('message')
        e = request.POST.get('dropdown')
        enquiry = enquiry_table(name = a, email = b, phone = c, message = d, dropdown = e)
        enquiry.save()

        messages.success(request, 'Enquiry Form Submitted Successfully...')

        

    return render(request, 'contact.html')


def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username = username, password = password)

        if user is not None:
            
            login(request, user)
            request.session['username'] = username
            
            # Redirect to a success page.
            return redirect('dashboarddemo')
            
        else:
            # display 'invalid login' error message
            messages.error(request, 'In-correct username or password!..')
        
    
    return render(request, 'login.html')

@login_required(login_url='login')
def dashboard(request):

    # print('Hi, the User Name is: ',request.session.get('username_id'))

    username = request.session.get('username')

    return render(request, 'dashboard/index.html', {'username':username})

@login_required(login_url='login')
def enquiry_details(request):

    data = enquiry_table.objects.all()

    records = { 'abc':data }

    return render(request, 'dashboard/tables.html', records)

def delete_record(request, id):
    if request.method=='POST':
        data = enquiry_table.objects.get(pk=id)
        data.delete()
    return HttpResponseRedirect('/enquiry-details/')

def edit_record(request, id):
    info = enquiry_table.objects.filter(pk=id)
    
    data = {'abc':info}

    return render(request, 'dashboard/editrecord.html', data)

def update_record(request, id):
    info = enquiry_table.objects.get(pk=id)
    
    info.name = request.POST.get('name')
    info.email = request.POST.get('email')
    info.phone = request.POST.get('phone')
    info.message = request.POST.get('message')
    info.date_field = request.POST.get('date')
    info.save()
    
    return HttpResponseRedirect('/enquiry-details/')

def logout_user(request):
    logout(request)
    return redirect('/')

def reports(request):

    data = None
    
    if request.method=='POST':

        # from date and to date store into variable from form field data.
        from_date = request.POST.get('fromdate')
        to_date = request.POST.get('todate')
     
        # Convert the date strings to datetime objects
        
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()


        # Fetch the data from the table based on the date range
        searchresult = enquiry_table.objects.filter(date_field__range=[from_date, to_date])

        data = {"abc":searchresult}
    
    return render(request, 'dashboard/reports.html', data)


class student_data(APIView):
    def get(self, request, format=None):
        data = enquiry_table.objects.all()
        serializer = enquiry_tableSerializer(data, many=True)
        return Response(serializer.data)


def add_location(request):
    
    if request.method == 'POST':
        a = request.POST.get('name')

        info = DropdownOption(name = a)
        info.save()

    return render(request, 'dashboard/add_location.html')


def dropdown_view(request):
    info = DropdownOption.objects.all()
    data = {'options': info}
    return render(request, 'contact.html', data)


def signup(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        surname = request.POST.get('surname')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        myuser = User.objects.create_user(username, email, password)
        myuser.username = username
        
        myuser.save()

        messages.success(request, 'Congratulations, You are sign-up successfully, Now you can sign-in.. ')

        
    return render(request, 'signup.html')