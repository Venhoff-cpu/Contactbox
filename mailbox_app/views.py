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
    template_name = "person_detail.html"

    def get_context_data(self, person_id, **kwargs):
        ctx = {}
        person = get_object_or_404(Person, pk=person_id)
        ctx["person"] = person
        ctx["address"] = person.address
        ctx["addresses"] = Address.objects.all()
        ctx["phones"] = Phone.objects.filter(person=person.id)
        ctx["emails"] = Email.objects.filter(person=person.id)
        ctx["groups"] = Group.objects.filter(person=person.id)
        return ctx

    def get(self, request, person_id):
        return render(request, self.template_name, self.get_context_data(person_id))


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
        return render(request, "add_phone_to_person.html", {"phone_type": phone_type})

    def post(self, request, person_id):
        phone_type = request.POST.get("phone_type")
        phone_number = int(request.POST.get("phone_number"))
        person = get_object_or_404(Person, pk=person_id)
        new_phone = Phone.objects.create(
            type=phone_type,
            number=phone_number,
            person=person,
        )
        messages.add_message(request, messages.INFO, f"Dodano nowy numer telefonu: {phone_number}")
        return redirect("person", person_id=person_id)


class AddEmail(View):

    def get(self, request, person_id):
        mail_type = Email.TYPE_OF_MAIL
        return render(request, "add_maile_to_person.html", {"mail_type": mail_type})

    def post(self, request, person_id):
        mail_type = request.POST.get("mail_type")
        email = request.POST.get("email")
        person = get_object_or_404(Person, pk=person_id)
        new_email = Email.objects.create(
            type=mail_type,
            email=email,
            person=person,
        )
        messages.add_message(request, messages.INFO, f"Dodano nowy numer email: {email}")
        return redirect("person", person_id=person_id)


class ModifyPerson(PersonDetail):
    template_name = "modify_person.html"

    def post(self, request, person_id):
        person = get_object_or_404(Person, pk=person_id)
        person.first_name = request.POST.get("first_name")
        person.last_name = request.POST.get("last_name")
        person.description = request.POST.get("description")
        if request.FILES.get("photo"):
            person.photo = request.FILES.get("photo")
        person.address = Address.objects.get(pk=request.POST.get("address"))
        person.save()
        messages.add_message(request, messages.SUCCESS, "Zaktualizowano pomyślnie")
        return redirect("modify_person", person_id=person_id)


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
                                                         f"kontaktów")
            return redirect("main")
        else:
            messages.add_message(request, messages.INFO, f"nastąpił nieoczekiwany błąd")
            return redirect("main")


class DeletePhone(View):
    def get(self, request, phone_id):
        return render(request, "delete_phone.html")

    def post(self, request, phone_id):

        phone_to_delete = get_object_or_404(Phone, pk=phone_id)
        person_id = phone_to_delete.person.id
        if "Yes" in request.POST.get("del"):
            phone_to_delete.delete()
            messages.add_message(request, messages.INFO, f"Telefon usunięty.")

        return redirect("modify_person", person_id=person_id)


class DeleteEmail(View):
    def get(self, request, email_id):
        return render(request, "delete_email.html")

    def post(self, request, email_id):

        email_to_delete = get_object_or_404(Email, pk=email_id)
        person_id = email_to_delete.person.id
        if "Yes" in request.POST.get("del"):
            email_to_delete.delete()
            messages.add_message(request, messages.INFO, f"Email usunięty.")

        return redirect("modify_person", person_id=person_id)


class GroupsList(View):

    def get(self, request):
        group_list = Group.objects.all().order_by("name")
        paginator = Paginator(group_list, 50)

        page = request.GET.get("page")
        groups = paginator.get_page(page)
        ctx = {
            "groups": groups,
        }
        return render(request, "group_list.html", ctx)



class GroupDetail(View):
    pass


class AddGroup(View):
    pass


class DeleteGroup(View):
    pass


class AddPersonToGroup(View):
    pass


class SearchPerson(View):
    pass


class SearchPersonInGroup(View):
    pass
