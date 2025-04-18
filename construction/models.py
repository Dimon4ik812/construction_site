from django.db import models


class Services(models.Model):
    """Модель услуг"""

    name = models.CharField(max_length=100, verbose_name="название услуги")
    description = models.CharField(max_length=500, verbose_name="описание услуги")
    price = models.IntegerField(verbose_name="цена")
    image = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return f" {self.name} - {self.description} - {self.price}"

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["name", "price"]
