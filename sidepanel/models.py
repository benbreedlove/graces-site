from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.core.models import Ownable, RichText

class Sidepanel(RichText):
    """
    A sidepanel.
    """
    order = models.IntegerField(default=0)


    def __unicode__(self):
        return str(self.order)
    class Meta:
        verbose_name = _("Sidepanel")
        verbose_name_plural = _("Sidepanels")
        ordering = ('order',)
