from typing import Dict, Any
from fhir.resources.R4B.medicationrequest import MedicationRequest

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class MedicationRequestExtractor(BaseResourceExtractor[MedicationRequest]):
    def extract(self, medication_request: MedicationRequest) -> Dict[str, Any]:
        """
        Extract comprehensive medication request data

        Args:
            medication_request (MedicationRequest): FHIR MedicationRequest resource

        Returns:
            Dict[str, Any]: Extracted medication request data
        """
        return {
            "id": medication_request.id,
            "patient_id": safe_get(
                lambda: medication_request.subject.reference.split("/")[-1]
            ),
            "status": safe_get(lambda: medication_request.status),
            "intent": safe_get(lambda: medication_request.intent),
            "category": safe_get(
                lambda: medication_request.category[0].coding[0].code
                if medication_request.category
                else None
            ),
            "medication_code": safe_get(
                lambda: medication_request.medicationCodeableConcept.coding[0].code
            ),
            "medication_display": safe_get(
                lambda: medication_request.medicationCodeableConcept.coding[0].display
            ),
            "authored_on": safe_get(lambda: str(medication_request.authoredOn)),
            "dosage_instruction": safe_get(
                lambda: medication_request.dosageInstruction[0].text
                if medication_request.dosageInstruction
                else None
            ),
        }
