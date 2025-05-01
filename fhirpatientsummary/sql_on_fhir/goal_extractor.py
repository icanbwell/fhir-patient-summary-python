from typing import Dict, Any
from fhir.resources.R4B.goal import Goal

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class GoalExtractor(BaseResourceExtractor[Goal]):
    def extract(self, goal: Goal) -> Dict[str, Any]:
        """
        Extract comprehensive goal data

        Args:
            goal (Goal): FHIR Goal resource

        Returns:
            Dict[str, Any]: Extracted goal data
        """
        return {
            "id": goal.id,
            "patient_id": safe_get(lambda: goal.subject.reference.split("/")[-1]),
            "status": safe_get(lambda: goal.status),
            "description": safe_get(lambda: goal.description.text),
            "category": safe_get(
                lambda: goal.category[0].coding[0].code if goal.category else None
            ),
            "priority": safe_get(lambda: goal.priority),
            "start_date": safe_get(
                lambda: str(goal.start.date) if goal.start else None
            ),
            "target_date": safe_get(
                lambda: str(goal.target[0].dueDate)
                if goal.target and goal.target[0].dueDate
                else None
            ),
            "target_quantity": safe_get(
                lambda: goal.target[0].measure.coding[0].code
                if goal.target and goal.target[0].measure
                else None
            ),
        }
