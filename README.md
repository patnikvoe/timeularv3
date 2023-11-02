# timeularv3

a python implementation of version3 of the timeular public API https://developers.timeular.com/

## Implemented
### Authentication
- POST Sign-in with API Key & API Secret
- GET Fetch API Key
- POST Generate new API Key & API Secret
- POST Logout

### Integrations
- GET List enabled Integrations

### Time Tracking
#### Activities
- GET List all Activities

#### Devices
- GET List all known Devices

#### Current Tracking
- GET Show current Tracking

#### Time Entries
- GET Find Time Entries in given range

- GET Find Time Entry by its ID


#### Reports
- GET All Data as JSON

#### Tags & Mentions
- GET Fetch Tags & Mentions
- POST Create Tag
- PATCH Update Tag
- DEL Delete Tag
- POST Create Mention
- PATCH Update Mention
- DEL Delete Mention


## TODO

### Time Tracking
#### Activities
- POST Create an Activity
- PATCH Edit an Activity
- DEL Archive an Activity
- POST Assign an Activity to Device Side
- DEL Unassign an Activity from a Device Side

#### Devices
- POST Activate Device
- POST Deactivate Device
- PATCH Edit Device
- DEL Forget Device
- POST Disable Device
- POST Enable Device

#### Current Tracking
- POST Start Tracking
- PATCH Edit Tracking
- POST Stop Tracking

#### Time Entries
- POST Create Time Entry

- PATCH Edit a Time Entry
- DEL Delete a Time Entry

#### Reports
- GET Generate Report -> Requires Pro Subscription, I do not have it to test
