from typing import Dict, Any
from fhir.resources.R4B.condition import Condition

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class ConditionExtractor(BaseResourceExtractor[Condition]):
    def extract(self, condition: Condition) -> Dict[str, Any]:
        """
        Extract comprehensive condition data

        Args:
            condition (Condition): FHIR Condition resource

        Returns:
            Dict[str, Any]: Extracted condition data
        """
        return {
            "id": condition.id,
            "patient_id": safe_get(lambda: condition.subject.reference.split("/")[-1]),
            "clinical_status": safe_get(
                lambda: condition.clinicalStatus.coding[0].code
            ),
            "verification_status": safe_get(
                lambda: condition.verificationStatus.coding[0].code
            ),
            "category": safe_get(lambda: condition.category[0].coding[0].code),
            "code": safe_get(lambda: condition.code.coding[0].code),
            "code_display": safe_get(lambda: condition.code.coding[0].display),
            "onset_datetime": safe_get(lambda: str(condition.onsetDateTime)),
            "recorded_date": safe_get(lambda: str(condition.recordedDate)),
        }
