# CFG_Summer2024_Degree_Group_Project_G5
CFG Degree Software and Data engineering G1 summer cohort, group 5 project repository

# How To get the OpenTripMaps API Key
- Open the OpenTripMap website: [Click here](https://dev.opentripmap.org/)
- Create an account by clicking on 'Register'
- Enter your personal information
- Confirm your email through the email they will send you (check you spam!)
- You can find your API key in 'My Account/Settings'

# Obtaining a weatherapi API Key

Navigate to https://www.weatherapi.com/signup.aspx and create an account.
1. You'll be presented with / navigate to https://www.weatherapi.com/my/ for the API key.
2. For the Swagger navigate to https://app.swaggerhub.com/apis-docs/WeatherAPI.com/WeatherAPI/1.0.2, scroll down and select the 'Authorize' button and enter your API key to start using it


## Database Config

1. Set up database

Go to `database/destinations_db.sql` as well as `database/customer_details_db.sql` and run the scripts in MySQL workbench
to set up the database

2. Config DB password 

Go to `config_oli.py`, replace "Password, please" with your own database password :
```shell
PASSWORD = "Password, please"
```

# Obtaining a travelpayouts API Key

Visit https://www.travelpayouts.com/ and create an account.
1. Scroll to the bottom and click "I’m here for White Label or API"
2. Click create project in the popup 
3. once created, click the sidebar > click api and data > hotels api > hotels data api > api token hyperlink >  connect to hotellook > connect > api from the overview sidebar    

## config.py format
config.py is in the gitignore list as it holds sensitive information so it will need to be added manually in the root folder and is formatted as below:
```python
weather_api_key = "<your_key>"
activities_api_key = "<your_key>"
hotels_api_key = "<your_key>"
HOST = "<your_local_db_host_name>"
PASSWORD = "<your_local_db_password>"
USER = "<your_local_db_user_name>"
```

