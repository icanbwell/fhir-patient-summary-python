from typing import Dict, Any
from fhir.resources.R4B.encounter import Encounter

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class EncounterExtractor(BaseResourceExtractor[Encounter]):
    def extract(self, encounter: Encounter) -> Dict[str, Any]:
        """
        Extract comprehensive encounter data

        Args:
            encounter (Encounter): FHIR Encounter resource

        Returns:
            Dict[str, Any]: Extracted encounter data
        """
        return {
            "id": encounter.id,
            "patient_id": safe_get(lambda: encounter.subject.reference.split("/")[-1]),
            "status": safe_get(lambda: encounter.status),
            "class_code": safe_get(lambda: encounter.class_.code),
            "type": safe_get(lambda: encounter.type[0].coding[0].code),
            "period_start": safe_get(lambda: str(encounter.period.start)),
            "period_end": safe_get(lambda: str(encounter.period.end)),
            "reason_code": safe_get(
                lambda: encounter.reasonCode[0].coding[0].code
                if encounter.reasonCode
                else None
            ),
        }
