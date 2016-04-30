from django.db import models


class CreationModificationMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class InstanceDeleteQuerySetMixin(object):
    """Mixin for deleting instances using `delete` method on model instance
    instead of deleting using `QuerySet` method. Made as mixin in order to
    combine with other mixins
    """

    def delete(self, *args, **kwargs):
        for i in self:
            i.delete()
