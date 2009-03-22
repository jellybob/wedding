from django.db import models
from django.conf import settings

class Gift(models.Model):
    """A gift that we'd like to be given."""
    def generate_gift_path(instance, filename):
        return "gifts/%s/%s" % (instance.slug, filename)
        
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField(help_text = "In pennies, not pounds. &pound;1.99 should be entered as 199")
    reserved = models.BooleanField()
    address = models.URLField(help_text = "The web address for this gift")
    image = models.FileField(upload_to = generate_gift_path)
    slug = models.SlugField(help_text = "A version of the name used for image storage. Leave it blank to generate one.")
    
    def __unicode__(self):
        return self.name