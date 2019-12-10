from django.db import models

# Create your models here.

class Fakultas(models.Model):
    nama = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nama

class MataKuliah(models.Model):
    fakultas = models.ForeignKey(Fakultas, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    kode = models.CharField(max_length=100)

    def toJSON(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "kode": self.kode
        }

    def __str__(self):
        return str(self.id) + " " + self.fakultas.nama + " : " + self.nama
