import base64
import requests
from requests.packages import urllib3
from urllib.parse import urljoin
from requests_ntlm import HttpNtlmAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class _BaseUrlSession(requests.Session):
    base_url: str = None

    def __init__(self, base_url: str = None) -> None:
        if base_url:
            self.base_url = base_url
        
        super(_BaseUrlSession, self).__init__()
    
    def request(self, method, url, *args, **kwargs):
        """Send the request after generating the complete URL"""
        
        request_url = self.create_url(url)
        return super(_BaseUrlSession, self).request(method, request_url, *args, **kwargs)
    
    def create_url(self, url: str):
        """Create the URL based off this partial path"""

        return urljoin(self.base_url, url)

class HttpException(Exception):
    pass

class HttpClient:
    def __init__(self, base_url: str, verify: bool=False) -> None:
        if not base_url.endswith('/'):
            base_url += '/'
        
        self.__base_url = base_url
        self.__httpClient = _BaseUrlSession(base_url=self.__base_url)
        self.__verify_ssl = verify
    
    @property
    def base_url(self) -> str:
        return self.__base_url
    
    @base_url.setter
    def base_url(self, base_url: str) -> None:
        if not base_url.endswith('/'):
            base_url += '/'

        self.__base_url = base_url
        self.__httpClient.base_url = base_url
    
    def authentificate_with_password(self, user_name: str, user_password: str) -> None:
        if user_name is None and user_password is None:
            raise HttpException('Authentificate error: user_name or user_password can\'t be None')

        self.__httpClient.auth = HttpNtlmAuth(user_name, user_password)
    
    def authentificate_with_pat(self, personal_access_token: str) -> None:
        if not personal_access_token:
            raise HttpException('Authentificate error: personal access token can\'t be None')

        pat = ':' + personal_access_token
        pat_base64 = b'Basic ' + base64.b64encode(pat.encode("utf8"))

        self.__httpClient.headers.update({'Authorization': pat_base64})
    
    def get(self, resource: str, query_params=None, custom_headers=None):
        response = self.__httpClient.get(resource, 
            params=query_params, 
            headers=custom_headers,
            verify=self.__verify_ssl)
        response.raise_for_status()

        return response
    
    def post(self, resource: str, data, query_params=None, custom_headers=None):
        response = self.__httpClient.post(resource, 
            data=data, 
            params=query_params, 
            headers=custom_headers,
            verify=self.__verify_ssl)
        response.raise_for_status()

        return response
    
    def post_json(self, resource: str, json_data, query_params=None, custom_headers=None):
        response = self.__httpClient.post(resource, 
            json=json_data, 
            params=query_params, 
            headers=custom_headers,
            verify=self.__verify_ssl)
        response.raise_for_status()

        return response
    
    def patch(self, resource: str, data, query_params=None, custom_headers=None):
        response = self.__httpClient.patch(resource,
            data=data,
            params=query_params,
            headers=custom_headers,
            verify=self.__verify_ssl)
        response.raise_for_status()

        return response

    def patch_json(self, resource: str, json_data, query_params=None, custom_headers=None):
        response = self.__httpClient.patch(resource,
            json=json_data,
            params=query_params,
            headers=custom_headers,
            verify=self.__verify_ssl)
        response.raise_for_status()

        return response