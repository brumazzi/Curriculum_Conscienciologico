from __future__ import unicode_literals

from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    register = models.CharField(max_length=10)

    niver = models.CharField(max_length=12)
    nation = models.CharField(max_length=20,null=True)
    country = models.CharField(max_length=2,null=True)
    city = models.CharField(max_length=30,null=True)
    CEP = models.CharField(max_length=12,null=True)
    district = models.CharField(max_length=30,null=True)
    address = models.CharField(max_length=60,null=True)
    number = models.IntegerField(null=True)
    complement = models.CharField(max_length=15,null=True)

    phone = models.CharField(max_length=18,null=True)
    cell1 = models.CharField(max_length=18,null=True)
    cell2 = models.CharField(max_length=18,null=True)

    def __str__(self):
        fname = self.name.split(' ')
        lam = lambda(x): str(x[1][0]) if len(x) > 2 else ""
        return "%s %s%s." %(fname[len(fname)-1].upper(), str(fname[0][0]).upper(), lam(fname).upper())

class Projects(models.Model):
    title = models.CharField(max_length=120)
    char_key = models.CharField(max_length=360)
    date_pub = models.CharField(max_length=12)
    description = models.CharField(max_length=512)
    url = models.URLField()
    author = models.ManyToManyField(Author)

    def __str__(self):
        return self.title

class School(models.Model):
    date = models.CharField(max_length=12)
    grade = models.CharField(max_length=30)
    institute = models.CharField(max_length=100)
    phase = models.CharField(max_length=20)
    author = models.ForeignKey(Author)

    def __str__(self):
        return self.phase

class Education(models.Model):
    date = models.CharField(max_length=12)
    institute = models.CharField(max_length=100)
    educ_type = models.CharField(max_length=50)
    tecnologies = models.TextField()
    author = models.ForeignKey(Author)

class Jobs(models.Model):
    start = models.CharField(max_length=12)
    end = models.CharField(max_length=12,null=True)
    foundation = models.CharField(max_length=100)
    office = models.CharField(max_length=30)
    description = models.TextField()
    author = models.ForeignKey(Author)

class Lectures(models.Model):
    date = models.CharField(max_length=12)
    area = models.CharField(max_length=100)
    event_name = models.CharField(max_length=60)
    theme = models.CharField(max_length=60)
    place = models.CharField(max_length=30)
    author = models.ForeignKey(Author)
