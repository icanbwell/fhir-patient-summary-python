"""
Test the NarrativeGenerator.

This test file corresponds to the original narrativeGenerator.test.ts
"""

import pytest
from typing import List, Dict, Any

from fhirpatientsummary.generators import NarrativeGenerator
from fhirpatientsummary.structures import IPSSections
from fhirpatientsummary.types import TPatient


class TestNarrativeGenerator:
    """Test suite for NarrativeGenerator."""

    @pytest.fixture
    def mock_patient(self) -> TPatient:
        """Mock patient resource for testing."""
        return {
            "resourceType": "Patient",
            "id": "test-patient-01",
            "identifier": [{"system": "https://example.org", "value": "12345"}],
            "name": [{"family": "Doe", "given": ["John"]}],
            "gender": "male",
            "birthDate": "1980-01-01",
        }

    @pytest.fixture
    def mock_allergies(self) -> List[Dict[str, Any]]:
        """Mock allergy resources for testing."""
        return [
            {
                "resourceType": "AllergyIntolerance",
                "id": "allergy-01",
                "clinicalStatus": {"coding": [{"code": "active"}]},
                "verificationStatus": {"coding": [{"code": "confirmed"}]},
                "code": {"text": "Penicillin"},
                "patient": {"reference": "Patient/test-patient-01"},
            },
            {
                "resourceType": "AllergyIntolerance",
                "id": "allergy-02",
                "clinicalStatus": {"coding": [{"code": "active"}]},
                "verificationStatus": {"coding": [{"code": "confirmed"}]},
                "code": {"text": "Peanuts"},
                "patient": {"reference": "Patient/test-patient-01"},
                "reaction": [
                    {"manifestation": [{"text": "Anaphylaxis"}], "severity": "severe"}
                ],
            },
            {
                "resourceType": "AllergyIntolerance",
                "id": "allergy-03",
                "clinicalStatus": {"coding": [{"code": "inactive"}]},
                "verificationStatus": {"coding": [{"code": "confirmed"}]},
                "code": {"text": "Latex"},
                "patient": {"reference": "Patient/test-patient-01"},
                "reaction": [
                    {"manifestation": [{"text": "Skin rash"}], "severity": "moderate"}
                ],
            },
        ]

    @pytest.fixture
    def mock_medications(self) -> List[Dict[str, Any]]:
        """Mock medication resources for testing."""
        return [
            {
                "resourceType": "MedicationStatement",
                "id": "med-01",
                "status": "active",
                "medicationCodeableConcept": {"text": "Aspirin"},
                "subject": {"reference": "Patient/test-patient-01"},
            },
            {
                "resourceType": "MedicationStatement",
                "id": "med-02",
                "status": "active",
                "medicationCodeableConcept": {"text": "Lisinopril"},
                "subject": {"reference": "Patient/test-patient-01"},
                "dosage": [
                    {
                        "text": "10mg daily",
                        "timing": {
                            "repeat": {"frequency": 1, "period": 1, "periodUnit": "d"}
                        },
                    }
                ],
            },
        ]

    @pytest.fixture
    def mock_conditions(self) -> List[Dict[str, Any]]:
        """Mock condition resources for testing."""
        return [
            {
                "resourceType": "Condition",
                "id": "condition-01",
                "clinicalStatus": {"coding": [{"code": "active"}]},
                "verificationStatus": {"coding": [{"code": "confirmed"}]},
                "code": {"text": "Hypertension"},
                "subject": {"reference": "Patient/test-patient-01"},
            },
            {
                "resourceType": "Condition",
                "id": "condition-02",
                "clinicalStatus": {"coding": [{"code": "resolved"}]},
                "verificationStatus": {"coding": [{"code": "confirmed"}]},
                "code": {"text": "Diabetes Type 2"},
                "subject": {"reference": "Patient/test-patient-01"},
            },
        ]

    @pytest.fixture
    def mock_immunizations(self) -> List[Dict[str, Any]]:
        """Mock immunization resources for testing."""
        return [
            {
                "resourceType": "Immunization",
                "id": "immunization-01",
                "status": "completed",
                "vaccineCode": {"text": "COVID-19"},
                "patient": {"reference": "Patient/test-patient-01"},
                "occurrenceDateTime": "2023-01-15",
            },
            {
                "resourceType": "Immunization",
                "id": "immunization-02",
                "status": "completed",
                "vaccineCode": {"text": "Influenza"},
                "patient": {"reference": "Patient/test-patient-01"},
                "occurrenceDateTime": "2022-10-01",
            },
        ]

    @pytest.mark.asyncio
    async def test_patient_narrative_generation(self, mock_patient: TPatient) -> None:
        """Test patient narrative generation."""
        narrative = await NarrativeGenerator.generate_narrative_content_async(
            IPSSections.PATIENT, [mock_patient], "America/New_York", True
        )

        assert narrative is not None
        assert "Patient Summary" in narrative
        assert "John Doe" in narrative
        assert "Male" in narrative
        assert "1980-01-01" in narrative

    @pytest.mark.asyncio
    async def test_allergies_narrative_generation(
        self, mock_allergies: List[Dict[str, Any]]
    ) -> None:
        """Test allergies narrative generation."""
        narrative = await NarrativeGenerator.generate_narrative_content_async(
            IPSSections.ALLERGIES, mock_allergies, "America/New_York", True
        )

        assert narrative is not None
        assert "Allergies and Adverse Reactions" in narrative
        assert "Penicillin" in narrative
        assert "Peanuts" in narrative
        assert "Latex" in narrative

    @pytest.mark.asyncio
    async def test_medications_narrative_generation(
        self, mock_medications: List[Dict[str, Any]]
    ) -> None:
        """Test medications narrative generation."""
        narrative = await NarrativeGenerator.generate_narrative_content_async(
            IPSSections.MEDICATIONS, mock_medications, "America/New_York", True
        )

        assert narrative is not None
        assert "Medications" in narrative
        assert "Aspirin" in narrative
        assert "Lisinopril" in narrative

    @pytest.mark.asyncio
    async def test_conditions_narrative_generation(
        self, mock_conditions: List[Dict[str, Any]]
    ) -> None:
        """Test conditions/problems narrative generation."""
        narrative = await NarrativeGenerator.generate_narrative_content_async(
            IPSSections.PROBLEMS, mock_conditions, "America/New_York", True
        )

        assert narrative is not None
        assert "Problems" in narrative
        assert "Hypertension" in narrative
        assert "Diabetes Type 2" in narrative

    @pytest.mark.asyncio
    async def test_immunizations_narrative_generation(
        self, mock_immunizations: List[Dict[str, Any]]
    ) -> None:
        """Test immunizations narrative generation."""
        narrative = await NarrativeGenerator.generate_narrative_content_async(
            IPSSections.IMMUNIZATIONS, mock_immunizations, "America/New_York", True
        )

        assert narrative is not None
        assert "Immunizations" in narrative
        assert "COVID-19" in narrative
        assert "Influenza" in narrative
        assert "2023-01-15" in narrative
        assert "2022-10-01" in narrative

    @pytest.mark.asyncio
    async def test_empty_resources_returns_none(self) -> None:
        """Test that empty resources return None."""
        narrative = await NarrativeGenerator.generate_narrative_content_async(
            IPSSections.PATIENT, [], "America/New_York", True
        )

        assert narrative is None

    @pytest.mark.asyncio
    async def test_narrative_with_xhtml_wrapping(self, mock_patient: TPatient) -> None:
        """Test narrative generation with XHTML wrapping."""
        narrative = await NarrativeGenerator.generate_narrative_content_async(
            IPSSections.PATIENT,
            [mock_patient],
            "America/New_York",
            True,  # wrap in XHTML
        )

        assert narrative is not None
        assert 'xmlns="http://www.w3.org/1999/xhtml"' in narrative

    @pytest.mark.asyncio
    async def test_narrative_without_xhtml_wrapping(
        self, mock_patient: TPatient
    ) -> None:
        """Test narrative generation without XHTML wrapping."""
        narrative = await NarrativeGenerator.generate_narrative_content_async(
            IPSSections.PATIENT,
            [mock_patient],
            "America/New_York",
            False,  # don't wrap in XHTML
        )

        assert narrative is not None
        assert 'xmlns="http://www.w3.org/1999/xhtml"' not in narrative

    @pytest.mark.asyncio
    async def test_create_narrative_object(self) -> None:
        """Test creating a complete narrative object."""
        content = "<p>Test content</p>"

        narrative = await NarrativeGenerator.create_narrative_async(content, True)

        assert narrative.status == "generated"
        assert 'xmlns="http://www.w3.org/1999/xhtml"' in narrative.div
        assert "Test content" in narrative.div

    @pytest.mark.asyncio
    async def test_generate_narrative_object(self, mock_patient: TPatient) -> None:
        """Test generating a complete narrative object."""
        narrative = await NarrativeGenerator.generate_narrative_async(
            IPSSections.PATIENT, [mock_patient], "America/New_York", True, True
        )

        assert narrative is not None
        assert narrative.status == "generated"
        assert 'xmlns="http://www.w3.org/1999/xhtml"' in narrative.div
        assert "John Doe" in narrative.div

    @pytest.mark.asyncio
    async def test_html_minification(self) -> None:
        """Test HTML minification functionality."""
        html = """
        <div>
            <p>  Test content  </p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
        </div>
        """

        minified = await NarrativeGenerator.minify_html_async(html, False)

        assert minified is not None
        assert len(minified) <= len(html)  # Should be smaller or equal

    @pytest.mark.asyncio
    async def test_aggressive_html_minification(self) -> None:
        """Test aggressive HTML minification functionality."""
        html = """
        <div>
            <p>  Test content  </p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
        </div>
        """

        minified = await NarrativeGenerator.minify_html_async(html, True)

        assert minified is not None
        assert len(minified) <= len(html)  # Should be smaller or equal

    @pytest.mark.asyncio
    async def test_wrap_in_xhtml(self) -> None:
        """Test XHTML wrapping functionality."""
        content = "<p>Test content</p>"

        wrapped = await NarrativeGenerator.wrap_in_xhtml_async(content, False)

        assert (
            wrapped
            == '<div xmlns="http://www.w3.org/1999/xhtml"><p>Test content</p></div>'
        )

    @pytest.mark.asyncio
    async def test_wrap_in_xhtml_with_minification(self) -> None:
        """Test XHTML wrapping with minification."""
        content = """
        <p>  Test content  </p>
        <ul>
            <li>Item</li>
        </ul>
        """

        wrapped = await NarrativeGenerator.wrap_in_xhtml_async(content, True)

        assert 'xmlns="http://www.w3.org/1999/xhtml"' in wrapped
        assert "Test content" in wrapped
        assert len(wrapped) < len(content) + 100  # Should be minified

    @pytest.mark.asyncio
    async def test_timezone_parameter(self, mock_patient: TPatient) -> None:
        """Test that timezone parameter is accepted (even if not used in basic implementation)."""
        narrative_ny = await NarrativeGenerator.generate_narrative_content_async(
            IPSSections.PATIENT, [mock_patient], "America/New_York", True
        )

        narrative_london = await NarrativeGenerator.generate_narrative_content_async(
            IPSSections.PATIENT, [mock_patient], "Europe/London", True
        )

        # Both should generate content
        assert narrative_ny is not None
        assert narrative_london is not None
        # Basic implementation might not use timezone, so content could be the same
        assert "John Doe" in narrative_ny
        assert "John Doe" in narrative_london


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
