from django.db import models
from django.contrib.auth.models import User
from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator

CITY_CHOICES = (
    ('ludhiana', 'LUDHIANA'),
    ('chandigarh', 'CHANDIGARH'),
)

ITEM_CHOICES = (
    ('school bag', 'SCHOOL BAG'),
    ('hand bag', 'HAND BAG'),
    ('travelling bag', 'TRAVELLING BAG'),
)


class city(models.Model):
    id = models.AutoField(primary_key=True, blank=True, null=False)

    city = models.CharField(
        max_length=20,

        choices=CITY_CHOICES,
        default='ludhiana'
    )

    def __str__(self):
        return self.city


class item(models.Model):
    item = models.CharField(
        max_length=20,

        choices=ITEM_CHOICES,
        default='schoolbag'
    )
    stock = models.CharField(max_length=7, default="10000")

    def __str__(self):
        return self.item


class customer(models.Model):
    id = models.AutoField(primary_key=True, blank=True, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phoneNumberRegex = RegexValidator(
        regex=r"^\+?1?\d{8,15}$", message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phoneNumberRegex], max_length=16, unique=True)
    #phone_number = PhoneNumberField(unique=True, null=False, blank=False)
    city = models.ForeignKey(
        city, on_delete=models.CASCADE, blank=True, null=False, default='')
    item = models.ForeignKey(
        item, on_delete=models.CASCADE, blank=True, null=False, default='')

    timestamp = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=False)

    def __str__(self):
        return self.first_name


class person(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    in_persons = models.PositiveIntegerField(default=0)
    out_persons = models.PositiveIntegerField(default=0)
    total_persons = models.PositiveIntegerField(default=0)
