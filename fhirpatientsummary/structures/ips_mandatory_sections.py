"""
IPS Mandatory Sections.

This module corresponds to the original ips_mandatory_sections.ts
"""

from .ips_sections import IPSSections


class IPSMandatorySections:
    """IPS mandatory sections constants."""

    PATIENT: str = IPSSections.PATIENT
    ALLERGIES: str = IPSSections.ALLERGIES
    MEDICATIONS: str = IPSSections.MEDICATIONS
    PROBLEMS: str = IPSSections.PROBLEMS
    IMMUNIZATIONS: str = IPSSections.IMMUNIZATIONS
