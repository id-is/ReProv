import requests
import os
from .base_client import AbstractClient

class WorkflowRegistryClient(AbstractClient):
    def __init__(self):
        super().__init__("workflow_registry")

    def get_all(self):
        """
        List all workflows.
        :return: The JSON response from the server.
        """
        url = f"{self.base_url}/"
        return self._request("GET", url)

    def get(self, registry_id):
        """
        Get details of a specific workflow by registry_id.
        :param registry_id: The ID of the workflow registry to be retrieved.
        :return: The JSON response from the server.
        """
        url = f"{self.base_url}/{registry_id}"
        return self._request("GET", url)

    def create(self, params, spec_file_path, input_file_path=None):
        """
        Upload a file to the workflow registry.
        
        :param params: Dictionary containing 'name' and 'version'
        :param spec_file_path: Path to the specification file
        :param input_file_path: Path to the input file (optional)
        :return: The JSON response from the server.
        """
        url = f"{self.base_url}/register/"

        with open(spec_file_path, "rb") as spec_file:
            files = {
                "spec_file": (os.path.basename(spec_file_path), spec_file, 'application/octet-stream')
            }
            if input_file_path:
                with open(input_file_path, "rb") as input_file:
                    files["input_file"] = (os.path.basename(input_file_path), input_file, 'application/octet-stream')

            return self._request("POST", url, params=params, files=files)

    def update(self, registry_id, params=None, spec_file_path=None, input_file_path=None):
        """
        Update an existing workflow by registry_id.
        
        This method updates an existing workflow in the registry based on the provided registry_id. 
        Only the provided fields will be updated. If no fields are provided, the update will be skipped.

        :param registry_id: The ID of the workflow registry entry to update.
        :param params: Optional dictionary containing the fields to update.
        :param spec_file_path: Optional path to the specification file to be uploaded.
        :param input_file_path: Optional path to the input file to be uploaded.
        :return: The JSON response from the server.
        """
        url = f"{self.base_url}/update/{registry_id}"
        files = {}
        data = {}

        if params:
            data.update(params)

        if spec_file_path:
            files["spec_file"] = (os.path.basename(spec_file_path),  open(spec_file_path, "rb"), 'application/octet-stream')
        if input_file_path:
            files["input_file"] = (os.path.basename(input_file_path),  open(input_file_path, "rb"), 'application/octet-stream')
        if not data and not files:
            print("No fields to update.")
            return

        if files:
            return self._request("PUT", url, params=data, files=files)
        else:
            return self._request("PUT", url, body=data)
    
    def delete(self, registry_id):
        """
        Delete a workflow by registry_id.
        :param registry_id: The ID of the workflow registry entry to delete.
        :return: The JSON response from the server.

        """
        url = f"{self.base_url}/delete/{registry_id}"
        return self._request("DELETE", url)