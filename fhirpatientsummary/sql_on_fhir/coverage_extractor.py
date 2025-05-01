from typing import Dict, Any
from fhir.resources.R4B.coverage import Coverage

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class CoverageExtractor(BaseResourceExtractor[Coverage]):
    def extract(self, coverage: Coverage) -> Dict[str, Any]:
        """
        Extract comprehensive coverage data

        Args:
            coverage (Coverage): FHIR Coverage resource

        Returns:
            Dict[str, Any]: Extracted coverage data
        """
        return {
            "id": coverage.id,
            "status": safe_get(lambda: coverage.status),
            "type_code": safe_get(
                lambda: coverage.type.coding[0].code
                if coverage.type and coverage.type.coding
                else None
            ),
            "type_display": safe_get(
                lambda: coverage.type.coding[0].display
                if coverage.type and coverage.type.coding
                else None
            ),
            "subscriber_id": safe_get(
                lambda: coverage.subscriber.reference.split("/")[-1]
                if coverage.subscriber
                else None
            ),
            "beneficiary_id": safe_get(
                lambda: coverage.beneficiary.reference.split("/")[-1]
                if coverage.beneficiary
                else None
            ),
            "dependent": safe_get(lambda: coverage.dependent),
            "relationship_code": safe_get(
                lambda: coverage.relationship.coding[0].code
                if coverage.relationship and coverage.relationship.coding
                else None
            ),
            "period_start": safe_get(
                lambda: str(coverage.period.start) if coverage.period else None
            ),
            "period_end": safe_get(
                lambda: str(coverage.period.end) if coverage.period else None
            ),
        }
