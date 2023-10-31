# timeularv3

a python implementation of version3 of the timeular public API https://developers.timeular.com/

## Implemented
### Authentication
- POST Sign-in with API Key & API Secret
- GET Fetch API Key
- POST Logout

### Time Tracking
#### Tags & Mentions
- GET Fetch Tags & Mentions
- POST Create Tag
- PATCH Update Tag
- DEL Delete Tag
- POST Create Mention
- PATCH Update Mention
- DEL Delete Mention


## TODO
### Authentication
- POST Generate new API Key & API Secret

### Integrations
- GET List enabled Integrations

### Time Tracking
#### Activities
- GET List all Activities
- POST Create an Activity
- PATCH Edit an Activity
- DEL Archive an Activity
- POST Assign an Activity to Device Side
- DEL Unassign an Activity from a Device Side

#### Devices
- GET List all known Devices
- POST Activate Device
- POST Deactivate Device
- PATCH Edit Device
- DEL Forget Device
- POST Disable Device
- POST Enable Device

#### Current Tracking
- GET Show current Tracking
- POST Start Tracking
- PATCH Edit Tracking
- POST Stop Tracking

#### Time Entries
- GET Find Time Entries in given range
- POST Create Time Entry
- GET Find Time Entry by its ID
- PATCH Edit a Time Entry
- DEL Delete a Time Entry

#### Reports
- GET Generate Report
- GET All Data as JSON
