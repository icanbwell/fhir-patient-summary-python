from typing import Dict, Any
from fhir.resources.R4B.medication import Medication

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class MedicationExtractor(BaseResourceExtractor[Medication]):
    def extract(self, medication: Medication) -> Dict[str, Any]:
        """
        Extract comprehensive medication data

        Args:
            medication (Medication): FHIR Medication resource

        Returns:
            Dict[str, Any]: Extracted medication data
        """
        return {
            "id": medication.id,
            "code": safe_get(lambda: medication.code.coding[0].code),
            "code_display": safe_get(lambda: medication.code.coding[0].display),
            "status": safe_get(lambda: medication.status),
            "manufacturer": safe_get(
                lambda: medication.manufacturer.display
                if medication.manufacturer
                else None
            ),
            "form": safe_get(
                lambda: medication.form.coding[0].code if medication.form else None
            ),
            "ingredient_codes": safe_get(
                lambda: [
                    ingredient.itemCodeableConcept.coding[0].code
                    for ingredient in medication.ingredient
                    if ingredient.itemCodeableConcept
                    and ingredient.itemCodeableConcept.coding
                ]
                if medication.ingredient
                else None
            ),
        }
