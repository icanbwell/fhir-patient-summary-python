from typing import Dict, Any
from fhir.resources.R4B.servicerequest import ServiceRequest

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class ServiceRequestExtractor(BaseResourceExtractor[ServiceRequest]):
    def extract(self, service_request: ServiceRequest) -> Dict[str, Any]:
        """
        Extract comprehensive service request data

        Args:
            service_request (ServiceRequest): FHIR ServiceRequest resource

        Returns:
            Dict[str, Any]: Extracted service request data
        """
        return {
            "id": service_request.id,
            "patient_id": safe_get(
                lambda: service_request.subject.reference.split("/")[-1]
            ),
            "status": safe_get(lambda: service_request.status),
            "intent": safe_get(lambda: service_request.intent),
            "category": safe_get(
                lambda: service_request.category[0].coding[0].code
                if service_request.category
                else None
            ),
            "code": safe_get(lambda: service_request.code.coding[0].code),
            "code_display": safe_get(lambda: service_request.code.coding[0].display),
            "occurrence_datetime": safe_get(
                lambda: str(service_request.occurrenceDateTime)
            ),
            "occurrence_period_start": safe_get(
                lambda: str(service_request.occurrencePeriod.start)
                if service_request.occurrencePeriod
                else None
            ),
            "occurrence_period_end": safe_get(
                lambda: str(service_request.occurrencePeriod.end)
                if service_request.occurrencePeriod
                else None
            ),
            "performer_ids": safe_get(
                lambda: [
                    performer.reference.split("/")[-1]
                    for performer in service_request.performer
                ]
                if service_request.performer
                else None
            ),
        }
