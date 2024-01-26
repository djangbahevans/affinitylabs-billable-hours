import datetime

from pydantic import (AliasChoices, BaseModel, Field, ValidationInfo,
                      field_validator)


class Timetable(BaseModel):
    employee_id: int = Field(
        ...,
        validation_alias=AliasChoices("Employee ID", "employee_id"),
        serialization_alias="employee_id",
    )
    billable_rate: int = Field(
        ...,
        validation_alias=AliasChoices(
            "Billable Rate (per hour)", "Billable Rate", "billable_rate"
        ),
        serialization_alias="billable_rate",
    )
    project: str = Field(
        ...,
        validation_alias=AliasChoices("Project", "project"),
        serialization_alias="project",
    )
    date: datetime.date = Field(
        ..., validation_alias=AliasChoices("Date", "date"), serialization_alias="date"
    )
    start_time: datetime.time = Field(
        ...,
        validation_alias=AliasChoices("Start Time", "start_time"),
        serialization_alias="start_time",
    )
    end_time: datetime.time = Field(
        ...,
        validation_alias=AliasChoices("End Time", "end_time"),
        serialization_alias="end_time",
    )

    @field_validator("end_time")
    def end_time_must_be_after_start_time(cls, v: datetime.date, info: ValidationInfo):
        if v < info.data["start_time"]:
            raise ValueError("end_time must be after start_time")
        return v

    @field_validator("date")
    def date_must_be_in_past(cls, v: datetime.date, info: ValidationInfo):
        if v > datetime.date.today():
            raise ValueError("date must be in the past")
        return v
