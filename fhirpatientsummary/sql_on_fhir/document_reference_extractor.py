from typing import Dict, Any
from fhir.resources.R4B.documentreference import DocumentReference

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class DocumentReferenceExtractor(BaseResourceExtractor[DocumentReference]):
    def extract(self, doc_ref: DocumentReference) -> Dict[str, Any]:
        """
        Extract comprehensive document reference data

        Args:
            doc_ref (DocumentReference): FHIR DocumentReference resource

        Returns:
            Dict[str, Any]: Extracted document reference data
        """
        return {
            "id": doc_ref.id,
            "patient_id": safe_get(lambda: doc_ref.subject.reference.split("/")[-1]),
            "status": safe_get(lambda: doc_ref.status),
            "type": safe_get(lambda: doc_ref.type.coding[0].code),
            "type_display": safe_get(lambda: doc_ref.type.coding[0].display),
            "category": safe_get(lambda: doc_ref.category[0].coding[0].code),
            "date": safe_get(lambda: str(doc_ref.date)),
            "content_attachment_url": safe_get(
                lambda: doc_ref.content[0].attachment.url
                if doc_ref.content and doc_ref.content[0].attachment
                else None
            ),
            "content_attachment_title": safe_get(
                lambda: doc_ref.content[0].attachment.title
                if doc_ref.content and doc_ref.content[0].attachment
                else None
            ),
        }
