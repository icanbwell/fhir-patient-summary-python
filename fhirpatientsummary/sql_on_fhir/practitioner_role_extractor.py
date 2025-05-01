from typing import Dict, Any
from fhir.resources.R4B.practitionerrole import PractitionerRole

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class PractitionerRoleExtractor(BaseResourceExtractor[PractitionerRole]):
    def extract(self, practitioner_role: PractitionerRole) -> Dict[str, Any]:
        """
        Extract comprehensive practitioner role data

        Args:
            practitioner_role (PractitionerRole): FHIR PractitionerRole resource

        Returns:
            Dict[str, Any]: Extracted practitioner role data
        """
        return {
            "id": practitioner_role.id,
            "practitioner_id": safe_get(
                lambda: practitioner_role.practitioner.reference.split("/")[-1]
                if practitioner_role.practitioner
                else None
            ),
            "organization_id": safe_get(
                lambda: practitioner_role.organization.reference.split("/")[-1]
                if practitioner_role.organization
                else None
            ),
            "active": safe_get(lambda: practitioner_role.active),
            "specialty_codes": safe_get(
                lambda: [
                    specialty.coding[0].code
                    for specialty in practitioner_role.specialty
                ]
                if practitioner_role.specialty
                else None
            ),
            "specialty_displays": safe_get(
                lambda: [
                    specialty.coding[0].display
                    for specialty in practitioner_role.specialty
                ]
                if practitioner_role.specialty
                else None
            ),
            "role_codes": safe_get(
                lambda: [role.coding[0].code for role in practitioner_role.code]
                if practitioner_role.code
                else None
            ),
            "role_displays": safe_get(
                lambda: [role.coding[0].display for role in practitioner_role.code]
                if practitioner_role.code
                else None
            ),
        }
