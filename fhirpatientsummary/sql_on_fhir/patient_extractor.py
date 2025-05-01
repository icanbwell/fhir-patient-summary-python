from typing import Dict, Any
from fhir.resources.R4B.patient import Patient

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class PatientExtractor(BaseResourceExtractor[Patient]):
    def extract(self, patient: Patient) -> Dict[str, Any]:
        """
        Extract comprehensive patient data

        Args:
            patient (Patient): FHIR Patient resource

        Returns:
            Dict[str, Any]: Extracted patient data
        """
        return {
            "id": patient.id,
            "name_given": safe_get(lambda: patient.name[0].given[0]),
            "name_family": safe_get(lambda: patient.name[0].family),
            "birth_date": safe_get(lambda: str(patient.birthDate)),
            "gender": safe_get(lambda: patient.gender),
            "race": safe_get(
                lambda: patient.extension[0].extension[0].valueCoding.display
            ),
            "ethnicity": safe_get(
                lambda: patient.extension[1].extension[0].valueCoding.display
            ),
            "address_line": safe_get(lambda: patient.address[0].line[0]),
            "address_city": safe_get(lambda: patient.address[0].city),
            "address_state": safe_get(lambda: patient.address[0].state),
            "telecom_phone": safe_get(
                lambda: next(
                    contact.value
                    for contact in patient.telecom
                    if contact.system == "phone"
                )
            ),
        }
