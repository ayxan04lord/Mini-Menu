from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MenuItem(models.Model):
    name = models.CharField(max_length=200, verbose_name="Məhsul adı")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Qiymət (AZN)")
    class Meta:
        verbose_name = "Məhsul"
        verbose_name_plural = "Məhsullar"
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="İstifadəçi")
    items = models.ManyToManyField(MenuItem, related_name='orders', verbose_name="Sifariş elementləri")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sifariş tarixi")

    class Meta:
        verbose_name = "Sifariş"
        verbose_name_plural = "Sifarişlər"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.created_at:%Y-%m-%d %H:%M}"
