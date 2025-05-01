from typing import Dict, Any
from fhir.resources.R4B.organization import Organization

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class OrganizationExtractor(BaseResourceExtractor[Organization]):
    def extract(self, organization: Organization) -> Dict[str, Any]:
        """
        Extract comprehensive organization data

        Args:
            organization (Organization): FHIR Organization resource

        Returns:
            Dict[str, Any]: Extracted organization data
        """
        return {
            "id": organization.id,
            "name": safe_get(lambda: organization.name),
            "active": safe_get(lambda: organization.active),
            "type_code": safe_get(
                lambda: organization.type[0].coding[0].code
                if organization.type
                else None
            ),
            "type_display": safe_get(
                lambda: organization.type[0].coding[0].display
                if organization.type
                else None
            ),
            "address_line": safe_get(
                lambda: organization.address[0].line[0]
                if organization.address
                else None
            ),
            "address_city": safe_get(
                lambda: organization.address[0].city if organization.address else None
            ),
            "address_state": safe_get(
                lambda: organization.address[0].state if organization.address else None
            ),
            "address_postal_code": safe_get(
                lambda: organization.address[0].postalCode
                if organization.address
                else None
            ),
            "contact_names": safe_get(
                lambda: [
                    contact.name.text
                    for contact in organization.contact
                    if contact.name
                ]
                if organization.contact
                else None
            ),
        }
