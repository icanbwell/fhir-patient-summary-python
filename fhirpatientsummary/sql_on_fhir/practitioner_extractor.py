from typing import Dict, Any
from fhir.resources.R4B.practitioner import Practitioner

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class PractitionerExtractor(BaseResourceExtractor[Practitioner]):
    def extract(self, practitioner: Practitioner) -> Dict[str, Any]:
        """
        Extract comprehensive practitioner data

        Args:
            practitioner (Practitioner): FHIR Practitioner resource

        Returns:
            Dict[str, Any]: Extracted practitioner data
        """
        return {
            "id": practitioner.id,
            "name_given": safe_get(
                lambda: practitioner.name[0].given[0] if practitioner.name else None
            ),
            "name_family": safe_get(
                lambda: practitioner.name[0].family if practitioner.name else None
            ),
            "name_prefix": safe_get(
                lambda: practitioner.name[0].prefix[0]
                if practitioner.name and practitioner.name[0].prefix
                else None
            ),
            "gender": safe_get(lambda: practitioner.gender),
            "birthdate": safe_get(lambda: str(practitioner.birthDate)),
            "qualifications": safe_get(
                lambda: [
                    {
                        "code": qual.code.coding[0].code,
                        "display": qual.code.coding[0].display,
                        "issuer": qual.issuer.display if qual.issuer else None,
                    }
                    for qual in practitioner.qualification
                ]
                if practitioner.qualification
                else None
            ),
            "communication_languages": safe_get(
                lambda: [lang.coding[0].code for lang in practitioner.communication]
                if practitioner.communication
                else None
            ),
        }
