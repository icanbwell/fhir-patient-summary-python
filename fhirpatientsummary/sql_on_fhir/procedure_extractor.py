from typing import Dict, Any
from fhir.resources.R4B.procedure import Procedure

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class ProcedureExtractor(BaseResourceExtractor[Procedure]):
    def extract(self, procedure: Procedure) -> Dict[str, Any]:
        """
        Extract comprehensive procedure data

        Args:
            procedure (Procedure): FHIR Procedure resource

        Returns:
            Dict[str, Any]: Extracted procedure data
        """
        return {
            "id": procedure.id,
            "patient_id": safe_get(lambda: procedure.subject.reference.split("/")[-1]),
            "status": safe_get(lambda: procedure.status),
            "category": safe_get(lambda: procedure.category.coding[0].code),
            "code": safe_get(lambda: procedure.code.coding[0].code),
            "code_display": safe_get(lambda: procedure.code.coding[0].display),
            "performed_datetime": safe_get(lambda: str(procedure.performedDateTime)),
            "performed_period_start": safe_get(
                lambda: str(procedure.performedPeriod.start)
                if procedure.performedPeriod
                else None
            ),
            "performed_period_end": safe_get(
                lambda: str(procedure.performedPeriod.end)
                if procedure.performedPeriod
                else None
            ),
            "reason_code": safe_get(
                lambda: procedure.reasonCode[0].coding[0].code
                if procedure.reasonCode
                else None
            ),
        }
