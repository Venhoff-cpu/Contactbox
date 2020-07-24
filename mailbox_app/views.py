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
    def get(self, request, person_id):
        ctx = {}
        person = get_object_or_404(Person, pk=person_id)
        ctx["person"] = person
        ctx["address"] = person.address
        ctx["phones"] = Phone.objects.filter(person=person.id)
        ctx["emails"] = Email.objects.filter(person=person.id)
        ctx["groups"] = Group.objects.filter(person=person.id)
        return render(request, "person_detail.html", ctx)


class AddPerson(View):
    def get(self, request):
        ctx = {
            "addresses": Address.objects.all()
        }
        return render(request, "add_person.html", ctx)

    def post(self, request):
        name = request.POST.get("first_name")
        surname = request.POST.get("last_name")
        description = request.POST.get("description")
        my_file = request.FILES.get("photo")
        address_id = request.POST.get("address")
        print(address_id)
        address = Address.objects.get(pk=request.POST.get("address"))
        new_person = Person.objects.create(
            first_name=name,
            last_name=surname,
            description=description,
            photo=my_file,
            address=address,
        )
        return redirect("person", person_id=new_person.id)


class AddAddress(View):

    def get(self, request):
        return render(request, "add_address.html")

    def post(self, request):
        city_name = request.POST.get("city")
        street_name = request.POST.get("street")
        house = request.POST.get("house_no")
        local = request.POST.get("local_no")
        postal = request.POST.get("postal_code")
        new_address = Address.objects.create(
            city=city_name,
            street=street_name,
            house_no=house,
            local_no=local,
            postal_code=postal,
        )
        new_address.save()
        messages.add_message(request, messages.INFO, f"Dodano nowy adres")
        return redirect("main")


class AddPhone(View):

    def get(self, request, person_id):
        phone_type = Phone.TYPE_OF_PHONE
        return render(request, "add_phone_to_person.html", {"phone_type":phone_type})

    def post(self, request, person_id):
        phone_type = request.POST.get("phone_type")
        phone_number = int(request.POST.get("phone_number"))
        person = Person.objects.get(pk=person_id)
        new_phone = Phone.objects.create(
            type=phone_type,
            number=phone_number,
            person=person,
        )
        return redirect("person", person_id=person_id)


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
