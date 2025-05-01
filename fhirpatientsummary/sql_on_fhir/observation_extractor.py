from typing import Dict, Any
from fhir.resources.R4B.observation import Observation

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class ObservationExtractor(BaseResourceExtractor[Observation]):
    def extract(self, observation: Observation) -> Dict[str, Any]:
        """
        Extract comprehensive observation data

        Args:
            observation (Observation): FHIR Observation resource

        Returns:
            Dict[str, Any]: Extracted observation data
        """
        return {
            "id": observation.id,
            "patient_id": safe_get(
                lambda: observation.subject.reference.split("/")[-1]
            ),
            "status": safe_get(lambda: observation.status),
            "category": safe_get(lambda: observation.category[0].coding[0].code),
            "code": safe_get(lambda: observation.code.coding[0].code),
            "value_quantity": safe_get(lambda: observation.valueQuantity.value),
            "value_string": safe_get(lambda: observation.valueString),
            "effective_datetime": safe_get(lambda: str(observation.effectiveDateTime)),
        }
