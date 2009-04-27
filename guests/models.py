from django.db import models

class Guest(models.Model):
    """A wedding guest."""
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60, blank=True)
    attending_ceremony = models.NullBooleanField()
    attending_meal = models.NullBooleanField()
    attending_reception = models.NullBooleanField()
    group = models.ForeignKey('Group')
    
    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

class Group(models.Model):
    """A group of guests, who will be invite in one shot."""
    name = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    category = models.ForeignKey('Category')
    invite_to_meal = models.BooleanField()
    save_the_date_sent = models.BooleanField()
    invite_sent = models.BooleanField()
    rsvp_received = models.BooleanField()
    
    def __unicode__(self):
        return self.name
    
    def name_list(self):
      names = [] 
      for guest in self.guest_set.all():
        names += [guest.first_name]
      
      if (len(names)):
        return ", ".join(names[0:-1]) + " and " + names[-1]
      else:
        return names[0]

    class Meta:
      ordering = ['name']

class Category(models.Model):
    """A category of guests, such as 'Wedding Party', or 'Jon's Friends'."""
    name = models.CharField(max_length=40)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "categories"
