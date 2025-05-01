from typing import Dict, Any
from fhir.resources.R4B.allergyintolerance import AllergyIntolerance

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class AllergyIntoleranceExtractor(BaseResourceExtractor[AllergyIntolerance]):
    def extract(self, allergy: AllergyIntolerance) -> Dict[str, Any]:
        """
        Extract comprehensive allergy intolerance data

        Args:
            allergy (AllergyIntolerance): FHIR AllergyIntolerance resource

        Returns:
            Dict[str, Any]: Extracted allergy intolerance data
        """
        return {
            "id": allergy.id,
            "patient_id": safe_get(lambda: allergy.patient.reference.split("/")[-1]),
            "clinical_status": safe_get(lambda: allergy.clinicalStatus.coding[0].code),
            "verification_status": safe_get(
                lambda: allergy.verificationStatus.coding[0].code
            ),
            "type": safe_get(lambda: allergy.type),
            "category": safe_get(
                lambda: allergy.category[0] if allergy.category else None
            ),
            "criticality": safe_get(lambda: allergy.criticality),
            "code": safe_get(lambda: allergy.code.coding[0].code),
            "code_display": safe_get(lambda: allergy.code.coding[0].display),
            "onset_datetime": safe_get(lambda: str(allergy.onsetDateTime)),
        }
