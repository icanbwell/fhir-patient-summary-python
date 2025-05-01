from datetime import datetime, timedelta
from typing import List, Any, Dict, cast, Callable

from fhir.resources.R4B.allergyintolerance import (
    AllergyIntolerance,
    AllergyIntoleranceReaction,
)
from fhir.resources.R4B.careplan import CarePlan
from fhir.resources.R4B.codeableconcept import CodeableConcept
from fhir.resources.R4B.coding import Coding

# Import all potential IPS resources
from fhir.resources.R4B.condition import Condition
from fhir.resources.R4B.deviceusestatement import DeviceUseStatement
from fhir.resources.R4B.diagnosticreport import DiagnosticReport
from fhir.resources.R4B.documentreference import DocumentReference
from fhir.resources.R4B.familymemberhistory import FamilyMemberHistory
from fhir.resources.R4B.immunization import Immunization
from fhir.resources.R4B.medicationstatement import MedicationStatement
from fhir.resources.R4B.observation import Observation
from fhir.resources.R4B.period import Period
from fhir.resources.R4B.procedure import Procedure


class IPSResourceFilter:
    @staticmethod
    def filter_conditions(conditions: List[Condition]) -> List[Condition]:
        """
        Filter conditions for IPS

        Inclusion Criteria:
        1. Active or recurring conditions
        2. Clinically significant
        3. Exclude certain low-impact conditions
        """
        return [
            condition
            for condition in conditions
            if (
                # Active clinical status
                condition.clinicalStatus
                and cast(CodeableConcept, condition.clinicalStatus).coding
                and any(
                    cast(Coding, status).code in ["active", "recurrence", "relapse"]
                    for status in cast(CodeableConcept, condition.clinicalStatus).coding
                )
                # Exclude certain conditions
                and not _is_excluded_condition(condition)
            )
        ]

    @staticmethod
    def filter_medications(
        medications: List[MedicationStatement],
    ) -> List[MedicationStatement]:
        """
        Filter medications for IPS

        Inclusion Criteria:
        1. Currently active medications
        2. Ongoing or recent treatments
        """
        return [
            medication
            for medication in medications
            if (
                # Active status
                medication.status == "active"
                # Currently being taken or taken recently
                and (
                    not medication.effectivePeriod
                    or (
                        cast(Period, medication.effectivePeriod).start
                        and (
                            not cast(Period, medication.effectivePeriod).end
                            or cast(Period, medication.effectivePeriod).end
                            > (datetime.now() - timedelta(days=180))
                        )
                    )
                )
                # Exclude certain medication types
                and not _is_excluded_medication(medication)
            )
        ]

    @staticmethod
    def filter_allergies(
        allergies: List[AllergyIntolerance],
    ) -> List[AllergyIntolerance]:
        """
        Filter allergies for IPS

        Inclusion Criteria:
        1. Active allergies
        2. Clinically confirmed
        3. Significant reactions
        """
        return [
            allergy
            for allergy in allergies
            if (
                # Active clinical status
                allergy.clinicalStatus
                and cast(CodeableConcept, allergy.clinicalStatus).coding
                and any(
                    cast(Coding, status).code == "active"
                    for status in cast(CodeableConcept, allergy.clinicalStatus).coding
                )
                # Confirmed verification status
                and (
                    not allergy.verificationStatus
                    or any(
                        cast(Coding, status).code in ["confirmed", "validated"]
                        for status in cast(
                            CodeableConcept, allergy.verificationStatus
                        ).coding
                    )
                )
                # Exclude minor or irrelevant allergies
                and _is_significant_allergy(allergy)
            )
        ]

    @staticmethod
    def filter_immunizations(immunizations: List[Immunization]) -> List[Immunization]:
        """
        Filter immunizations for IPS

        Inclusion Criteria:
        1. Completed immunizations
        2. Clinically relevant vaccines
        3. Within reasonable time frame
        """
        return [
            immunization
            for immunization in immunizations
            if (
                # Completed status
                immunization.status == "completed"
                # Exclude certain vaccine types
                and not _is_excluded_immunization(immunization)
                # Within last 10 years for most vaccines
                and (
                    not immunization.occurrenceDateTime
                    or immunization.occurrenceDateTime
                    > (datetime.now() - timedelta(days=3650))
                )
            )
        ]

    @staticmethod
    def filter_observations(observations: List[Observation]) -> List[Observation]:
        """
        Filter observations for IPS

        Inclusion Criteria:
        1. Clinically significant observations
        2. Recent measurements
        3. Specific observation types
        """
        return [
            observation
            for observation in observations
            if (
                # Observation status
                observation.status in ["final", "amended"]
                # Significant observation categories
                and _is_significant_observation(observation)
                # Recent observations (within 1 year)
                and (
                    not observation.effectiveDateTime
                    or observation.effectiveDateTime
                    > (datetime.now() - timedelta(days=365))
                )
            )
        ]

    @staticmethod
    def filter_procedures(procedures: List[Procedure]) -> List[Procedure]:
        """
        Filter procedures for IPS

        Inclusion Criteria:
        1. Completed or in-progress procedures
        2. Clinically significant
        3. Recent procedures
        """
        return [
            procedure
            for procedure in procedures
            if (
                # Procedure status
                procedure.status in ["completed", "in-progress"]
                # Exclude certain procedure types
                and not _is_excluded_procedure(procedure)
                # Recent procedures (within 5 years)
                and (
                    not procedure.performedDateTime
                    or procedure.performedDateTime
                    > (datetime.now() - timedelta(days=1825))
                )
            )
        ]

    @staticmethod
    def filter_device_use(
        devices: List[DeviceUseStatement],
    ) -> List[DeviceUseStatement]:
        """
        Filter device use statements for IPS

        Inclusion Criteria:
        1. Currently active devices
        2. Clinically significant
        """
        return [
            device
            for device in devices
            if (
                # Device status
                device.status == "active"
                # Significant medical devices
                and _is_significant_device(device)
            )
        ]

    @staticmethod
    def filter_family_history(
        family_histories: List[FamilyMemberHistory],
    ) -> List[FamilyMemberHistory]:
        """
        Filter family member history for IPS

        Inclusion Criteria:
        1. Conditions with genetic significance
        2. Recent or ongoing conditions
        """
        return [
            history
            for history in family_histories
            if (
                # Family history status
                history.status in ["completed", "partial"]
                # Significant genetic conditions
                and _is_significant_family_condition(history)
            )
        ]

    @staticmethod
    def filter_document_references(
        documents: List[DocumentReference],
    ) -> List[DocumentReference]:
        """
        Filter document references for IPS

        Inclusion Criteria:
        1. Clinical summary documents
        2. Recent medical records
        """
        return [
            doc
            for doc in documents
            if (
                # Document status
                doc.status == "current"
                # Clinical summary types
                and _is_significant_document(doc)
                # Recent documents (within 2 years)
                and (not doc.date or doc.date > (datetime.now() - timedelta(days=730)))
            )
        ]

    @staticmethod
    def filter_care_plans(care_plans: List[CarePlan]) -> List[CarePlan]:
        """
        Filter care plans for IPS

        Inclusion Criteria:
        1. Active care plans
        2. Ongoing management plans
        """
        return [
            plan
            for plan in care_plans
            if (
                # Care plan status
                plan.status in ["active", "draft"]
                # Significant care management plans
                and _is_significant_care_plan(plan)
            )
        ]

    @staticmethod
    def filter_diagnostic_reports(
        reports: List[DiagnosticReport],
    ) -> List[DiagnosticReport]:
        """
        Filter diagnostic reports for IPS

        Inclusion Criteria:
        1. Final or amended reports
        2. Clinically significant
        3. Recent reports
        """
        return [
            report
            for report in reports
            if (
                # Report status
                report.status in ["final", "amended"]
                # Significant diagnostic reports
                and _is_significant_diagnostic_report(report)
                # Recent reports (within 2 years)
                and (
                    not report.effectiveDateTime
                    or report.effectiveDateTime > (datetime.now() - timedelta(days=730))
                )
            )
        ]


# Helper functions for detailed filtering
def _is_excluded_condition(condition: Condition) -> bool:
    """Determine if a condition should be excluded from IPS"""
    excluded_codes = [
        "162864005",  # History of condition
        "248536006",  # Finding context
    ]

    if condition.code and cast(CodeableConcept, condition.code).coding:
        return any(
            cast(Coding, coding).code in excluded_codes
            for coding in cast(CodeableConcept, condition.code).coding
        )

    return False


def _is_excluded_medication(medication: MedicationStatement) -> bool:
    """Determine if a medication should be excluded from IPS"""
    # Add logic for excluding specific medications
    return False


def _is_significant_allergy(allergy: AllergyIntolerance) -> bool:
    """Determine if an allergy is clinically significant"""
    # Check for severe reactions or critical allergies
    if allergy.reaction:
        return any(
            cast(AllergyIntoleranceReaction, reaction).severity in ["severe", "extreme"]
            for reaction in allergy.reaction
        )
    return True


def _is_excluded_immunization(immunization: Immunization) -> bool:
    """Determine if an immunization should be excluded from IPS"""
    # Add logic for excluding specific immunizations
    return False


def _is_significant_observation(observation: Observation) -> bool:
    """Determine if an observation is clinically significant"""
    significant_categories = ["vital-signs", "laboratory", "imaging", "clinical"]

    return (
        any(
            cast(Coding, cast(CodeableConcept, category).coding[0]).code
            in significant_categories
            for category in observation.category
        )
        if observation.category
        else False
    )


def _is_excluded_procedure(procedure: Procedure) -> bool:
    """Determine if a procedure should be excluded from IPS"""
    # Add logic for excluding specific procedures
    return False


def _is_significant_device(device: DeviceUseStatement) -> bool:
    """Determine if a device is clinically significant"""
    # Add logic for significant medical devices
    return True


def _is_significant_family_condition(history: FamilyMemberHistory) -> bool:
    """Determine if a family condition is significant"""
    # Check for hereditary or genetic conditions
    return True


def _is_significant_document(document: DocumentReference) -> bool:
    """Determine if a document is clinically significant"""
    significant_types = ["clinical-note", "discharge-summary", "history-and-physical"]

    return (
        any(
            cast(Coding, doc_type).code in significant_types
            for doc_type in cast(CodeableConcept, document.type).coding
        )
        if document.type and cast(CodeableConcept, document.type).coding
        else False
    )


def _is_significant_care_plan(care_plan: CarePlan) -> bool:
    """Determine if a care plan is significant"""
    # Add logic for significant care management plans
    return True


def _is_significant_diagnostic_report(report: DiagnosticReport) -> bool:
    """Determine if a diagnostic report is significant"""
    significant_categories = ["LAB", "RAD", "PAT"]

    return (
        any(
            cast(Coding, cast(CodeableConcept, category).coding[0]).code
            in significant_categories
            for category in report.category
        )
        if report.category
        else False
    )


class IPSResourceAggregator:
    def __init__(self, resources: Dict[str, List[Any]]) -> None:
        """
        Aggregate and filter resources for IPS

        Args:
            resources: Dictionary of FHIR resources
        """
        self.resources = resources
        self.filters = {
            "Condition": IPSResourceFilter.filter_conditions,
            "MedicationStatement": IPSResourceFilter.filter_medications,
            "AllergyIntolerance": IPSResourceFilter.filter_allergies,
            "Immunization": IPSResourceFilter.filter_immunizations,
            "Observation": IPSResourceFilter.filter_observations,
            "Procedure": IPSResourceFilter.filter_procedures,
            "DeviceUseStatement": IPSResourceFilter.filter_device_use,
            "FamilyMemberHistory": IPSResourceFilter.filter_family_history,
            "DocumentReference": IPSResourceFilter.filter_document_references,
            "CarePlan": IPSResourceFilter.filter_care_plans,
            "DiagnosticReport": IPSResourceFilter.filter_diagnostic_reports,
        }

    def get_filtered_ips_resources(self) -> Dict[str, List[Any]]:
        """
        Apply filters to resources for IPS

        Returns:
            Filtered resources ready for IPS
        """
        filtered_resources = {}

        for resource_type, resource_list in self.resources.items():
            # Apply filter if exists
            filter_method: Callable[[List[Any]], List[Any]] = self.filters.get(
                resource_type
            )
            if filter_method:
                filtered_resources[resource_type] = filter_method(resource_list)
            else:
                # Keep unfiltered if no specific filter
                filtered_resources[resource_type] = resource_list

        return filtered_resources
