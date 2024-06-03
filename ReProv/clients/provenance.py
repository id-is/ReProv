import requests
from .base_client import AbstractClient

class ProvenanceClient(AbstractClient):
    def __init__(self):
        super().__init__("provenance")

    def get_all(self):
        pass

    def get(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def capture(self, execution_id):
        url = f"{self.base_url}/capture/{execution_id}"
        return self._request("GET", url)

    def draw(self, execution_id):
        url = f"{self.base_url}/draw/{execution_id}"
        return self._download_file(url, 'prov.png')

