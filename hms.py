from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List


REQUIRED_APPOINTMENT_TYPES = {
    "pr-employment",
    "annual check up",
    "exit appointment",
    "walk in",
    "emmergencies",
}


@dataclass(frozen=True)
class Clinic:
    clinic_id: str
    name: str


@dataclass(frozen=True)
class Employee:
    employee_id: str
    name: str


@dataclass(frozen=True)
class HrStaff:
    staff_id: str
    name: str


@dataclass(frozen=True)
class Appointment:
    clinic_id: str
    employee_id: str
    appointment_type: str
    scheduled_for: datetime
    booked_by_role: str
    booked_by_id: str


class EmployeeHealthManagementSystem:
    def __init__(self) -> None:
        self._clinics: Dict[str, Clinic] = {}
        self._employees: Dict[str, Employee] = {}
        self._hr_staff: Dict[str, HrStaff] = {}
        self._appointments: List[Appointment] = []

    def add_clinic(self, clinic_id: str, name: str) -> Clinic:
        clinic = Clinic(clinic_id=clinic_id, name=name)
        self._clinics[clinic_id] = clinic
        return clinic

    def add_employee(self, employee_id: str, name: str) -> Employee:
        employee = Employee(employee_id=employee_id, name=name)
        self._employees[employee_id] = employee
        return employee

    def add_hr_staff(self, staff_id: str, name: str) -> HrStaff:
        staff = HrStaff(staff_id=staff_id, name=name)
        self._hr_staff[staff_id] = staff
        return staff

    def list_clinics(self) -> List[Clinic]:
        return list(self._clinics.values())

    def list_appointments(self) -> List[Appointment]:
        return list(self._appointments)

    def book_employee_appointment(
        self,
        employee_id: str,
        clinic_id: str,
        appointment_type: str,
        scheduled_for: datetime,
    ) -> Appointment:
        if employee_id not in self._employees:
            raise ValueError(f"Unknown employee: {employee_id}")
        return self._book_appointment(
            clinic_id=clinic_id,
            employee_id=employee_id,
            appointment_type=appointment_type,
            scheduled_for=scheduled_for,
            booked_by_role="employee",
            booked_by_id=employee_id,
        )

    def book_hr_appointment(
        self,
        hr_staff_id: str,
        employee_id: str,
        clinic_id: str,
        appointment_type: str,
        scheduled_for: datetime,
    ) -> Appointment:
        if hr_staff_id not in self._hr_staff:
            raise ValueError(f"Unknown HR staff: {hr_staff_id}")
        if employee_id not in self._employees:
            raise ValueError(f"Unknown employee: {employee_id}")
        return self._book_appointment(
            clinic_id=clinic_id,
            employee_id=employee_id,
            appointment_type=appointment_type,
            scheduled_for=scheduled_for,
            booked_by_role="hr",
            booked_by_id=hr_staff_id,
        )

    def _book_appointment(
        self,
        clinic_id: str,
        employee_id: str,
        appointment_type: str,
        scheduled_for: datetime,
        booked_by_role: str,
        booked_by_id: str,
    ) -> Appointment:
        if clinic_id not in self._clinics:
            raise ValueError(f"Unknown clinic: {clinic_id}")
        if appointment_type not in REQUIRED_APPOINTMENT_TYPES:
            raise ValueError(
                "Unsupported appointment type. Must be one of: "
                + ", ".join(sorted(REQUIRED_APPOINTMENT_TYPES))
            )

        appointment = Appointment(
            clinic_id=clinic_id,
            employee_id=employee_id,
            appointment_type=appointment_type,
            scheduled_for=scheduled_for,
            booked_by_role=booked_by_role,
            booked_by_id=booked_by_id,
        )
        self._appointments.append(appointment)
        return appointment
