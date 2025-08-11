"""
IPS Sections Enumeration

Defines all possible International Patient Summary section types.
"""


class IPSSections:
    """Enum for all possible IPS sections."""

    # Mandatory Sections
    PATIENT: str = "Patient"
    ALLERGIES = "AllergyIntoleranceSection"
    MEDICATIONS = "MedicationSection"
    PROBLEMS = "ProblemSection"
    IMMUNIZATIONS = "ImmunizationSection"

    # Optional Sections
    VITAL_SIGNS = "VitalSignsSection"
    MEDICAL_DEVICES = "MedicalDeviceSection"

    # Additional Recommended Sections
    DIAGNOSTIC_REPORTS = "DiagnosticReportSection"
    PROCEDURES = "ProcedureSection"
    FAMILY_HISTORY = "FamilyHistorySection"
    SOCIAL_HISTORY = "SocialHistorySection"
    PREGNANCY_HISTORY = "PregnancyHistorySection"
    FUNCTIONAL_STATUS = "FunctionalStatusSection"
    MEDICAL_HISTORY = "MedicalHistorySection"
    CARE_PLAN = "CarePlanSection"
    CLINICAL_IMPRESSION = "ClinicalImpressionSection"
    ADVANCE_DIRECTIVES = "AdvanceDirectivesSection"
