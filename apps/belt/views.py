from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *
import re

def index(request):
    return render(request, 'belt/login.html')

def home(request):
    context = {
            'user':  User.objects.get(id=request.session['id']),
            'quotes': Quote.objects.exclude(fave__person_id=request.session['id']),
            'lists': List.objects.filter(person_id=request.session['id'])
    }
    return render(request, 'belt/quotes.html', context)

def process(request, quotes_id):
    quotes_id = quotes_id
    person_id = request.session['id']
    List.objects.create(quotes_id=quotes_id, person_id=person_id)
    return redirect('belt:home')

def create(request):
    if len(request.POST['html_author']) < 3:
        messages.error(request, 'Author must be at least 3 characters!. Do not be such a MARK!!!')
        return redirect('belt:home')
    if len(request.POST['html_quote']) < 10:
        messages.error(request, 'Quote must be at least 10 characters!. Do not be such a Nigam!!!')
        return redirect('belt:home')
    author = request.POST['html_author']
    text = request.POST['html_quote']
    Quote.objects.create(author=author, text=text, poster_id=request.session['id'])
    return redirect('belt:home')

def remove(request, quotes_id):
    quotes_id= quotes_id
    person_id = request.session['id']
    List.objects.filter(quotes_id=quotes_id, person_id=person_id).delete()
    return redirect('belt:home')

def userPage(request, user_id):
    context = {
            'user': User.objects.get(id=user_id),
            'posts': Quote.objects.filter(poster_id=user_id),
            'count': Quote.objects.filter(poster_id=user_id).count()
    }
    return render(request, 'belt/user.html', context)


def login(request):
    is_valid = True
    if not User.objects.email_validate(request.POST['html_email']):
        messages.error(request, 'Invalid email!')
        is_valid = False
        return redirect('belt:index')
    if User.objects.get(email = request.POST['html_email']).password != request.POST['html_password']:
        messages.error(request, 'Password is incorrect!')
        is_valid = False
        return redirect('belt:index')
    if is_valid:
        user = User.objects.get(email=request.POST['html_email'])
        request.session['id'] = user.id
        print "+++++++++++++++++++++++++++"
        print request.session['id']
        return redirect('belt:home')

def register(request):
    is_valid = True
    if len(request.POST['html_email']) < 4:
        messages.add_message(request,messages.ERROR,'Email must be at least 4 characters!')
        is_valid = False
    if len(request.POST['html_name']) < 2:
        messages.add_message(request,messages.ERROR, 'Name must be at least 3 characters!')
        is_valid = False
    if len(request.POST['html_alias']) <2:
        messages.add_message(request,messages.ERROR, 'Alias must be at least 3 characters!')
        is_valid = False
    if not User.objects.email_validate(request.POST['html_email']):
        messages.add_message(request,messages.ERROR, 'Invalid email!')
        is_valid = False
    if not User.objects.pw_validate(request.POST['html_password'], request.POST['html_confirm']):
        messages.add_message(request,messages.ERROR, "passwords don't match")
        is_valid = False
    if is_valid:
        user = User.objects.create(email = request.POST['html_email'], name=request.POST['html_name'], alias=request.POST['html_alias'], password=request.POST['html_password'], dateofbirth=request.POST['html_date'])
        request.session['id'] = user.id

        return redirect('belt:home')
    else:
        return redirect('/')

def logout(request):
    del request.session['id']
    return redirect('belt:index')
