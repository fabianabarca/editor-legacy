from django.shortcuts import render, redirect
from gtfs.models import Agency, Route, Stop, Zone

# Create your views here.


def edition(request):
    return render(request, "edition.html")


def create_agency(request):
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

def create_stop(request):
    if request.method == "POST":
        # Handle the POST request as before
        zone = Zone.objects.get(zone_id=request.POST["stop_zone"])
        stop = Stop(
            stop_id=request.POST["stop_id"],
            name=request.POST["stop_name"],
            desc=request.POST["stop_desc"],
            lat=request.POST["stop_lat"],
            lon=request.POST["stop_lon"],
            loc=request.POST["stop_loc"],
            zone=zone,
            url=request.POST["stop_url"],
            location_type=request.POST["stop_location_type"],
            parent_station=request.POST["stop_parent_station"],
            wheelchair_boarding=request.POST["stop_wheelchair_boarding"],
        )
        stop.save()
        return redirect("edited")
    else:
        return render(request, "stop.html")

def list_agency(request):
    agencies = Agency.objects.all()
    return render(request, 'list_agency.html', {'agencies': agencies})

def list_route(request):
    routes = Route.objects.all()
    return render(request, 'list_route.html', {'routes': routes})

def list_stop(request):
    stops = Stop.objects.all()
    return render(request, 'list_stop.html', {'stops': stops})

def delete_agency(request, agency_id):
    agency = Agency.objects.get(agency_id=agency_id)
    agency.delete()
    return redirect("list_agency")

def delete_route(request, route_id):
    route = Route.objects.get(Route, route_id=route_id)
    route.delete()
    return redirect("list_route")

def edit_agency(request, agency_id):
    agency = Agency.objects.get(agency_id=agency_id)
    if request.method == "POST":
        agency.name = request.POST["agency_name"]
        agency.url = request.POST["agency_url"]
        agency.timezone = request.POST["agency_timezone"]
        agency.lang = request.POST["agency_lang"]
        agency.phone = request.POST["agency_phone"]
        agency.fare_url = request.POST["agency_fare_url"]
        agency.email = request.POST["agency_email"]
        agency.save()
        return redirect("edited")
    else:
        context = {"agency": agency}
        return render(request, "edit_agency.html", context)

def edit_route(request, route_id):
    route = Route.objects.get(route_id=route_id)
    agencies = Agency.objects.all()
    route_type_choices = Route.ROUTE_TYPE_CHOICES  # Mover esto fuera de la condición

    if request.method == "POST":
        # Procesar el formulario POST y guardar los cambios en la ruta
        route.short_name = request.POST["route_short_name"]
        route.long_name = request.POST["route_long_name"]
        route.desc = request.POST["route_desc"]
        route.route_type = request.POST["route_type"]
        route.url = request.POST["route_url"]
        route.color = request.POST["route_color"][1:7]
        route.text_color = request.POST["route_text_color"][1:7]

        # Obtener la agencia seleccionada y asignarla a la ruta
        agency_id = request.POST["route_agency"]
        agency = Agency.objects.get(agency_id=agency_id)
        route.agency = agency

        route.save()
        return redirect("edited")
    else:
        # Renderizar el formulario de edición con la información actual y las agencias disponibles
        context = {"route": route, "agencies": agencies, "route_type_choices": route_type_choices}
        return render(request, "edit_route.html", context)


def edited(request):
    return render(request, "edited.html")
