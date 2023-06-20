from django.db import models


class Society(models.Model):
    name = models.CharField(max_length=100)
    rut = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Partner(models.Model):
    name = models.CharField(max_length=100)
    rut = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    participation = models.DecimalField(max_digits=5, decimal_places=2)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Administrator(models.Model):
    name = models.CharField(max_length=100)
    rut = models.CharField(max_length=20)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Faculty(models.Model):
    name = models.CharField(max_length=100)
    administrator = models.ForeignKey(Administrator, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
