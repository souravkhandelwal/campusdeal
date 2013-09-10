from django.db import models
import time

class User(models.Model):
    name = models.CharField(max_length=50)
    roll = models.CharField(max_length=10)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    isStudent = models.CharField(max_length=1)
    dept = models.CharField(max_length=5)
    sex = models.CharField(max_length=1)
    
class StudentAddress(models.Model):
    user = models.ForeignKey(User)
    hall = models.CharField(max_length=10)
    room = models.CharField(max_length=4)
    
class FacultyAddress(models.Model):
    user = models.ForeignKey(User)
    typename = models.CharField(max_length=30)
    houseno = models.CharField(max_length=5)
    
class Item(models.Model):
    sellerID = models.ForeignKey(User)
    category = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    s = time.strftime('%X').replace(':','')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/'+s)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    soldPrice = models.DecimalField(max_digits=10, decimal_places=2)
    
class Bidder(models.Model):
    item = models.ForeignKey(Item)
    bidderID = models.ForeignKey(User)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    
class History(models.Model):
    buyerID = models.ForeignKey(User)
    itemID = models.ForeignKey(Item)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
