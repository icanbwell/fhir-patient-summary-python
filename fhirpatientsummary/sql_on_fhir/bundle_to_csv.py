import importlib
import pkgutil
import inspect
from typing import Dict, Type

from fhir.resources.R4B.domainresource import DomainResource

from fhirpatientsummary.sql_on_fhir.base_extractor import BaseResourceExtractor


class USCoreExtractorRegistry:
    """
    Enhanced registry for dynamically discovering and registering extractors
    """

    _extractors: Dict[str, Type[BaseResourceExtractor[DomainResource]]] = {}

    @classmethod
    def discover_extractors(cls, package_name: str = "us_core_extractors") -> None:
        """
        Dynamically discover and register all extractors in the package

        Args:
            package_name (str): Package containing extractor modules
        """
        try:
            package = importlib.import_module(package_name)
            for _, module_name, _ in pkgutil.iter_modules(package.__path__):
                full_module_name = f"{package_name}.{module_name}"
                module = importlib.import_module(full_module_name)

                for name, obj in inspect.getmembers(module):
                    if (
                        inspect.isclass(obj)
                        and issubclass(obj, BaseResourceExtractor)
                        and obj is not BaseResourceExtractor
                    ):
                        # Extract resource type from class name
                        resource_type = name.replace("Extractor", "")
                        cls._extractors[resource_type] = obj

        except ImportError as e:
            print(f"Error discovering extractors: {e}")

    @classmethod
    def get_extractor(cls, resource_type: str):
        """
        Get extractor for a specific resource type

        Args:
            resource_type (str): FHIR resource type

        Returns:
            BaseResourceExtractor: Extractor for the resource type

        Raises:
            ValueError: If no extractor found
        """
        # Ensure extractors are discovered
        if not cls._extractors:
            cls.discover_extractors()

        if resource_type not in cls._extractors:
            raise ValueError(f"No extractor found for resource type: {resource_type}")

        return cls._extractors[resource_type]()


# # Call this at module import or application startup
# USCoreExtractorRegistry.discover_extractors()
