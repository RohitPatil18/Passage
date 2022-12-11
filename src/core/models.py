from django.db import models


class TimestampModel(models.Model):
    """
    This model contains timestamp fields to keep log of record
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(TimestampModel):
    """
    Accumulation of multiple models which are common across project
    """

    class Meta:
        abstract = True
