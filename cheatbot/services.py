"""
This module contains the ServiceManager class, which is responsible for
caching and filtering the services.
"""
from .models import Service


class ServiceManager:
    """
    Manages the services, including caching and filtering.
    """

    def __init__(self, services: list[Service]):
        """
        Initializes the ServiceManager.

        Args:
            services: A list of Service objects.
        """
        self._services = services
        self._services_by_id = {service.service: service for service in services}
        self._categories = sorted(list(set(s.category.name for s in services)))
        self._service_types_by_category = {
            category: sorted(
                list(
                    set(
                        s.type.name
                        for s in services
                        if s.category.name.lower() == category.lower()
                    )
                )
            )
            for category in self._categories
        }

    def get_all(self) -> list[Service]:
        """
        Returns all the services.

        Returns:
            A list of Service objects.
        """
        return self._services

    def get_by_id(self, service_id: int) -> Service | None:
        """
        Finds a service by its unique ID.

        Args:
            service_id: The integer ID of the service.

        Returns:
            A Service object if found, otherwise None.
        """
        return self._services_by_id.get(service_id)

    def find(
        self,
        category: str | None = None,
        service_type: str | None = None,
        keyword: str | None = None,
    ) -> list[Service]:
        """
        Finds services based on optional filters.

        Args:
            category: The category name to filter by (e.g., "Telegram").
            service_type: The service type name to filter by (e.g., "Подписчики").
            keyword: A keyword to search for in the service name, category, or type.

        Returns:
            A list of Service objects that match the criteria.
        """
        services = self._services

        if category:
            services = [
                s for s in services if s.category.name.lower() == category.lower()
            ]

        if service_type:
            services = [
                s for s in services if s.type.name.lower() == service_type.lower()
            ]

        if keyword:
            keyword = keyword.lower()
            services = [
                s
                for s in services
                if keyword in s.name.lower()
                or keyword in s.category.name.lower()
                or keyword in s.type.name.lower()
            ]

        return services

    def get_categories(self) -> list[str]:
        """
        Gets a sorted list of unique service category names.

        Returns:
            A list of strings, where each string is a unique category name.
        """
        return self._categories

    def get_service_types(self, category: str) -> list[str]:
        """
        Gets a sorted list of unique service type names for a specific category.

        Args:
            category: The name of the category to get types for.

        Returns:
            A list of strings, where each string is a unique service type name.
        """
        return self._service_types_by_category.get(category, [])
