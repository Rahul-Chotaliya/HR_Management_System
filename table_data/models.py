from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Department(models.Model):
    dep_name = models.CharField(max_length=25, verbose_name="Department Name")

    def __str__(self):
        return str(self.dep_name)


GENDER_CHOICES = (
    ("0", "Male"),
    ("1", "Female"),
)


class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=255, default=None, null=True)
    dep = models.ForeignKey('Department', null=True,blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, default=None, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.age}'

    class Meta:
        ordering = ['id']

    # @property
    # def age_text(self):
    #     if self.age < 18:
    #         result = "Minor"
    #     elif 18 < self.age < 50:
    #         result = "Young"
    #     else:
    #         result = "Senior"
    #     return result


class Author(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()


class Publisher(models.Model):
    name = models.CharField(max_length=255)


class Book(models.Model):
    name = models.CharField(max_length=255)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()


class Store(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name='store_list')


class Publication(models.Model):
    title = models.CharField(max_length=255)


class Article(models.Model):
    headline = models.CharField(max_length=255)
    publications = models.ManyToManyField(Publication)


class VerifyOtp(models.Model):
    otp = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    exp = models.DateTimeField()


#
# b1 =
# b2 =
# b3 =
#
# s = Store(name="test")
# s.save()
# s.books.add(b3)
# # s.books.add(b1)
# s.books.remove(b3)
# s.books.add(b1, b2)
# s.books.set([b1, b2])