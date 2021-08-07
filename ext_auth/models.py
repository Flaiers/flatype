from django.db import models
from django.contrib.auth import get_user_model


actual_user_model = get_user_model()


class ExternalHashId(models.Model):
    user = models.ForeignKey(actual_user_model, on_delete=models.CASCADE)
    session = models.CharField(max_length=32, unique=True, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = "External hash id"
        verbose_name_plural = "External hash id's"
