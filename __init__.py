
import json
import logging
import uuid
import datetime
import pytz

from requests import request

NAME = 'TimeularAPI'

logging.basicConfig(filename=f'{NAME}.log',filemode='w+',level=logging.DEBUG)

class TimeularAPI(object):

    def __init__(self,
            api_key, api_secret,
            timezone,
            timeout = 5,
            debug = False
    ):
        self.__apikey__ = api_key
        self.__apisecret__ = api_secret
        self.__token__ = None
        self.__debugflag__ = debug
        self.__timezone__ = pytz.timezone(timezone)
        self.__timeout__ = timeout
        self.__baseurl__ = "https://api.timeular.com/api/v3/"
        self.__default_space_id__ = None
        self.__user_id__ = None

    def __enter__(self):
        logging.debug('start __enter__')
        self.sign_in()
        self.__get_user_ids__()
        logging.debug('returning self __enter__')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.debug('start __exit_')
        self.logout()
        logging.debug('end __exit_')

    def __get_user_ids__(self):
        response = self.get_user()
        self.__default_space_id__ = int(response['defaultSpaceId'])
        self.__user_id__ = int(response['userId'])

################################################################################
    # Authentication
    ## POST Sign-in with API Key & API Secret
    def sign_in(self):
        """
        Signs in to the Timeular API using the provided API key and secret.

        This method sends a POST request to the Timeular API's developer sign-in
        endpoint with the provided API key and secret. Upon successful sign-in, it
        retrieves an access token, which is stored in the `self.__token__` attribute.

        If the `self.__token__` attribute is already set, this method will not attempt
        to sign in again to avoid unnecessary API requests.

        Returns:
            None

        Raises:
            RequestException: If there is an issue with the HTTP request, e.g., network
                problems or server errors.
            KeyError: If the expected 'token' key is not present in the API response.

        Note:
        - Make sure to set the `self.__apikey__` and `self.__apisecret__` attributes
          with your API key and secret before calling this method.
        - The `self.__baseurl__` attribute should be properly set to the base URL of
          the Timeular API.
        - The `self.__timeout__` attribute should be set to the maximum time to wait
          for the HTTP request to complete.

        Example Usage:
        timeular = TimeularAPI()
        timeular.sign_in()
        # You can now use the `timeular` object with an access token for authenticated requests.
        """
        if self.__token__ is None:
            data = {"apiKey": self.__apikey__, "apiSecret": self.__apisecret__}

            url = self.__baseurl__ + 'developer/sign-in'

            response = request('POST',
                url,
                data=json.dumps(data),
                timeout=self.__timeout__
            ).json()

            logging.debug('sign_in - response: %s', response)

            self.__token__ = response['token']

    # GET Fetch API Key
    def fetch_api_key(self):

        data = {}
        url = self.__baseurl__ + 'developer/api-access'
        logging.debug('fetch_api_key - data: %s', data)

        headers = {'Authorization': f'Bearer {self.__token__}'}

        logging.debug('fetch_api_key - headers: %s', headers)

        response = request('GET',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )

        logging.info('fetch_api_key - response: %s', response)

        return response.json()['apiKey']

    # POST Generate new API Key & API Secret
    def generate_new_api_creds(self):

        data = {}
        url = self.__baseurl__ + 'developer/api-access'
        logging.debug('generate_new_api_creds - data: %s', data)

        headers = {'Authorization': f'Bearer {self.__token__}'}

        logging.debug('generate_new_api_creds - headers: %s', headers)

        response = request('POST',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )

        logging.info('generate_new_api_creds - response: %s', response)

        return response.json()

    # POST Logout
    def logout(self):
        """
        Logs out the user from the Timeular API.

        This method sends a POST request to the Timeular API to log out the currently authenticated user.

        Raises:
            TimeularAPIError: If there is an issue with the API request, such as invalid credentials.

        Example:
            timeular = TimeularAPI()
            timeular.login(username, password)
            timeular.logout()

        Note:
            This method will clear the authentication token, and you will need to log in again
            to make further authenticated API calls.
        """
        if self.__token__ is not None:
            data = {}
            logging.debug('logout - data: %s', data)

            url = self.__baseurl__ + 'developer/logout'
            logging.debug('logout - url: %s', url)

            headers = {'Authorization': f'Bearer {self.__token__}'}

            logging.debug('logout - headers: %s', headers)

            response = request('POST',
                url,
                data=json.dumps(data),
                headers=headers,
                timeout=self.__timeout__
            )

            logging.info('logout - response: %s', response)
            self.__token__ = None
            logging.info('logout - __token__: %s', self.__token__)

################################################################################
# Integrations
# GET List enabled Integrations
    def get_enabled_integrations(self):

        data = {}
        url = self.__baseurl__ + 'integrations'
        logging.debug('get_enabled_integrations - data: %s', data)

        headers = {'Authorization': f'Bearer {self.__token__}'}

        logging.debug('get_enabled_integrations - headers: %s', headers)

        response = request('GET',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )

        logging.info('get_enabled_integrations - response: %s', response)

        return response.json()['integrations']

################################################################################
# Time Tracking
## Activities
# GET List all Activities
    def get_all_activities(self):

        data = {}
        url = self.__baseurl__ + 'activities'
        logging.debug('get_all_activities - data: %s', data)

        headers = {'Authorization': f'Bearer {self.__token__}'}

        logging.debug('get_all_activities - headers: %s', headers)

        response = request('GET',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )

        logging.info('get_all_activities - response: %s', response)

        return response.json()

# TODO: POST Create an Activity
# TODO: PATCH Edit an Activity
# TODO: DEL Archive an Activity
# TODO: POST Assign an Activity to Device Side
# TODO: DEL Unassign an Activity from a Device Side
########################################
## Devices
# GET List all known Devices
    def get_all_known_devices(self):

        data = {}
        url = self.__baseurl__ + 'devices'
        logging.debug('get_all_known_devices - data: %s', data)

        headers = {'Authorization': f'Bearer {self.__token__}'}

        logging.debug('get_all_known_devices - headers: %s', headers)

        response = request('GET',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )

        logging.info('get_all_known_devices - response: %s', response)

        return response.json()['devices']

# TODO: POST Activate Device
# TODO: POST Deactivate Device
# TODO: PATCH Edit Device
# TODO: DEL Forget Device
# TODO: POST Disable Device
# TODO: POST Enable Device
########################################
## Current Tracking
# GET Show current Tracking
    def get_current_tracking(self):

        data = {}
        url = self.__baseurl__ + 'tracking'
        logging.debug('get_current_tracking - data: %s', data)

        headers = {'Authorization': f'Bearer {self.__token__}'}

        logging.debug('get_current_tracking - headers: %s', headers)

        response = request('GET',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )

        logging.info('get_current_tracking - response: %s', response)

        return response.json()['currentTracking']

# POST Start Tracking
    def start_tracking(self, activity_id:int, started_at: datetime.datetime = datetime.datetime.utcnow()):

        data = {
            'startedAt': started_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        }
        logging.debug('start_tracking - data: %s', data)

        url = self.__baseurl__ + f'tracking/{str(activity_id)}/start'
        logging.debug('start_tracking - url: {url}')

        headers = {
            'Authorization': f'Bearer {self.__token__}', 
            'Subscriber-ID': str(self.__user_id__), 
            'Content-Type': 'application/json'
            }

        logging.debug('start_tracking - headers: %s', headers)

        response = request('POST',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )

        logging.info('start_tracking - response: {response.text}')

        return response.json()

# PATCH Edit Tracking
# POST Stop Tracking
    def stop_tracking(self, stopped_at: datetime.datetime = datetime.datetime.utcnow()):

        data = {
            'stoppedAt': stopped_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        }
        logging.debug('stop_tracking - data: %s', data)

        url = self.__baseurl__ + 'tracking/stop'
        logging.debug('stop_tracking - url: {url}')

        headers = {
            'Authorization': f'Bearer {self.__token__}', 
            'Subscriber-ID': str(self.__user_id__), 
            'Content-Type': 'application/json'
            }

        logging.debug('stop_tracking - headers: %s', headers)

        response = request('POST',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )

        logging.info('stop_tracking - response: %s', response)

        return response.json()

########################################
## Time Entries
# GET Find Time Entries in given range
    def get_time_entries_in_range(self, start: datetime.datetime, end: datetime.datetime):
        """Find Time Entries within the given time range.

        Args:
            start (datetime.datetime): datetime object for the start
            end (datetime.datetime): datetime object for the end

        Returns:
            dict: all time entries in the given range
        """
        s_start = start.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        s_end = end.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

        data = {}
        url = self.__baseurl__ + f'time-entries/{s_start}/{s_end}'
        logging.debug('get_time_entries_in_range - data: %s', data)

        headers = {'Authorization': f'Bearer {self.__token__}'}

        logging.debug('get_time_entries_in_range - headers: %s', headers)

        response = request('GET',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )

        logging.info('get_time_entries_in_range - response: %s', response)

        return response.json()['timeEntries']

# TODO: POST Create Time Entry
# GET Find Time Entry by its ID
    def get_time_entry_by_id(self, entry_id: int):
        """Find Time Entry by its ID

        Args:
            entry_id (int): ID of the required time entry

        Returns:
            dict: of the Time Entry
        """

        data = {}
        url = self.__baseurl__ + f'time-entries/{entry_id}'
        logging.debug('get_time_entry_by_id - data: %s', data)

        headers = {'Authorization': f'Bearer {self.__token__}'}

        logging.debug('get_time_entry_by_id - headers: %s', headers)

        response = request('GET',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )

        logging.info('get_time_entry_by_id - response: %s', response)

        return response.json()

# TODO: PATCH Edit a Time Entry
# TODO: DEL Delete a Time Entry
########################################
## Reports
# TODO: GET Generate Report
# GET All Data as JSON
    def get_all_data_as_json(self, start: datetime.datetime, end: datetime.datetime):
        """
        Generates a Report which contains all the Time Entries from inside the given time range as JSON from all personal spaces and shared spaces. If some Time Entry exceeds the report’s time range, only matching part will be included.
        
        Args:
            start (datetime.datetime): datetime object for the start
            end (datetime.datetime): datetime object for the end

        Returns:
            dict: all time entries in the given range
        """

        s_start = start.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        s_end = end.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

        data = {}
        url = self.__baseurl__ + f'time-entries/{s_start}/{s_end}'
        logging.debug('get_all_data_as_json - data: %s', data)

        headers = {'Authorization': f'Bearer {self.__token__}'}

        logging.debug('get_all_data_as_json - headers: %s', headers)

        response = request('GET',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )

        logging.info('get_all_data_as_json - response: %s', response)

        return response.json()['timeEntries']

########################################
    ## Tags & Mentions

    ### GET Fetch Tags & Mentions
    def fetch_tags_mentions(self):
        """
        Fetches tags and mentions from the Timeular API.

        Returns:
            dict: A dictionary containing tags and mentions data.
        """
        data = ""
        logging.debug('fetch_tags_mentions - data: %s', data)

        url = self.__baseurl__ + 'tags-and-mentions'
        logging.debug('fetch_tags_mentions - url: {url}')

        headers = {'Authorization': f'Bearer {self.__token__}'}

        logging.debug('fetch_tags_mentions - headers: %s', headers)

        response = request('GET',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )

        logging.info('fetch_tags_mentions - response: %s', response)
        return response.json()

    def fetch_tags(self):
        """
        Fetches only the tags from the Timeular API.

        Returns:
            list: A list of tags.
        """
        return self.fetch_tags_mentions()['tags']

    def fetch_mentions(self):
        """
        Fetches only the mentions from the Timeular API.

        Returns:
            list: A list of mentions.
        """
        return self.fetch_tags_mentions()['mentions']

    ### POST Create Tag
    def create_tag(self, label, scope='timeular', space_id=None):
        """
        Create a new tag using the TimeularAPI.

        Args:
            label (str): The label/name of the tag you want to create.
            scope (str, optional): The scope of the tag (default is 'timeular').
            space_id (str, optional): The ID of the space where you want to create the tag. If not provided,
                the default space ID will be used.

        Returns:
            dict: A dictionary containing information about the created tag, including its unique key, label,
            scope, and space ID.

        Raises:
            Exception: If there is an issue with the HTTP request or if the response indicates an error.

        Note:
            This function sends a POST request to the Timeular API to create a new tag with the specified
            parameters. It requires authorization through the 'Bearer' token provided when initializing
            the TimeularAPI. The function logs debug and info messages for tracking the process.

        Example:
            To create a new tag with the label 'Work' and a custom space ID:
            >>> timeularAPI.create_tag("Work", "timeular", "custom_space_id")
    """
        if space_id is None:
            space_id = self.__default_space_id__

        data = {
            "key": str(uuid.uuid4()),
            "label": label,
            "scope": scope,
            "spaceId": str(space_id)
            }
        logging.debug('create_tag - data: %s', data)

        url = self.__baseurl__ + 'tags'

        logging.debug('create_tag - url: {url}')

        headers = {'Authorization': f'Bearer {self.__token__}', 'Content-Type': 'application/json'}
        logging.debug('create_tag - headers: %s', headers)

        response = request('POST',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )
        logging.info('create_tag - response: %s', response)
        return response.json()

    ### PATCH Update Tag
    def update_tag(self, tag_id: int, label):
        """
        Update a tag with the specified tag_id using the Timeular API.

        Args:
            tag_id (int): The unique identifier of the tag to be updated.
            label (str): The new label to set for the tag.

        Returns:
            dict: A dictionary representing the updated tag information, typically containing the tag's ID and label.
            
        Raises:
            - RequestException: If there was an issue with the HTTP request to the Timeular API.
            - ValueError: If the provided tag_id is not a positive integer.
            - TypeError: If the provided label is not a string.
            - json.JSONDecodeError: If the response from the API cannot be parsed as JSON.

        Note:
            This function sends a PATCH request to the Timeular API to update the label of the specified tag.
            It requires the user to be authenticated with a valid bearer token (access token).

        Example:
            # Update the label of a tag with ID 123 to "Work"
            updated_tag = timeularApi.update_tag(123, "Work")
        """
        data = {
            "label": label
            }
        logging.debug('update_tag - data: %s', data)

        url = self.__baseurl__ + 'tags/' +  str(tag_id)

        logging.debug('update_tag - url: {url}')

        headers = {'Authorization': f'Bearer {self.__token__}', 'Content-Type': 'application/json'}
        logging.debug('update_tag - headers: %s', headers)

        response = request('PATCH',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )
        logging.info('update_tag - response: %s', response)
        return response.json()

    ### DEL Delete Tag
    def delete_tag(self, tag_id: int):
        """
        Deletes a tag with the specified tag_id.

        Args:
            tag_id (int): The ID of the tag to be deleted.

        Returns:
            dict: A dictionary containing the response data from the Timeular API after
                attempting to delete the tag.

        Raises:
            Exception: If the request to delete the tag fails, an exception will be raised.

        Notes:
            This function sends a DELETE request to the Timeular API to delete a tag with the
            specified tag_id. The request is authenticated using the provided access token.

        Example:
            To delete a tag with tag_id 123, you can call the function as follows:
            response = timeular_api.delete_tag(123)
            print(response)

        See Also:
            - `TimeularAPI`: The main class for interacting with the Timeular API.
            - `create_tag`: Use this method to create a new tag.
            - `update_tag`: Use this method to update the details of an existing tag.
        """

        data = {}
        logging.debug('delete_tag - data: %s', data)

        url = self.__baseurl__ + 'tags/' +  str(tag_id)

        logging.debug('delete_tag - url: {url}')

        headers = {'Authorization': f'Bearer {self.__token__}', 'Content-Type': 'application/json'}
        logging.debug('delete_tag - headers: %s', headers)

        response = request('DELETE',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )
        logging.info('delete_tag - response: %s', response)
        return response.json()

    ### POST Create Mention
    def create_mention(self, label, scope='timeular', space_id=None):
        """
        Create a mention with the specified label.

        Args:
            label (str): The label for the mention.
            scope (str, optional): The scope of the mention (default is 'timeular').
            space_id (int, optional): The ID of the space where the mention will be created.

        Returns:
            dict: A JSON response containing information about the created mention.

        """
        if space_id is None:
            space_id = self.__default_space_id__

        data = {
            "key": str(uuid.uuid4()),
            "label": label,
            "scope": scope,
            "spaceId": str(space_id)
            }

        logging.debug('create_mention - data: %s', data)

        url = self.__baseurl__ + 'mentions'
        logging.debug('create_mention - url: {url}')

        headers = {'Authorization': f'Bearer {self.__token__}', 'Content-Type': 'application/json'}
        logging.debug('create_mention - headers: %s', headers)

        response = request('POST',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )
        logging.info('create_mention - response: %s', response)
        return response.json()

    ### PATCH Update Mention
    def update_mention(self, mention_id: int, label):
        """
        Update the label of an existing mention.

        Args:
            mention_id (int): The ID of the mention to be updated.
            label (str): The new label for the mention.

        Returns:
            dict: A JSON response containing information about the updated mention.

        """
        data = {
            "label": label
            }
        logging.debug('update_mention - data: %s', data)

        url = self.__baseurl__ + 'mentions/' +  str(mention_id)

        logging.debug('update_mention - url: {url}')

        headers = {'Authorization': f'Bearer {self.__token__}', 'Content-Type': 'application/json'}
        logging.debug('update_mention - headers: %s', headers)

        response = request('PATCH',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )
        logging.info('update_mention - response: %s', response)
        return response.json()

    ### DEL Delete Mention
    def delete_mention(self, mention_id: int):
        """
        Delete a mention with the specified ID.

        Args:
            mention_id (int): The ID of the mention to be deleted.

        Returns:
            dict: A JSON response containing information about the deletion status.

        """
        data = {}
        logging.debug('delete_mention - data: %s', data)

        url = self.__baseurl__ + 'mentions/' +  str(mention_id)

        logging.debug('delete_mention - url: {url}')

        headers = {'Authorization': f'Bearer {self.__token__}', 'Content-Type': 'application/json'}
        logging.debug('delete_mention - headers: %s', headers)

        response = request('DELETE',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )
        logging.info('delete_mention - response: %s', response)
        return response.json()

################################################################################
    # User Profile
    ## User
    ### GET Me
    def get_user(self):
        """
        Retrieve information about the authenticated user.

        Returns:
            dict: A JSON response containing information about the user.

        """
        data = {}
        logging.debug('get_user - data: %s', data)

        url = self.__baseurl__ + 'me'
        logging.debug('get_user - url: {url}')

        headers = {'Authorization': f'Bearer {self.__token__}'}

        logging.debug('get_user - headers: %s', headers)

        response = request('GET',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )

        logging.info('get_user - response: %s', response)
        return response.json()['data']

    ## Space
    ### GET Spaces with Members
    def get_spaces_with_members(self):
        """
        Retrieve a list of spaces along with their members.

        Returns:
            list: A list of spaces with associated member information.

        """
        data = {}
        logging.debug('get_spaces_with_members - data: %s', data)

        url = self.__baseurl__ + 'space'
        logging.debug('get_spaces_with_members - url: {url}')

        headers = {'Authorization': f'Bearer {self.__token__}'}

        logging.debug('get_spaces_with_members - headers: %s', headers)

        response = request('GET',
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=self.__timeout__
        )

        logging.info('get_spaces_with_members - response: %s', response)
        return response.json()['data']
