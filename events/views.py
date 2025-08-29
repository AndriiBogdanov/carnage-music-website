from django.shortcuts import render

# Create your views here.

def events_view(request):
    """Страница событий"""
    return render(request, 'events.html')
