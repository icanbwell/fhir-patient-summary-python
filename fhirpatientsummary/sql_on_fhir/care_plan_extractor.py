from typing import Dict, Any
from fhir.resources.R4B.careplan import CarePlan

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class CarePlanExtractor(BaseResourceExtractor[CarePlan]):
    def extract(self, care_plan: CarePlan) -> Dict[str, Any]:
        """
        Extract comprehensive care plan data

        Args:
            care_plan (CarePlan): FHIR CarePlan resource

        Returns:
            Dict[str, Any]: Extracted care plan data
        """
        return {
            "id": care_plan.id,
            "patient_id": safe_get(lambda: care_plan.subject.reference.split("/")[-1]),
            "status": safe_get(lambda: care_plan.status),
            "intent": safe_get(lambda: care_plan.intent),
            "category": safe_get(
                lambda: care_plan.category[0].coding[0].code
                if care_plan.category
                else None
            ),
            "title": safe_get(lambda: care_plan.title),
            "description": safe_get(lambda: care_plan.description),
            "period_start": safe_get(
                lambda: str(care_plan.period.start) if care_plan.period else None
            ),
            "period_end": safe_get(
                lambda: str(care_plan.period.end) if care_plan.period else None
            ),
            "activity_count": safe_get(
                lambda: len(care_plan.activity) if care_plan.activity else 0
            ),
            "first_activity_detail": safe_get(
                lambda: care_plan.activity[0].detail.code.coding[0].code
                if care_plan.activity and care_plan.activity[0].detail
                else None
            ),
        }
