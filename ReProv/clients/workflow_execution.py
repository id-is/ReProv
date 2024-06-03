import requests
import json
from .base_client import AbstractClient

class WorkflowExecutionClient(AbstractClient):
    def __init__(self):
        """
        Initialize the WorkflowExecutionClient with the base URL for workflow execution.
        """
        super().__init__("workflow_execution")

    def get_all(self):
        """
        List all executed workflows.

        """
        url = f"{self.base_url}/"
        return self._request("GET", url)

    def get(self, execution_id):
        """
        Get details of a specific workflow execution by execution_id.

        :param execution_id: The ID of the workflow execution.
        :return: Details of the specified workflow execution.
        """
        url = f"{self.base_url}/{execution_id}"
        return self._request("GET", url)

    def create(self, registry_id):
        """
        Execute a workflow by registry_id.

        :param registry_id: The ID of the workflow registry.
        :return: Response from the workflow execution request.
        """
        url = f"{self.base_url}/execute/{registry_id}"
        return self._request("POST", url)

    def delete(self, execution_data):
        """
        Delete a specific workflow execution.

        :param execution_data: The registry ID or an object with a reana_name attribute.
        :return: Response from the delete request.
        """
        if isinstance(execution_data, int):
            url = f"{self.base_url}/delete/?registry_id={execution_data}"
        elif hasattr(execution_data, 'reana_name'):
            url = f"{self.base_url}/delete/?reana_name={execution_data.reana_name}"
        else:
            raise ValueError("execution_data must be an integer (registry_id) or an object with a reana_name attribute")
        
        return self._request("DELETE", url)
    
    def download_outputs(self, execution_id, path='outputs.zip'):
        """
        Download outputs of a specific workflow execution by execution_id.

        :param execution_id: The ID of the workflow execution.
        :param path: The path where the downloaded file will be stored
        :return: The downloaded output file content.
        """
        url = f"{self.base_url}/outputs/{execution_id}"

        return self._download_file(url, path)

    def download_inputs(self, execution_id, path='inputs.zip'):
        """
        Download inputs of a specific workflow execution by execution_id.

        :param execution_id: The ID of the workflow execution.
        :param path: The path where the downloaded file will be stored
        :return: The downloaded input file content.
        """
        url = f"{self.base_url}/inputs/{execution_id}"
        return self._download_file(url, path)
    

    def update(self, execution_id):
        pass
