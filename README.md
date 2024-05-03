# F1 data API

**Creators**
*Team Turts:*
* Robin Söderholm
* Hampus Hägglund
* Jannik Skovgaard


### Introduction
    Team Turts Formula 1 API, brings you closer to the the drivers racing Formula 1.
    🏎️ What data can you get:
    * All Formula 1 drivers of 2024
    * Driver stats
    * Interact with user-defined presets and preferences stored in our database

### Installation
    The API is set up on a local SQLite database, for more flexibility and customization set up your own
    database and rearrange the database routes to your own. For guidance on SQLite, 
    refer to the official documentation (see references at the end).

### Requirements
    * Ensure you install have the following tools and packages installed to use the API:
        * Python: The API is built with Python. Make sure Python is installed on your system (for the link see references at the end). 
    
    * Dependencies: The required packages are listed in the 'requirements.txt' file. Can be installed using the following command:
        *$ bash
    'pip install -r requirements.txt'
   
    * Included packages:
        * 'Flask': Web application framework.
        * 'Requests': User-friendly HTTP library.

### Setup
    1. Clone the repository.
    2. Install dependencies from 'requirements.txt'.
    3. (Optional) Set up your own database for more customization.
    4. Set the 'API_SPORTS_KEY' in the 'config.py' for API authentication (should be located in the directory with main.py).
    5. Run 'python main.py' to start the server.


## Project Structure

#### Backend
    * main.py: Script running the Flask API server.
    * config.py - Storing configurations such as API keys (not included in the GitHub repo).
    * F1searchpresets.db: local SQlite database file used for the project.

#### Documentation:
    * 'docs.yaml': Documents API usage, data formats, request examples, and more.  

#### API data format
    * Responses are formatted in JSON

#### How the API works
    1. Request data from the API by following the docs.yaml
    2. As data is in JSON object format, you're able to retrieve specific data by filtering it as {key: value} pairs,
        where you request the key for the value (data) you want. 

    * We currently allow 100 requests per day. If more is needed we recommend caching the data, reference:

### Methods and validations
##### Interacting with external API:
    
    * This API interacts with an external Formula 1 data provider to verify and retrieve current information and stats about drivers.
        Before storing any user 'interests' in the local database 'F1searchpresets.db', the API validates the driver's name against the external API.
        This ensures all user interests are real current drivers of Formula 1 2024.

##### Data validation process
    When a POST request is made to '/presets', the API performs the following steps:
    1. Receives the user's input for the driver's name.
    2. Requests the external API to fetch the current list of F1 drivers.
    3. Check if the submitted driver's name (step 1) exists in the fetched list.
    4. If the driver exists, the API proceeds to store the user's preset interest in the database.
    5. If the driver does NOT exist, returns an error message referring the user to check spelling or the current season's driver list.
    The method was implemented to ensure the database remains accurate and up to date with valid F1 driver information. 

#### API Endpoints and Database Methods
    * '/api/docs': Returns the API documentation

    * '/drivers': Returns current F1 driver standings

    * '/presets': Allows retrieval and insertion of user presets (specific driver) in the database 
        * Supports GET and POST if the driver's name is valid.

    * '/db/<item_id>': Retrieves or deletes a specific database record based on the ID
        * Supports GET and DELETE rows by ID.

#### Improvements
    * API authentication, secure data transmissions.

    * Cache data from external API, which is limited to 100 requests per day. We can update our data cache every 3 times per hour, or 72 times per day.
    This approach would ensure API users can access the data without directly impacting the limit set by the external API.  

##### References
* SQLite data: *[SQLite Documentation](https://docs.python.org/3/library/sqlite3.html)*
* External API: *[api-Sports Documentation](https://api-sports.io/documentation/formula-1/v1#section/Introduction)*
* docs.yaml documentation: *[OpenAPI Documentation](https://spec.openapis.org/oas/latest.html)*
* Flask: *[Flask Documentation](https://spec.openapis.org/oas/latest.html)*
* Python: *[python.org](https://www.python.org/downloads/)*
