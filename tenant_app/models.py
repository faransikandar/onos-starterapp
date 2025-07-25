from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="members")

    def __str__(self):
        return self.name