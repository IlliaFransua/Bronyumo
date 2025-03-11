import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from apps.bookings.models import TableLayoutModel


@method_decorator(csrf_protect, name="dispatch")
class EditAvailableObjectsPanelView(View):
    def get(self, request):
        return render(request, "accounts/entrepreneur-floor-panel.html")

    def post(self, request):
        try:
            data = json.loads(request.body)
            table_coordinates = data.get("table_coordinates", [])

            if not isinstance(table_coordinates, list):
                return JsonResponse({"message": "Table coordinates are not a list"}, status=400)

            validated_coordinates = []
            for coord in table_coordinates:
                try:
                    validated_coord = TableLayoutModel.objects.create(
                        x1=float(coord["x1"]),
                        y1=float(coord["y1"]),
                        x2=float(coord["x2"]),
                        y2=float(coord["y2"]),
                    )
                    validated_coordinates.append({
                        "id": validated_coord.id,
                        "x1": validated_coord.x1,
                        "y1": validated_coord.y1,
                        "x2": validated_coord.x2,
                        "y2": validated_coord.y2,
                    })
                except (KeyError, ValueError):
                    continue

            print({"saved_tables": validated_coordinates})
            return JsonResponse({
                "status": "success",
                "saved_tables": validated_coordinates
            })

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
