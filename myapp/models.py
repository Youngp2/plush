from django.db import models
import uuid

# Create your models here.

class Item(models.Model):
    profile_image = models.ImageField(upload_to='item_images/')
    name = models.CharField(max_length=20, null=False, blank=False)
    age = models.CharField(max_length=20, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    description = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable= False)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        
        
class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/')
    is_main = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Images for {self.item.name}"



