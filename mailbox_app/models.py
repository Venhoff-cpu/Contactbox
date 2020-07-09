from django.db import models

# Create your models here.


class Person(models.Model):
    first_name = models.CharField(max_lenght=64)
    last_name = models.CharField(max_lenght=64)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="person_photo", null=True)


class Address(models.Model):
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=128)
    house_no = models.CharField(max_length=8)
    local_no = models.CharField(max_length=8, blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


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
        (PRYWATNY, "PRYWATNY"),
        (SLUZBOWY, "Służbowy"),
    ]
    number = models.IntegerField()
    type = models.CharField(max_length=1, choices=TYPE_OF_MAIL)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Group(models.Model):
    name = models.CharField(max_length=124)
    person = models.ManyToManyField(Person, blank=True)

