from django.db import models

class Guest(models.Model):
    """A wedding guest."""
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    invite_to_meal = models.BooleanField()
    save_the_date_sent = models.BooleanField()
    invite_sent = models.BooleanField()
    attending_ceremony = models.NullBooleanField()
    attending_meal = models.NullBooleanField()
    attending_reception = models.NullBooleanField()
    group = models.ForeignKey('GuestGroup')
    
    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

class GuestGroup(models.Model):
    """A group of guests."""
    group_name = models.CharField(max_length=40)
    
    def __unicode__(self):
        return self.group_name