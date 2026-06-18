from datetime import datetime
import unittest

from hms import EmployeeHealthManagementSystem, REQUIRED_APPOINTMENT_TYPES


class EmployeeHealthManagementSystemTests(unittest.TestCase):
    def setUp(self) -> None:
        self.system = EmployeeHealthManagementSystem()
        self.system.add_clinic("clinic-1", "Clinic One")
        self.system.add_clinic("clinic-2", "Clinic Two")
        self.system.add_employee("emp-1", "Sam")
        self.system.add_hr_staff("hr-1", "Pat")

    def test_supports_multiple_clinics(self) -> None:
        clinic_ids = {clinic.clinic_id for clinic in self.system.list_clinics()}
        self.assertEqual({"clinic-1", "clinic-2"}, clinic_ids)

    def test_employee_can_book_appointment(self) -> None:
        appointment = self.system.book_employee_appointment(
            employee_id="emp-1",
            clinic_id="clinic-1",
            appointment_type="annual check up",
            scheduled_for=datetime(2026, 1, 1, 10, 0),
        )

        self.assertEqual("employee", appointment.booked_by_role)
        self.assertEqual("emp-1", appointment.booked_by_id)
        self.assertEqual("clinic-1", appointment.clinic_id)

    def test_hr_can_book_employee_appointment(self) -> None:
        appointment = self.system.book_hr_appointment(
            hr_staff_id="hr-1",
            employee_id="emp-1",
            clinic_id="clinic-2",
            appointment_type="pr-employment",
            scheduled_for=datetime(2026, 1, 2, 9, 0),
        )

        self.assertEqual("hr", appointment.booked_by_role)
        self.assertEqual("hr-1", appointment.booked_by_id)
        self.assertEqual("emp-1", appointment.employee_id)

    def test_all_required_appointment_types_are_supported(self) -> None:
        for appointment_type in REQUIRED_APPOINTMENT_TYPES:
            with self.subTest(appointment_type=appointment_type):
                appointment = self.system.book_employee_appointment(
                    employee_id="emp-1",
                    clinic_id="clinic-1",
                    appointment_type=appointment_type,
                    scheduled_for=datetime(2026, 1, 3, 8, 0),
                )
                self.assertEqual(appointment_type, appointment.appointment_type)

    def test_rejects_unsupported_appointment_type(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported appointment type"):
            self.system.book_employee_appointment(
                employee_id="emp-1",
                clinic_id="clinic-1",
                appointment_type="dental",
                scheduled_for=datetime(2026, 1, 4, 8, 0),
            )


if __name__ == "__main__":
    unittest.main()
