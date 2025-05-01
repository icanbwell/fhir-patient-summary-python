from fhir.resources.R4B.bundle import Bundle


class PatientSummaryGenerator:
    def __init__(self, patient_data: Bundle) -> None:
        self.patient_data = patient_data
