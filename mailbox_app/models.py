from django.db import models


class Address(models.Model):
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=128)
    house_no = models.CharField(max_length=8)
    local_no = models.CharField(max_length=8, blank=True)
    postal_code = models.CharField(max_length=6)


class Person(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="person_photo/", null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)


class Phone(models.Model):
    DOMOWY = "1"
    SLUZBOWY = "2"

    TYPE_OF_PHONE = [
        (DOMOWY, "Domowy"),
        (SLUZBOWY, "Służbowy"),
    ]
    number = models.IntegerField()
    type = models.CharField(max_length=1, choices=TYPE_OF_PHONE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Email(models.Model):
    PRYWATNY = "1"
    SLUZBOWY = "2"

    TYPE_OF_MAIL = [
        (PRYWATNY, "Prywatny"),
        (SLUZBOWY, "Służbowy"),
    ]
    number = models.IntegerField()
    type = models.CharField(max_length=1, choices=TYPE_OF_MAIL)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Group(models.Model):
    name = models.CharField(max_length=124)
    person = models.ManyToManyField(Person, blank=True)

