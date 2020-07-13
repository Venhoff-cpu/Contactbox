from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.core.files.storage import FileSystemStorage
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
    def get(self, request):
        return render(request, "add_person.html")

    def post(self, reuqest):
        name = reuqest.POST.get("first_name")
        surname = reuqest.POST.get("last_name")
        description = reuqest.POST.get("description")
        myfile = reuqest.FILES["photo"]
        person = Person.ojects.create(
            first_name=name,
            last_name=surname,
            description=description,
            photo=myfile.name
        )
        return redirect("main")


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
