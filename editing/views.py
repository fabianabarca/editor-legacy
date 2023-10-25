from django.shortcuts import render, redirect
from gtfs.models import Agency

# Create your views here.


def edition(request):
    return render(request, "edition.html")


def agency(request):
    if request.method == "POST":
        agency = Agency(
            agency_id=request.POST["agency_id"],
            name=request.POST["agency_name"],
            url=request.POST["agency_url"],
            timezone=request.POST["agency_timezone"],
            lang=request.POST["agency_lang"],
            phone=request.POST["agency_phone"],
            fare_url=request.POST["agency_fare_url"],
            email=request.POST["agency_email"],
        )
        agency.save()
        return redirect("edited")
    else:
        return render(request, "agency.html")


def routes(request):
    return render(request, "routes.html")


def edited(request):
    return render(request, "edited.html")
