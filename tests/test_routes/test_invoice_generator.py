import datetime
import pytest
from app.models.timetable import Timetable
from app.routes.invoice.invoice_generator import InvoiceGenerator


class TestInvoiceGenerator:
    @staticmethod
    def test_calculate_cost():
        timetable = [
            Timetable(
                employee_id=1,
                project="ProjectA",
                date=datetime.date(2020, 1, 1),
                start_time=datetime.time(8, 0),
                end_time=datetime.time(12, 0),
                billable_rate=10,
            ),
            Timetable(
                employee_id=2,
                project="ProjectA",
                date=datetime.date(2020, 1, 1),
                start_time=datetime.time(9, 0),
                end_time=datetime.time(11, 0),
                billable_rate=15,
            ),
        ]

        result = InvoiceGenerator.calculate_cost(timetable)

        assert result == {
            "ProjectA": {
                "total_hours": 6,
                "total_cost": 70,
                "employees": {
                    1: {"hours": 4, "cost": 40},
                    2: {"hours": 2, "cost": 30},
                },
            }
        }

    @staticmethod
    def test_parse_content():
        with pytest.raises(NotImplementedError):
            InvoiceGenerator.parse_content("")

    @staticmethod
    def test_model_validate():
        with pytest.raises(NotImplementedError):
            InvoiceGenerator.model_validate({})
