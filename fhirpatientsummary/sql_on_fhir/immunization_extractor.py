from typing import Dict, Any
from fhir.resources.R4B.immunization import Immunization

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class ImmunizationExtractor(BaseResourceExtractor[Immunization]):
    def extract(self, immunization: Immunization) -> Dict[str, Any]:
        """
        Extract comprehensive immunization data

        Args:
            immunization (Immunization): FHIR Immunization resource

        Returns:
            Dict[str, Any]: Extracted immunization data
        """
        return {
            "id": immunization.id,
            "patient_id": safe_get(
                lambda: immunization.patient.reference.split("/")[-1]
            ),
            "status": safe_get(lambda: immunization.status),
            "vaccine_code": safe_get(lambda: immunization.vaccineCode.coding[0].code),
            "vaccine_display": safe_get(
                lambda: immunization.vaccineCode.coding[0].display
            ),
            "occurrence_datetime": safe_get(
                lambda: str(immunization.occurrenceDateTime)
            ),
            "manufacturer": safe_get(lambda: immunization.manufacturer.display),
            "lot_number": safe_get(lambda: immunization.lotNumber),
        }
