from django.shortcuts import render_to_response
from wedding.gifts.models import Gift

def index(request):
    gifts = Gift.objects.all()
    return render_to_response('gifts/index.html', { 'gifts': gifts })