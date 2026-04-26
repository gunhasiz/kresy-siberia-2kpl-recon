import requests
from typing import Dict, Any, Optional

from recon.core.config import config
from recon.models.record import Record
from recon.models.status import Status

class ReconAPIClient:
    def __init__(self):
        self.base_url: Optional[str] = config.API_URL
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def send_status(self, status: Status) -> Dict[str, Any] | None:
        endpoint = f"{self.base_url}/status/"

        payload = {
            "entry_id": status.entry_id,
            "url": status.url,
            "status": status.status
        }

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"[!] Error sending status for entry {status.entry_id}: {e}\n API response: {response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"[!] Error sending status for entry {status.entry_id}: {e}\n API response: {response.text}")
            return None
        except Exception as e:
            print(f"[!] An unexpected error occurred: {e}")
            return None

    def send_record(self, record: Record) -> Dict[str, Any] | None:
        endpoint: str = f"{self.base_url}/records/"
        
        payload: Dict[str, Any] = record.model_dump(mode="json")
        
        try:
            response: requests.Response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            
            result = response.json()
            print(f"[+] Record saved: {record.person.full_name} (ID in database: {result.get('person_id')})")
            return result

        except requests.exceptions.HTTPError as e:
            print(f"[!] Error sending status for entry {record.person.external_entry_id}: {e}\n API response: {response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"[!] Error sending status for entry {record.person.external_entry_id}: {e}\n API response: {response.text}")
            return None
        except Exception as e:
            print(f"[!] An unexpected error occurred: {e}")
            return None