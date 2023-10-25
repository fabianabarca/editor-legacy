from django.shortcuts import render
from .models import Agency

# Create your views here.

def feeds(request):
    """Renders the feeds page."""
    agencies = Agency.objects.all()
    context = {
        'agencies': agencies,
    }
    return render(request, 'feeds.html', context)


def feed(request, version_gtfs):
    """Renders the feed page."""
    agency = Agency.objects.get(agency_id=version_gtfs)
    context = {
        'agency': agency,
    }
    return render(request, 'feed.html', context)


def edit(request, version_gtfs):
    """Renders the edit page."""
    agency = Agency.objects.get(agency_id=version_gtfs)
    context = {
        'agency': agency,
    }
    if request.method == 'POST':
        print(request.POST)
        agency.name = request.POST['name']
        agency.phone = request.POST['phone']
        agency.save()

    return render(request, 'edit.html', context)