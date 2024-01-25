import csv
from abc import ABC, abstractmethod
from typing import Dict, List

from app.models.timetable import Timetable


class InvoiceGenerator(ABC):
    @staticmethod
    def calculate_cost(timetable: List[Timetable]) -> Dict:
        company_data = {}
        for row in timetable:
            hours_worked = row.end_time.hour - row.start_time.hour
            cost = hours_worked * row.billable_rate

            if row.project not in company_data:
                company_data[row.project] = {
                    "total_hours": 0,
                    "total_cost": 0,
                    "employees": {},
                }

            if row.employee_id not in company_data[row.project]["employees"]:
                company_data[row.project]["employees"][row.employee_id] = {
                    "hours": 0,
                    "cost": 0,
                }

            company_data[row.project]["employees"][row.employee_id][
                "hours"
            ] += hours_worked
            company_data[row.project]["employees"][row.employee_id]["cost"] += cost
            company_data[row.project]["total_hours"] += hours_worked
            company_data[row.project]["total_cost"] += cost

        return company_data

    @staticmethod
    @abstractmethod
    def parse_content(content: str) -> List[Dict]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def model_validate(row: Dict) -> Timetable:
        raise NotImplementedError


class CsvInvoiceGenerator(InvoiceGenerator):
    @staticmethod
    def parse_content(content: str) -> List[Dict]:
        reader = csv.DictReader(content.splitlines())
        return list(reader)

    @staticmethod
    def model_validate(row: Dict) -> Timetable:
        return Timetable.model_validate(row)


def get_invoice_generator() -> type[InvoiceGenerator]:
        return CsvInvoiceGenerator
