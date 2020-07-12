from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.db import IntegrityError

from .models import Person, Address, Email, Phone, Group
# Create your views here.


class Main(View):
    def get(self, request):
        return render(request, "person_list.html")


class PersonDetail(View):
    pass


class AddPerson(View):
    pass


class AddAddress(View):
    pass


class AddPhone(View):
    pass


class AddEmail(View):
    pass


class ModifyPerson(View):
    pass


class DeletePerson(View):
    pass


class GroupsList(View):
    pass


class GroupDetail(View):
    pass


class AddGroup(View):
    pass


class AddPersonToGroup(View):
    pass


class SearchPerson(View):
    pass


class SearchPersonInGroup(View):
    pass
