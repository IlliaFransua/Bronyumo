from typing import Optional

from Bronyumo.settings import db_dsn
from apps.accounts.managers import CompanyManager, MapManager, CompanySessionManager
from apps.utils.decorators import session_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View


@method_decorator(session_required, name='dispatch')
class EntrepreneurPanelView(View):
    """
    This class handles HTTP requests related to the entrepreneur's
    dashboard when the map has not yet been uploaded.
    It uses the GET method to render an HTML template with the provided parameters.

    Main functions:
    - Receiving a GET request from the client.
    - Forming the context with data.
    - Generating an HTML response with the prepared information.

    The `get()` method operates in a static mode. Creating an instance of the class is not required.
    """

    def __init__(self, **kwargs: Optional[dict]) -> None:
        """
        Initializes the view. Sets up the company and session managers for use.

        :param kwargs: Additional keyword arguments passed to the parent class.
        """
        try:
            super().__init__(**kwargs)
            self.company_manager = CompanyManager(db_dsn=db_dsn)
            self.session_manager = CompanySessionManager(db_dsn=db_dsn)
            self.map_manager = MapManager(db_dsn=db_dsn)
        except Exception as e:
            # print(f"Error during initialization: {str(e)}")
            raise

    def get(self, request, status=None):
        """
        Expected parameters:
            request (HttpRequest): The HTTP request received from the client.

        Expected result:
            An HTML page containing the provided context.

        In the current version, a list of items is passed as an example.
        If the page needs to be displayed, it is preferable to use `render()`.
        """
        try:
            session_id: Optional[str] = request.COOKIES.get('session_id')

            company_data: Optional[dict] = self.company_manager.get_company_by_session_id(session_id)
            if not company_data:
                return render(request, "accounts/EntrepreneurPanelView.html", {
                    "error": "Company data not found."
                }, status=status.HTTP_404_NOT_FOUND)

            company_id = company_data.get("id")
            first_map = self.map_manager.get_first_map_hash_by_company_id(company_id)

            if first_map:
                return redirect(f"/edit-available-objects-panel/{first_map}/")

            return render(request, "accounts/EntrepreneurPanelView.html", {
                "company_name": company_data.get("name")
            })

        except ObjectDoesNotExist:
            return render(request, "accounts/EntrepreneurPanelView.html", {
                "error": "Company data not found."
            }, status=status.HTTP_404_NOT_FOUND)

        except KeyError as e:
            return render(request, "accounts/EntrepreneurPanelView.html", {
                "error": f"Missing key: {str(e)}."
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return render(request, "accounts/EntrepreneurPanelView.html", {
                "error": f"An unexpected error occurred: {e}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
