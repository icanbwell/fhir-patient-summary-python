from typing import Dict, Any
from fhir.resources.R4B.careteam import CareTeam

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class CareTeamExtractor(BaseResourceExtractor[CareTeam]):
    def extract(self, care_team: CareTeam) -> Dict[str, Any]:
        """
        Extract comprehensive care team data

        Args:
            care_team (CareTeam): FHIR CareTeam resource

        Returns:
            Dict[str, Any]: Extracted care team data
        """
        return {
            "id": care_team.id,
            "patient_id": safe_get(lambda: care_team.subject.reference.split("/")[-1]),
            "status": safe_get(lambda: care_team.status),
            "category": safe_get(
                lambda: care_team.category[0].coding[0].code
                if care_team.category
                else None
            ),
            "category_display": safe_get(
                lambda: care_team.category[0].coding[0].display
                if care_team.category
                else None
            ),
            "name": safe_get(lambda: care_team.name),
            "participants": safe_get(
                lambda: [
                    {
                        "member_id": participant.member.reference.split("/")[-1]
                        if participant.member
                        else None,
                        "role_code": participant.role.coding[0].code
                        if participant.role and participant.role.coding
                        else None,
                        "role_display": participant.role.coding[0].display
                        if participant.role and participant.role.coding
                        else None,
                    }
                    for participant in care_team.participant
                ]
                if care_team.participant
                else None
            ),
        }
