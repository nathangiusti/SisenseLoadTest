import urllib.parse

from PySense import PySenseException
from PySense import PySenseUtils


class LoadTestConnector:

    def __init__(self, host, token, client):
        self._host = PySenseUtils.format_host(host)
        self._token = token
        self._client = client

    def rest_call(self, action_type, url, *, data=None, json_payload=None, query_params=None, raw=False):
        """Run an arbitrary rest command against your Sisense instance and returns the JSON response

        Args:
            action_type: REST request type
            url: url to hit, example api/v1/app_database/encrypt_database_password or api/branding
            data: (optional) The data portion of the payload
            json_payload: (optional) The json portion of the payload
            query_params: (optional) A dictionary of query values to be added to the end of the url
            raw: (optional) True if raw content response wanted

        Returns:
            Returns the json content blob. If raw is set to true, returns the raw bytes of the content.
        """

        action_type = action_type.lower()
        if query_params is not None:
            query_string = build_query_string(query_params)
        else:
            query_string = ''
        full_url = '{}{}'.format(url, query_string)

        if action_type == 'get':
            response = self._client.get(full_url, headers=self._token, data=data, json=json_payload)
        elif action_type == 'post':
            response = self._client.post(full_url, headers=self._token, data=data, json=json_payload)
        elif action_type == 'put':
            response = self._client.put(full_url, headers=self._token, data=data, json=json_payload)
        elif action_type == 'delete':
            response = self._client.delete(full_url, headers=self._token, data=data, json=json_payload)

        parse_response(response)
        if len(response.content) == 0:
            return None
        elif raw:
            return response.content
        else:
            try:
                return response.json()
            except ValueError as e:
                return response.content


def parse_response(response):
    """Parses response and throw exception if not successful."""
    if response.status_code not in [200, 201, 204]:
        raise PySenseException.PySenseException('ERROR: {}: {}\nURL: {}'
                                                .format(response.status_code, response.content, response.url))


def build_query_string(dictionary):
    """Builds a query string based on the dictionary passed in"""
    ret_arr = []
    separator = '&'
    for key, value in dictionary.items():
        if value is not None:
            if isinstance(value, bool):
                if value is True:
                    validated = 'true'
                elif value is False:
                    validated = 'false'
            elif isinstance(value, list):
                validated = ','.join(value)
            else:
                if key != 'query':
                    validated = urllib.parse.quote(str(value))
                else:
                    validated = str(value)
            ret_arr.append("{}={}".format(key, validated))
    query_string = separator.join(ret_arr)
    if len(query_string) > 1:
        return '?' + query_string
    else:
        return ''





