from django.db import models


class JobOpening(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    tech = models.CharField(max_length=100)
    reward = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"JobOpening[{self.pk}]: {self.company}"


class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"<Company[{self.id}]:{self.name}>"
