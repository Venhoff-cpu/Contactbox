from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.db import IntegrityError

from .models import Person, Address, Email, Phone, Group


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
    def get(self, request, person_id):
        person = get_object_or_404(Person, pk=person_id)
        ctx = {
            "name": person.first_name,
            "last_name": person.last_name,
        }
        return render(request, "delete_person.html", ctx)

    def post(self, request, person_id):
        if "No" in request.POST.get("del"):
            return redirect("main")
        elif "Yes" in request.POST.get("del"):
            person_to_delete = get_object_or_404(Person, pk=person_id)
            person_name = person_to_delete.first_name
            person_surname = person_to_delete.last_name
            person_to_delete.delete()
            messages.add_message(request, messages.INFO, f"Uzytkownik {person_name} {person_surname} usunięty z "
                                                         f"listy uzytkowników")
            return redirect("main")
        else:
            messages.add_message(request, messages.INFO, f"nastąpił nieoczekiwany błąd")
            return redirect("main")


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
