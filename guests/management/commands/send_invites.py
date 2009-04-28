from django.core.management.base import BaseCommand
from wedding.guests.models import Group, Guest
from django.core.mail import SMTPConnection, EmailMultiAlternatives
from django.template.loader import render_to_string

class Command(BaseCommand):
  def handle(self, *args, **options):
    groups = Group.objects.filter(invite_sent=False)
    self.counts = {
      'total': groups.count(),
      'sent': 0,
      'failed': 0,
      'skipped': 0
    }

    print "Attempting to send %d invitations" % self.counts['total']
    
    conn = SMTPConnection()
    
    for group in groups:
      if group.email:
        html_body = render_to_string('guests/invites/invite.html', {
          'group': group 
        })
        text_body = render_to_string('guests/invites/invite.txt', {
          'group': group
        })
        
        email = EmailMultiAlternatives(
          "Come to our wedding!",
          text_body,
          "Jon & Laura <wedding@blankpad.net>",
          [group.email]
        )
        email.attach_alternative(html_body, 'text/html')
        try:
          email.send()
          group.invite_sent = True
          group.save()
          self.log_message(group, True)
        except Exception, e:
          self.log_message(group, False)
          print e
          
      else:
        print "No e-mail address. Skipping."
        self.counts['skipped'] += 1

    print "Sent: %d\nFailed: %d\nSkipped: %d" % ( self.counts['sent'], 
                                                  self.counts['failed'], 
                                                  self.counts['skipped'] )
  
  def log_message(self, group, success = True):
    if (success):
      key = 'sent'
    else:
      key = 'failed'

    self.counts[key] += 1
    print "%s <%s> %s" % (group.name, group.email, key)
