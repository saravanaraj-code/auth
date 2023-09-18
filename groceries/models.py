from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    CATEGORIES = (
        ('Vegetables', 'Vegetables'),
        ('Fruit', 'Fruit'),
        ('Meat', 'Meat'),
        ('Vegan', 'Vegan'),
        ('Seasoning', 'Seasoning'),
        ('Sweet', 'Sweet'),
        ('Drink', 'Drink')
    )
    name = models.CharField(primary_key=True, max_length=20, choices=CATEGORIES)

    class Meta:
        db_table = "Categories"

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(null=False, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
