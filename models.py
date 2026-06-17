from django.db import models
from django.contrib.auth.models import User

class PatientRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    n_days = models.IntegerField()
    status = models.CharField(max_length=2)
    drug = models.CharField(max_length=20)
    age = models.IntegerField()
    sex = models.CharField(max_length=1)
    ascites = models.CharField(max_length=1)
    hepatomegaly = models.CharField(max_length=1)
    spiders = models.CharField(max_length=1)
    edema = models.CharField(max_length=1)
    bilirubin = models.FloatField()
    cholesterol = models.FloatField()
    albumin = models.FloatField()
    copper = models.FloatField()
    alk_phos = models.FloatField()
    sgot = models.FloatField()
    triglycerides = models.FloatField()
    platelets = models.FloatField()
    prothrombin = models.FloatField()
    stage = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Stage {self.stage}"
