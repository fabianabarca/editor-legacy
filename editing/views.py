from django.shortcuts import render, redirect
from gtfs.models import Agency
from gtfs.models import Route

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
    if request.method == "POST":
        routes = Route(
            route_id=request.POST["route_id"],
            agency=request.POST["route_agency"],
            short_name=request.POST["route_short_name"],
            long_name=request.POST["route_long_name"],
            desc=request.POST["route_desc"],
            route_type=request.POST["route_type"],
            url=request.POST["route_url"],
            color=request.POST["route_color"],
            text_color=request.POST["route_text_color"],
        )
        agency.save()
        return redirect("edited")
    else:
        return render(request, "routes.html")

def edited(request):
    return render(request, "edited.html")
