from typing import Dict, Any
from fhir.resources.R4B.diagnosticreport import DiagnosticReport

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class DiagnosticReportExtractor(BaseResourceExtractor[DiagnosticReport]):
    def extract(self, report: DiagnosticReport) -> Dict[str, Any]:
        """
        Extract comprehensive diagnostic report data

        Args:
            report (DiagnosticReport): FHIR DiagnosticReport resource

        Returns:
            Dict[str, Any]: Extracted diagnostic report data
        """
        return {
            "id": report.id,
            "patient_id": safe_get(lambda: report.subject.reference.split("/")[-1]),
            "status": safe_get(lambda: report.status),
            "category": safe_get(lambda: report.category[0].coding[0].code),
            "code": safe_get(lambda: report.code.coding[0].code),
            "code_display": safe_get(lambda: report.code.coding[0].display),
            "effective_datetime": safe_get(lambda: str(report.effectiveDateTime)),
            "issued": safe_get(lambda: str(report.issued)),
            "conclusion": safe_get(lambda: report.conclusion),
            "performer_ids": safe_get(
                lambda: [
                    performer.reference.split("/")[-1] for performer in report.performer
                ]
                if report.performer
                else None
            ),
        }
