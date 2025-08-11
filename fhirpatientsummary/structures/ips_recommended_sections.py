"""
IPS Recommended Sections.

This module corresponds to the original ips_recommended_sections.ts
"""

from .ips_sections import IPSSections


class IPSRecommendedSections:
    """IPS recommended sections constants."""

    MEDICAL_DEVICES: str = "Device"
    PREGNANCY_STATUS: str = "PregnancyStatus"
    FUNCTIONAL_STATUS: str = "FunctionalStatus"
    ADVANCED_DIRECTIVES: str = "Consent"
    DIAGNOSTIC_REPORTS: str = IPSSections.DIAGNOSTIC_REPORTS
    VITAL_SIGNS: str = IPSSections.VITAL_SIGNS
