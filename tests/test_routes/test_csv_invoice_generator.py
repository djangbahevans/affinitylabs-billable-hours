import datetime

import pytest
from pydantic import ValidationError

from app.models import Timetable
from app.routes.invoice.invoice_generator import CsvInvoiceGenerator


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

        result = CsvInvoiceGenerator.calculate_cost(timetable)

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
    def test_parse_csv_content():
        csv_content = "project,employee_id,start_time,end_time,billable_rate\nProjectA,1,8,12,10\nProjectB,2,9,11,15"

        result = CsvInvoiceGenerator.parse_content(csv_content)

        assert len(result) == 2
        assert result[0]["project"] == "ProjectA"
        assert result[1]["project"] == "ProjectB"

    @staticmethod
    def test_model_validate():
        row = {
            "Employee ID": 1,
            "Billable Rate": 10,
            "Project": "ProjectA",
            "Date": "2020-01-01",
            "Start Time": "08:00",
            "End Time": "12:00",
        }

        result = CsvInvoiceGenerator.model_validate(row)

        assert isinstance(result, Timetable)
        assert result.employee_id == 1
        assert result.project == "ProjectA"
        assert result.start_time == datetime.time(8, 0)
        assert result.end_time == datetime.time(12, 0)
        assert result.billable_rate == 10

    @staticmethod
    def test_model_validate_invalid():
        row = {
            "Employee ID": 1,
            "Billable Rate": 10,
            "Project": "ProjectA",
            "Date": "2020-01-01",
            "Start Time": "08:00",
            "End Time": "07:00",
        }

        with pytest.raises(ValidationError):
            CsvInvoiceGenerator.model_validate(row)
