from abc import ABC
from ..client_connection import ClientConnection
from .http.http_client import HttpClient

class BaseClient(ABC):
    """Abstract base client class"""

    api_version: str = '6.0'
    api_version_preview: str = '6.0-preview.3'

    # Constructor
    def __init__(self, client_connection: ClientConnection) -> None:
        super().__init__()

        self._client_connection: ClientConnection = client_connection
        self._http_client: HttpClient = client_connection.http_client
    
    ### Properties section ###

    @property
    def client_connection(self) -> ClientConnection:
        """
        """
        return self._client_connection
    
    @property
    def http_client(self) -> HttpClient:
        """
        """
        return self._http_client