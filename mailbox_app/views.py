from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.db import IntegrityError

from .models import Person, Address, Email, Phone, Group
# Create your views here.


class Main(View):
    def get(self, request):
        person_list = Person.objects.all().order_by("first_name", "last_name")
        paginator = Paginator(person_list, 50)

        page = request.GET.get("page")
        persons = paginator.get_page(page)
        ctx = {
            "persons": persons,
        }
        return render(request, "person_list.html", ctx)


class PersonDetail(View):
    pass


class AddPerson(View):
    def get(self, request):
        return render(request, "add_person.html")

    def post(self, reuqest):
        name = reuqest.POST.get("first_name")
        surname = reuqest.POST.get("last_name")
        description = reuqest.POST.get("description")
        myfile = reuqest.FILES.get("photo")
        person = Person.objects.create(
            first_name=name,
            last_name=surname,
            description=description,
            photo=myfile,
        )
        person.save()
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
