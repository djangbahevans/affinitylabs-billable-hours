from fastapi import status
from fastapi.testclient import TestClient

from app.main import app


class TestInvoiceRoute:
    client = TestClient(app)

    @staticmethod
    def test_generate_invoice_route():
        with open("tests/test_routes/valid.csv", "rb") as file:
            print(file)
            response = TestInvoiceRoute.client.post(
                "/generate-invoice/",
                files={
                    "file": ("valid.csv", file, "text/csv"),
                },
            )

        assert response.status_code == status.HTTP_200_OK
        assert "7200" in response.text
        assert "4500" in response.text
        assert response.template.name == "invoice.html"
        assert response.context["company_data"] == {
            "Google": {
                "total_hours": 32,
                "total_cost": 7200,
                "employees": {
                    1: {"hours": 8, "cost": 2400},
                    3: {"hours": 8, "cost": 1600},
                    5: {"hours": 8, "cost": 800},
                    7: {"hours": 8, "cost": 2400},
                },
            },
            "Facebook": {
                "total_hours": 21,
                "total_cost": 4500,
                "employees": {
                    2: {"hours": 5, "cost": 500},
                    4: {"hours": 8, "cost": 2400},
                    6: {"hours": 8, "cost": 1600},
                },
            },
        }

    @staticmethod
    def test_generate_invoice_route_invalid_csv():
        with open("tests/test_routes/invalid.csv", "rb") as file:
            response = TestInvoiceRoute.client.post(
                "/generate-invoice/",
                files={
                    "file": ("invalid.csv", file, "text/csv"),
                },
            )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
