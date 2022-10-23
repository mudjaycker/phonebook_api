from tokenize import group
from django.db import models
from django.contrib.auth.models import User



class Group(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=26, default=f"No Group")
    created_at = models.DateTimeField(auto_now=True)

        
    def __str__(self):
        return f"{self.author.username}, {self.name}" 
    
    class Meta:
        unique_together = (('author', 'name'),)

class Contact(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=26, null=False, blank=False)
    number = models.CharField(max_length=26, null=False, blank=False, unique=True)
    favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.name}, {self.number}"