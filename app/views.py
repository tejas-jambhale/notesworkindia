# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout		
from .models import Notes, User, Label
from .forms import NoteForm
from django.http import HttpResponseRedirect
from .serializers import UserLoginSerializer, NotesSerializer, LabelSerializer
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from cryptography.fernet import Fernet
ENCRYPT_KEY = b'iDJpljxUBBsacCZ50GpSBff6Xem0R-giqXXnBFGJ2Rs='
key = Fernet.generate_key() #this is your "password"
cipher_suite = Fernet(key)

# Create your views here.
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
import base64
from .forms import SignUpForm

def encrypt(txt):
    try:
        # convert integer etc to string first
        txt = str(txt)
        # get the key from settings
        cipher_suite = Fernet(ENCRYPT_KEY) # key should be byte
        # #input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii") 
        return encrypted_text
    except Exception as e:
        # log the error if any
        print(e)
        return None


def decrypt(txt):
    try:
        # base64 decode
        txt = base64.urlsafe_b64decode(txt)
        cipher_suite = Fernet(ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(txt).decode("ascii")     
        return decoded_text
    except Exception as e:
        # log the error
        print(e)
        return None


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    #return render(request, 'signup.html', {'form': SignUpForm()})
    return Response({"success": False, "msg": "something went wrong"}, status=status.HTTP_401_UNAUTHORIZED)
    

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        #print(request.data)
        try:
            if 'username' in request.data and 'password' in request.data:
                user = authenticate(username=request.data['username'], password=request.data['password'])
                if user is not None:
                    login(request, user)
                    serializer = UserSerializer(user)
                    return Response({"success": True, "msg": "You are logged-in successfully"})
                else:
                    return Response({"success": False, "msg": "Incorrect Password"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"success": False, "msg": "Username & password is required"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e) 
            return Response({"success": False, "msg": "something went wrong"}, status=status.HTTP_401_UNAUTHORIZED)



class CreateNoteView(generics.ListCreateAPIView):
    serializer_class = NotesSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Notes.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}


    def filter_queryset(self, queryset):
        return queryset.filter(user =self.request.user)


class ListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = 'my_note'  
    queryset = Notes.objects.all()  
    template_name = 'listnotes.html'  

    def get_queryset(self):
        return Notes.objects.filter(user=self.request.user)


class NotesView(LoginRequiredMixin, DetailView):
    model = Notes
    query = Notes.objects.all()
    for i in range(len(query)):
        query[i].note = decrypt(query[i].note)
        print(query[i].note,2)
    slug_field = 'note_id'
    context_object_name = 'my_note'
    template_name = 'detailnotes.html'  
    def get_queryset(self):
        query = Notes.objects.all()
        for i in range(len(query)):
            query[i].note = decrypt(query[i].note)
            print(query[i].note,2)
        return query



def AddView(request):
    user = request.user
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.note = encrypt(new_note.note)
            
            
            new_note.save()
            return HttpResponseRedirect('/sites/list/')
    return render(request, 'notepage.html', {'form': NoteForm()})
    #return Response({"success": False, "msg": "something went wrong"}, status=status.HTTP_401_UNAUTHORIZED)
    
