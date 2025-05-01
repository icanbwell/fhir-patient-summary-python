from typing import Dict, Any
from fhir.resources.R4B.provenance import Provenance

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class ProvenanceExtractor(BaseResourceExtractor[Provenance]):
    def extract(self, provenance: Provenance) -> Dict[str, Any]:
        """
        Extract comprehensive provenance data

        Args:
            provenance (Provenance): FHIR Provenance resource

        Returns:
            Dict[str, Any]: Extracted provenance data
        """
        return {
            "id": provenance.id,
            "recorded": safe_get(lambda: str(provenance.recorded)),
            "target_references": safe_get(
                lambda: [target.reference for target in provenance.target]
                if provenance.target
                else None
            ),
            "agent_types": safe_get(
                lambda: [
                    agent.type.coding[0].code
                    for agent in provenance.agent
                    if agent.type and agent.type.coding
                ]
                if provenance.agent
                else None
            ),
            "agent_who_references": safe_get(
                lambda: [agent.who.reference for agent in provenance.agent if agent.who]
                if provenance.agent
                else None
            ),
            "reason_codes": safe_get(
                lambda: [
                    reason.coding[0].code
                    for reason in provenance.reason
                    if reason.coding
                ]
                if provenance.reason
                else None
            ),
        }
