import requests
from abc import ABC, abstractmethod
from ..config import BASE_URL, API_KEY

class AbstractClient(ABC):
    def __init__(self, endpoint):
        """
        Initialize the AbstractClient with a specific API endpoint.
        """
        self.base_url = f"{BASE_URL}/{endpoint}"
        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
    
    @abstractmethod
    def get(self, item_id):
        """
        Abstract method to get an item by its ID.
        """
        pass

    @abstractmethod
    def create(self, item_data):
        """
        Abstract method to create a new item.
        """
        pass

    @abstractmethod
    def update(self, item_id, item_data):
        """
        Abstract method to update an existing item by its ID.
        """
        pass

    @abstractmethod
    def delete(self, item_id):
        """
        Abstract method to delete an item by its ID.
        """
        pass

    def _request(self, method, url, body=None):
        """
        Internal method to handle HTTP requests using the requests library.
        """
        try:
            response = requests.request(method, url, headers=self.headers, json=body)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            self._handle_http_error(http_err)
            return None
        except Exception as err:
            print(f"An error occurred: {err}")
            return None

    def _handle_http_error(self, http_error):
        """
        Internal method to handle HTTPError raised by the requests library.
        """
        print(f"API request failed: {http_error}")
        status_code = http_error.response.status_code
        if status_code == 400:
            print("Bad request. Please check your input data.")
        elif status_code == 401:
            print("Unauthorized. Please check your API key.")
        elif status_code == 404:
            print("Resource not found. Please check the ID.")
        elif status_code == 500:
            print("Internal server error. Please try again later.")
        else:
            print(f"Unexpected error: {http_error}")

# Example of a concrete implementation
class ExampleClient(AbstractClient):
    def get(self, item_id):
        url = f"{self.base_url}/{item_id}"
        return self._request("GET", url)

    def create(self, item_data):
        url = self.base_url
        return self._request("POST", url, body=item_data)

    def update(self, item_id, item_data):
        url = f"{self.base_url}/{item_id}"
        return self._request("PUT", url, body=item_data)

    def delete(self, item_id):
        url = f"{self.base_url}/{item_id}"
        return self._request("DELETE", url)

# Usage example
if __name__ == "__main__":
    client = ExampleClient("example_endpoint")
    item = client.get("123")
    print(item)
