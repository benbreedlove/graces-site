from django.db import models
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField

from mezzanine.conf import settings

class Sidepanel(models.Model):
    """
    A sidepanel.
    """

    content = RichTextField(config_name='sidebar')

    order = models.IntegerField(default=0)


    search_fields = ("content",)

    def __unicode__(self):
        return str(self.order)
    class Meta:
        verbose_name = _("Sidepanel")
        verbose_name_plural = _("Sidepanels")
        ordering = ('order',)
