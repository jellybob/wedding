from django.shortcuts import render_to_response

def index(self):
  return render_to_response('home/index.html')  