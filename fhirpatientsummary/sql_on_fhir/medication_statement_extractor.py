from typing import Dict, Any
from fhir.resources.R4B.medicationstatement import MedicationStatement

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class MedicationStatementExtractor(BaseResourceExtractor[MedicationStatement]):
    def extract(self, medication_statement: MedicationStatement) -> Dict[str, Any]:
        """
        Extract comprehensive medication statement data

        Args:
            medication_statement (MedicationStatement): FHIR MedicationStatement resource

        Returns:
            Dict[str, Any]: Extracted medication statement data
        """
        return {
            "id": medication_statement.id,
            "patient_id": safe_get(
                lambda: medication_statement.subject.reference.split("/")[-1]
            ),
            "status": safe_get(lambda: medication_statement.status),
            "medication_code": safe_get(
                lambda: medication_statement.medicationCodeableConcept.coding[0].code
                if medication_statement.medicationCodeableConcept
                else None
            ),
            "medication_display": safe_get(
                lambda: medication_statement.medicationCodeableConcept.coding[0].display
                if medication_statement.medicationCodeableConcept
                else None
            ),
            "effective_datetime": safe_get(
                lambda: str(medication_statement.effectiveDateTime)
            ),
            "effective_period_start": safe_get(
                lambda: str(medication_statement.effectivePeriod.start)
                if medication_statement.effectivePeriod
                else None
            ),
            "effective_period_end": safe_get(
                lambda: str(medication_statement.effectivePeriod.end)
                if medication_statement.effectivePeriod
                else None
            ),
            "taken": safe_get(lambda: medication_statement.taken),
            "reason_code": safe_get(
                lambda: medication_statement.reasonCode[0].coding[0].code
                if medication_statement.reasonCode
                else None
            ),
        }
