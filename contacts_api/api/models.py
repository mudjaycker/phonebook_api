from django.db import models
from django.contrib.auth.models import User



class Group(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=26, unique=True, default="No Group")
    created_at = models.DateTimeField(auto_now=True)
    
    @classmethod
    def default(cls):
        group, created = cls.objects.get_or_create(name="No Group")
        return group.name
    
    def __str__(self):
        return str(self.name)

class Contact(models.Model):
    name = models.CharField(max_length=26, null=False, blank=False)
    number = models.CharField(max_length=26, null=False, blank=False, unique=True)
    favorite = models.BooleanField(default=False)
    group = models.ForeignKey(Group, to_field="name", default=Group.default, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.number}"