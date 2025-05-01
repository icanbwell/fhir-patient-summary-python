from collections.abc import Callable
from typing import Dict, Any
from abc import ABC, abstractmethod

from fhir.resources.R4B.domainresource import DomainResource


class BaseResourceExtractor[TResource: DomainResource](ABC):
    """
    Abstract base class for all FHIR resource extractors
    """

    @abstractmethod
    def extract(self, resource: TResource) -> Dict[str, Any]:
        """
        Abstract method to extract resource data

        Args:
            resource (Any): FHIR resource to extract

        Returns:
            Dict[str, Any]: Extracted resource data
        """
        pass


def safe_get[T](func: Callable[[], T], default: T | None = None) -> Any:
    """
    Safely execute a lambda or function, returning None or default if an exception occurs

    Args:
        func (Callable): Lambda or function to execute
        default (Any, optional): Default value to return if an exception occurs

    Returns:
        Optional[Any]: Result of the function or default/None
    """
    try:
        return func()
    except (AttributeError, IndexError, TypeError):
        return default
