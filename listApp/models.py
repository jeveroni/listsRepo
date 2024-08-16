from django.db import models
from django.utils import timezone

# Create your models here.

class List(models.Model):
    #Can have multiple lists for different things
    #Maybe have a specific list type which is like to do or to be bought etc and maybe that has a different vibe? (Future change?)
    name = models.CharField(max_length=50)
    
    def countItems(self):
        itemsList =  Item.objects.filter( list = self )
        return len( itemsList)
    
    def __str__(self):
        return self.name
    
class Item(models.Model):
    #Items belong to a list
    #I think we could have them as active and deactive so we wouldn't need to create each time? (Future change)
    #Possibly has a type as well, like Bakery etc if needed, or on the to do list it could be person based like jev/both/katie? (Future change)
    #Date? Required due date maybe? (Future change)
    #Created by (If we ever add users?) (Future change)
    name = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)
    list = models.ForeignKey( List, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name