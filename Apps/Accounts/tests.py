from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from datetime import date
from .models import Customer, Contract


class CustomerModelTests(TestCase):

    def test_create_customer_success(self):
        """Tests that a Customer can be created successfully."""
        customer = Customer.objects.create(
            cccd="001234567890",
            name="Test User",
            email="test@example.com",
            phone_number="0987654321"
        )
        self.assertEqual(customer.cccd, "001234567890")
        self.assertEqual(customer.name, "Test User")

    def test_duplicate_cccd_fails(self):
        """Tests that a duplicate cccd (Primary Key) fails."""
        Customer.objects.create(
            cccd="001111111111",
            name="First User",
            email="first@example.com",
            phone_number="0111111111"
        )
        # Try to create another customer with the same cccd
        with self.assertRaises(IntegrityError):
            Customer.objects.create(
                cccd="001111111111",
                name="Second User",
                email="second@example.com",
                phone_number="0222222222"
            )

    def test_duplicate_phone_number_fails(self):
        """Tests that a duplicate phone_number (unique=True) fails."""
        Customer.objects.create(
            cccd="001222222222",
            name="First User",
            email="first@example.com",
            phone_number="0123456789"
        )
        # Try to create another customer with the same phone number
        with self.assertRaises(IntegrityError):
            Customer.objects.create(
                cccd="001333333333",
                name="Second User",
                email="second@example.com",
                phone_number="0123456789"
            )

    def test_invalid_email_fails_validation(self):
        """Tests that the EmailField validation works."""
        customer = Customer(
            cccd="001444444444",
            name="Bad Email User",
            email="not-an-email",  # Invalid email format
            phone_number="0444444444"
        )
        # .full_clean() runs all model validation checks
        with self.assertRaises(ValidationError):
            customer.full_clean()


class ContractModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up a base customer to be used by all contract tests."""
        cls.customer = Customer.objects.create(
            cccd="001999888777",
            name="Contract Customer",
            email="contract@example.com",
            phone_number="0999888777"
        )

    def test_create_contract_success(self):
        """Tests that a Contract can be created successfully."""
        contract = Contract.objects.create(
            plate_number="30A-12345",
            vehicle_type="motorbike",
            cccd=self.customer,  # Pass the full Customer object
            term="monthly",
            duration=12,
            start_date=date(2025, 1, 1),
            end_date=date(2026, 1, 1)
        )

        self.assertEqual(contract.plate_number, "30A-12345")
        self.assertEqual(contract.term, "monthly")

        # Test the foreign key relationship
        self.assertEqual(contract.cccd, self.customer)

        # Test the raw ID value (as discussed in our previous chats)
        self.assertEqual(contract.cccd_id, "001999888777")

    def test_duplicate_plate_number_fails(self):
        """Tests that a duplicate plate_number (Primary Key) fails."""
        Contract.objects.create(
            plate_number="29B-98765",
            cccd=self.customer,
            term="yearly",
            duration=1,
            start_date=date(2025, 1, 1),
            end_date=date(2026, 1, 1)
        )
        # Try to create another contract with the same plate number
        with self.assertRaises(IntegrityError):
            Contract.objects.create(
                plate_number="29B-98765",
                cccd=self.customer,
                term="monthly",
                duration=12,
                start_date=date(2025, 2, 1),
                end_date=date(2026, 2, 1)
            )

    def test_on_delete_cascade(self):
        """Tests that deleting a Customer also deletes their Contracts."""
        contract = Contract.objects.create(
            plate_number="50C-55555",
            cccd=self.customer,
            term="monthly",
            duration=6,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 7, 1)
        )

        # Confirm the contract exists
        self.assertEqual(Contract.objects.count(), 1)

        # Delete the customer
        self.customer.delete()

        # Check that the associated contract was also deleted
        self.assertEqual(Contract.objects.count(), 0)

    def test_invalid_term_choice_fails(self):
        """Tests that a 'term' value not in 'choices' fails validation."""
        contract = Contract(
            plate_number="18D-11111",
            cccd=self.customer,
            term="weekly",  # 'weekly' is not a valid choice
            duration=52,
            start_date=date(2025, 1, 1),
            end_date=date(2026, 1, 1)
        )

        # .full_clean() runs validation, including checking 'choices'
        with self.assertRaises(ValidationError):
            contract.full_clean()

    def test_vehicle_type_can_be_blank(self):
        """Tests that 'vehicle_type' can be saved as a blank string."""
        contract = Contract.objects.create(
            plate_number="75E-00001",
            vehicle_type="",  # Set to blank
            cccd=self.customer,
            term="yearly",
            duration=1,
            start_date=date(2025, 1, 1),
            end_date=date(2026, 1, 1)
        )
        self.assertEqual(contract.plate_number, "75E-00001")
        self.assertEqual(contract.vehicle_type, "")
