from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=30, null=True)
    username = models.CharField(max_length=30, unique=True, null=True)
    password = models.CharField(max_length=30,null=True)
    college = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    join_date = models.DateField(null=True)
    total_fees = models.DecimalField(max_digits=30, decimal_places=2)
    paid_fees = models.DecimalField(max_digits=30, decimal_places=2)
    left_fees = models.DecimalField(max_digits=30, decimal_places=2, null=True)
    phone = models.CharField(max_length=15, null=True)
    tech = models.CharField(max_length=30, null=True)
    image = models.ImageField(upload_to='images/')



class Feddback(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name