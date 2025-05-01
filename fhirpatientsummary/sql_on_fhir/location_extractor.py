from typing import Dict, Any
from fhir.resources.R4B.location import Location

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class LocationExtractor(BaseResourceExtractor[Location]):
    def extract(self, location: Location) -> Dict[str, Any]:
        """
        Extract comprehensive location data

        Args:
            location (Location): FHIR Location resource

        Returns:
            Dict[str, Any]: Extracted location data
        """
        return {
            "id": location.id,
            "name": safe_get(lambda: location.name),
            "status": safe_get(lambda: location.status),
            "operational_status": safe_get(lambda: location.operationalStatus),
            "type_code": safe_get(
                lambda: location.type[0].coding[0].code if location.type else None
            ),
            "type_display": safe_get(
                lambda: location.type[0].coding[0].display if location.type else None
            ),
            "address_line": safe_get(
                lambda: location.address.line[0] if location.address else None
            ),
            "address_city": safe_get(
                lambda: location.address.city if location.address else None
            ),
            "address_state": safe_get(
                lambda: location.address.state if location.address else None
            ),
            "address_postal_code": safe_get(
                lambda: location.address.postalCode if location.address else None
            ),
            "managing_organization_id": safe_get(
                lambda: location.managingOrganization.reference.split("/")[-1]
                if location.managingOrganization
                else None
            ),
        }
