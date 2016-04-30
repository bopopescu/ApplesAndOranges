from django.db import models
from .mixins import InstanceDeleteQuerySetMixin


class InstanceDeleteQuerySet(InstanceDeleteQuerySetMixin, models.QuerySet):
    """Concrete class for deleting instances using `delete` method on model
    instance instead of deleting using `QuerySet` method
    """
    pass
