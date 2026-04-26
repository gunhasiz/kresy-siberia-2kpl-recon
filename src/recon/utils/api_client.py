import httpx
from typing import Dict, Any, Optional

from recon.core.config import config
from recon.models.record import Record
from recon.models.status import Status

class ReconAPIClient:
    def __init__(self) -> None:
        self.base_url: Optional[str] = config.API_URL
        self.client = httpx.AsyncClient(
            headers={
                "Content-Type": "application/json"
                }
        )

    async def send_status(self, status: Status) -> Dict[str, Any] | None:
        endpoint: str = f"{self.base_url}/status/"

        payload: Dict[str, str | None] = {
            "entry_id": status.entry_id,
            "url": status.url,
            "status": status.status
        }

        try:
            response: httpx.Response = await self.client.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"[!] HTTP error sending status for entry {status.entry_id}: {e}\n API response: {e.response.text}")
            return None
        except httpx.RequestError as e:
            print(f"[!] Network error sending status for entry {status.entry_id}: {e}")
            return None
        except Exception as e:
            print(f"[!] An unexpected error occurred: {e}")
            return None

    async def send_record(self, record: Record) -> Dict[str, Any] | None:
        endpoint: str = f"{self.base_url}/records/"
        
        payload: Dict[str, Any] = record.model_dump(mode="json")
        
        try:
            response: httpx.Response = await self.client.post(endpoint, json=payload)
            response.raise_for_status()
            
            result: Dict[str, Any] = response.json()
            print(f"[+] Record saved: {record.person.full_name} (ID in database: {result.get('person_id')})")
            return result

        except httpx.HTTPStatusError as e:
            print(f"[!] HTTP error sending record for entry {record.person.external_entry_id}: {e}\n API response: {e.response.text}")
            return None
        except httpx.RequestError as e:
            print(f"[!] Network error sending record for entry {record.person.external_entry_id}: {e}")
            return None
        except Exception as e:
            print(f"[!] An unexpected error occurred: {e}")
            return None