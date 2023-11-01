from django.shortcuts import render, redirect
from gtfs.models import Agency, Route

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


def create_route(request):
    if request.method == "POST":
        agency = Agency.objects.get(agency_id=request.POST["route_agency"])
        route = Route(
            route_id=request.POST["route_id"],
            agency=agency,
            short_name=request.POST["route_short_name"],
            long_name=request.POST["route_long_name"],
            desc=request.POST["route_desc"],
            route_type=request.POST["route_type"],
            url=request.POST["route_url"],
            color=request.POST["route_color"][1:7],
            text_color=request.POST["route_text_color"][1:7],
        )
        route.save()
        return redirect("edited")
    else:
        agencies = Agency.objects.all()
        route_type_choices = Route.ROUTE_TYPE_CHOICES
        context = {
            "agencies": agencies,
            "route_type_choices": route_type_choices,
        }
        return render(request, "routes.html", context)


def edit_route(request, route_id):
    route = Route.objects.get(route_id=route_id)
    pass


def edited(request):
    return render(request, "edited.html")
