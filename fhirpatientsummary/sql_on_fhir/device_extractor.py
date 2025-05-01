from typing import Dict, Any
from fhir.resources.R4B.device import Device

from fhirpatientsummary.sql_on_fhir.base_extractor import (
    BaseResourceExtractor,
    safe_get,
)


class DeviceExtractor(BaseResourceExtractor[Device]):
    def extract(self, device: Device) -> Dict[str, Any]:
        """
        Extract comprehensive device data

        Args:
            device (Device): FHIR Device resource

        Returns:
            Dict[str, Any]: Extracted device data
        """
        return {
            "id": device.id,
            "patient_id": safe_get(
                lambda: device.patient.reference.split("/")[-1]
                if device.patient
                else None
            ),
            "status": safe_get(lambda: device.status),
            "type": safe_get(lambda: device.type.coding[0].code),
            "type_display": safe_get(lambda: device.type.coding[0].display),
            "manufacturer": safe_get(lambda: device.manufacturer),
            "model_number": safe_get(lambda: device.modelNumber),
            "serial_number": safe_get(lambda: device.serialNumber),
            "manufacture_date": safe_get(lambda: str(device.manufactureDate)),
            "expiration_date": safe_get(lambda: str(device.expirationDate)),
        }
