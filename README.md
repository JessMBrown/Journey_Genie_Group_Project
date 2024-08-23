![logo.png](README_media/logo.png)
<a name="top"></a>

---
### Your travel wish is our command 🪄
<a href="#introduction">Introduction</a> | <a href="#main-components">Main Components</a> | <a href="#closing">Closing</a> | <a href="#contributors">Contributors</a>
## Introduction

<p>
<img src="README_media/holiday.gif" alt="Holiday GIF" align="right" width="100" height="90" style="margin-left: 20px;">
Welcome to Journey Genie, our console-based application that helps you plan your perfect vacation! Whether you're looking for a luxury experience, a business stay, or a fun family holiday, we've got you covered. Journey Genie eliminates the need to spend hours browsing tonnes of sites as it's all done in one place. Sit back, relax, and let the magic unfold...
</p>

---
<u><a name="main-components"></a>**Main Components:**</u>

🔍 Search for a country/city you're thinking of or, if not sure, activate our *Take me anywhere* option

📆 Narrow your search with dates, number of people and number of rooms

⭐ Filter hotels with the option of 10 categories such as stars, family-friendly and hotels with pools
 
🔗 Clickable link to help decide the perfect hotel for you

🩷 Save your favourites 

🌞 Receive average temperature information for your time of stay

🏄‍ Get suggested attractions and activities in the area

📜 Receive the full plan at the end!

---
## Getting Started

### 1. Clone the repository

In your terminal, open the working directory where you'd like to clone the project

Use the `git clone` command followed by the url and press enter to create a local copy:

```shell
git clone git@github.com:JessMBrown/CFG_Summer2024_Degree_Group_Project_G5.git
```

---
### 2. Install Dependencies

In order for the code to run smoothly, the necessary packages need to be installed. To do this, run the following command in your terminal to install the required packages:
```bash
pip install -r requirements.txt
```

---
### 3. Obtain the 3 API Tokens

***a)*** **TravelPayouts Hotels Data API**
- Create a TravelPayouts account [here](https://passport.travelpayouts.com/registration?client_id=b0e02fcc-0ab4-4b2c-a164-742762783a4e&response_type=code&redirect_uri=https%3A%2F%2Fapp.travelpayouts.com%2Fapi%2Fauth%2Fcallback&locale=en&parent_marker=direct&ad_source=support_en&ad_content=articles%2B115000343268-Hotels-data-API&tp_referrer=google.com%2F&regpage=mainpage)
- Ignore the select question and scroll to the bottom  to press "I'm here for White Label or API"
- Click "Create a Project in the popup that appears in the bottom right
- Click Mobile app > next > travel business > next > next > select Hotellook under hotels and accomodations > next > view tools
- In the sidebar, press API and it should reveal your API token


***b)*** **Weather API**
- Create a Weather API account [here](https://www.weatherapi.com/signup.aspx)
- You'll be presented with / navigate to [this link](https://www.weatherapi.com/my/) for the API key. 
- For the Swagger navigate [here](https://app.swaggerhub.com/apis-docs/WeatherAPI.com/WeatherAPI/1.0.2), scroll down and select the 'Authorize' button and enter your API key to start using it

***c)*** **OpenTripMaps API**
- Open the OpenTripMap website [here](https://dev.opentripmap.org/)
- Create an account by clicking on 'Register'
- Enter your personal information
- Confirm your email through the email they will send you (check you spam!)
- You can find your API key in 'My Account/Settings'

---
### 4. Database Setup
- Go to `database/destinations_db.sql` as well as `database/customer_details_db.sql` and run the scripts in MySQL workbench
to set up the database 
- Go to `config_oli.py`, replace "Password, please" with your own database password :
   ```shell 
  PASSWORD = "Password, please"
  ```
---
### 5. Putting the tokens in the Config.py
- Enter all the necessary API keys in the right places

---
### 6. Run the code
- Make sure you are in the *main* directory and run the following command:

```shell
python main.py
```
---
## Closing

Thank you for using Journey Genie! We're so glad you did. And a special thanks to the <a href="https://codefirstgirls.com/" target="_blank">Code First Girls</a> team and Olamide and Helen for building our skills and teaching us all we know. But for now,

🚢 Bon voyage!!!

---
## Contributors

[Jessica Brown](https://github.com/JessMBrown) 
| Karen Gonzalez Reginato
| [Joana Grafton](https://github.com/JoanaGraft)
| [Oliwia Polakiewicz](https://github.com/oli-pol)
| [Nadia Rehman](https://github.com/nadiaRehman149)

<div align="right">
<a href="#top">↑</a>
</div>

