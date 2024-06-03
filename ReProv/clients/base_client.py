import requests
import os 
from abc import ABC, abstractmethod
from ..utils.authentication import get_access_token
from dotenv import load_dotenv

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
load_dotenv(os.path.join(parent_dir, '.env'))

class AbstractClient(ABC):
    def __init__(self, endpoint):
        """
        Initialize the AbstractClient with a specific API endpoint.
        """
        self.base_url = f"{os.environ['BASE_URL']}/{endpoint}"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_access_token()}"
        }
    
    @abstractmethod
    def get_all(self):
        """
        Abstract method to get every item by its ID.
        """
        pass

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

    def _request(self, method, url, params=None, files=None, body=None):
        """
        Internal method to handle HTTP requests, with support for file uploads.
        """
        try:
            if files:
                # Ensure files are properly prepared for multipart/form-data request
                response = requests.request(method, url, headers=self.headers, params=params, files=files)
            else:
                # Standard request for other cases
                response = requests.request(method, url, headers=self.headers, json=body)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            if http_err.response is not None:
                print(f"Server response: {http_err.response.text}")
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


    def _download_file(self, url, path):
        """
        Internal method to handle file download.

        :param url: The URL from which to download the file.
        :param path: The path where the downloaded file will be stored
        :return: The content of the downloaded file.
        """
        response = requests.get(url, headers=self.headers)
 
        content_type = response.headers.get('Content-Type')

        if 'application/json' in content_type:
            data = response.json()
            print('Error:', data)
        else:
            file_content = response.content
            with open(path, 'wb') as file:
                file.write(file_content)