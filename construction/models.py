from django.db import models


class Services(models.Model):
    """Модель услуг"""

    SELECT_UNIT = [
        ("hour", "час"),
        ("square meter", "м2"),
        ("cubic meter", "м3"),
        ("ton", "т"),
        ("empty", " "),

    ]

    name = models.CharField(max_length=100, verbose_name="название услуги")
    description = models.CharField(max_length=500, verbose_name="описание услуги")
    price = models.IntegerField(verbose_name="цена")
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    unit_of_measurement = models.CharField(
        max_length=16,
        choices=SELECT_UNIT,
        verbose_name="Единица измерения",
        help_text="Выберите единицу измерения",
        default="hour",
    )

    def __str__(self):
        return f" {self.name} - {self.description} - {self.price}"

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["name", "price"]
