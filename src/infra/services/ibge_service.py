"""
IBGE API service for fetching Brazilian states and cities data.
"""

import asyncio
from typing import Any, Dict, List, Tuple
from uuid import uuid4

import httpx

from application.common.exception import ApplicationException
from infra.models.mongo.city_document import CityDocument
from infra.models.mongo.state_document import StateDocument


class IBGEService:
    """Service to interact with IBGE API for Brazilian geographic data."""

    BASE_URL = "https://servicodados.ibge.gov.br/api/v1/localidades"

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        # Map IBGE state codes to StateDocument instances for city creation
        self.state_map: Dict[int, StateDocument] = {}

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def fetch_states(self) -> List[Dict[str, Any]]:
        """
        Fetch all Brazilian states from IBGE API.

        Returns:
            List of state data dictionaries
        """
        try:
            response = await self.client.get(f"{self.BASE_URL}/estados")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise ApplicationException(f"Error fetching states from IBGE API: {e}")
            return []

    async def fetch_cities_by_state(self, state_id: int) -> List[Dict[str, Any]]:
        """
        Fetch all cities for a given state from IBGE API.

        Args:
            state_id: The IBGE state ID

        Returns:
            List of city data dictionaries
        """
        try:
            response = await self.client.get(f"{self.BASE_URL}/estados/{state_id}/municipios")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise ApplicationException(f"Error fetching cities for state {state_id} from IBGE API: {e}")
            return []

    async def create_state_documents(self) -> List[StateDocument]:
        """
        Create StateDocument objects from IBGE states data.

        Returns:
            List of StateDocument instances
        """
        states_data = await self.fetch_states()
        state_documents = []

        for state_data in states_data:
            state_document = StateDocument(id=uuid4(), name=state_data["nome"], abbreviation=state_data["sigla"])
            state_documents.append(state_document)
            # Store mapping for city creation
            self.state_map[state_data["id"]] = state_document

        return state_documents

    async def create_city_documents(self) -> List[CityDocument]:
        """
        Create CityDocument objects from IBGE cities data for all states.

        Returns:
            List of CityDocument instances
        """
        city_documents = []

        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(5)  # Limit to 5 concurrent requests

        async def fetch_cities_for_state(ibge_state_id: int, state_doc: StateDocument):
            async with semaphore:
                cities_data = await self.fetch_cities_by_state(ibge_state_id)
                state_cities = []

                for city_data in cities_data:
                    city_document = CityDocument(
                        id=uuid4(),
                        name=city_data["nome"],
                        state=state_doc,  # type: ignore
                    )
                    state_cities.append(city_document)

                return state_cities

        # Fetch cities for all states concurrently
        tasks = [
            fetch_cities_for_state(ibge_state_id, state_doc) for ibge_state_id, state_doc in self.state_map.items()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Flatten results and filter out exceptions
        for result in results:
            if isinstance(result, list):
                city_documents.extend(result)
            else:
                raise ApplicationException(f"Error fetching cities: {result}")

        return city_documents

    async def seed_brazilian_data(
        self,
    ) -> Tuple[List[StateDocument], List[CityDocument]]:
        """
        Fetch and create all Brazilian states and cities data.

        Returns:
            Tuple of (state_documents, city_documents)
        """
        state_documents = await self.create_state_documents()

        city_documents = await self.create_city_documents()

        return state_documents, city_documents
