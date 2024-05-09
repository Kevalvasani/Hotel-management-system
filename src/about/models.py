from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _

# Create your models here.

class About(BaseModel):
    site_name = models.CharField(_('Site Name'), max_length=255)
    description = models.TextField(_("Description"), null=True)
    image = models.FileField(upload_to="site_image/")
    
    def __str__(self):
        return self.site_name