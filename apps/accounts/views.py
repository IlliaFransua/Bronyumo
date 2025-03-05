import json

from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods


def home(request):
    context = {
        'items': ['one', 'two', 'three'],
    }
    return render(request, 'accounts/home.html', context=context)

def enrepreneur_page(request):
    return render(request, "accounts/entrepreneur-floor-panel.html")

@csrf_protect
@require_http_methods(["POST"])
def save_table_layout(request):
    try:
        data = json.loads(request.body)
        table_coordinates = data.get('table_coordinates', [])

        if not isinstance(table_coordinates, list):
            return JsonResponse({"message": "Table coordinates are not a list"}, status=400)

        validated_coordinates = []
        for coord in table_coordinates:
            try:
                validated_coord = {
                    'x1': float(coord['x1']),
                    'y1': float(coord['y1']),
                    'x2': float(coord['x2']),
                    'y2': float(coord['y2'])
                }
                validated_coordinates.append(validated_coord)
            except (KeyError, ValueError):
                continue

        # TODO: Save validated_coordinates to the database

        return JsonResponse({
            "status": "success",
        })

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

