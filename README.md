<a name="top"></a>
![logo.png](README_media/logo.png)


---
### Your travel wish is our command 🪄
<a href="#introduction">Introduction</a> | <a href="#main-features">Main Features</a> | <a href="#clone-the-repository">Clone the Repository</a> | <a href="#install-dependencies">Install Dependencies</a> | <a href="#obtain-the-3-api-tokens">Obtain the 3 API Tokens</a> | <a href="#database-setup">Database Setup</a> | <a href="#putting-the-tokens-in-the-configpy">Putting the tokens in the Config.py</a> | <a href="#run-the-code">Run the Code</a> | <a href="#closing">Closing</a> | <a href="#contributors">Contributors</a> | <a href="#development-stack">Development Stack</a> |
<a href="#license">License</a>  

## Introduction

<p>
<img src="README_media/holiday.gif" alt="Holiday GIF" align="right" width="100" height="90" style="margin-left: 20px;">
Welcome to Journey Genie, our console-based application that helps you plan your perfect vacation! Whether you're looking for a luxury experience, a business stay, or a fun family holiday, we've got you covered. Journey Genie eliminates the need to spend hours browsing tonnes of sites as it's all done in one place. Sit back, relax, and let the magic unfold...
</p>

---
<a name="main-components"></a>**Main Features:**

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

<u><a name="clone-the-repository"></a>
### 1. Clone the repository

In your terminal, open the working directory where you'd like to clone the project

Use the `git clone` command followed by the url and press enter to create a local copy:

```shell
git clone git@github.com:JessMBrown/CFG_Summer2024_Degree_Group_Project_G5.git
```

---
<a name="install-dependencies"></a>
### 2. Install Dependencies

In order for the code to run smoothly, the necessary packages need to be installed. To do this, run the following command in your terminal to install the required packages:
```bash
pip install -r requirements.txt
```

---
<a name="obtain-the-3-api-tokens"></a>
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
<a name="database-setup"></a>
### 4. Database Setup
- Go to `database/destinations_db.sql` as well as `database/customer_details_db.sql` and run the scripts in MySQL workbench
to set up the database 
- Go to `config_oli.py`, replace "Password, please" with your own database password :
   ```shell 
  PASSWORD = "Password, please"
  ```
---
<a name="putting-the-tokens-in-the-configpy"></a>
### 5. Putting the tokens in the Config.py
- Enter all the necessary API keys in the right places

---
<a name="run-the-code"></a>
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
| [Joana Grafton](https://github.com/JoanaGraft)
| [Oliwia Polakiewicz](https://github.com/oli-pol)
| [Nadia Rehman](https://github.com/nadiaRehman149)
| Karen Gonzalez Reginato

---
<a name="development-stack"></a>**Development Stack**

[<img height="32" width="32" alt="Python Logo" src="https://cdn.worldvectorlogo.com/logos/python-5.svg"/>]()
[<img height="32" width="32" alt="MySQL" src="https://cdn.worldvectorlogo.com/logos/mysql-2.svg"/>]()
[<img height="32" width="32" alt="PyCharm" src="https://cdn.worldvectorlogo.com/logos/pycharm.svg"/>]()
[<img height="32" width="32" alt="Jira" src="https://cdn.worldvectorlogo.com/logos/jira-1.svg"/>]()
[<img height="32" width="32" alt="Slack" src="https://cdn.worldvectorlogo.com/logos/slack-new-logo.svg"/>]()
[<img height="32" width="32" alt="Google Meet" src="https://cdn.worldvectorlogo.com/logos/google-meet-icon-2020-.svg"/>]()

---
<a name="license"></a>
## License

This project is licensed under the [MIT License.](https://github.com/milliedavidson/CFGProject/blob/main/LICENSE)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

```text
Copyright 2024 Journey Genie

Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the “Software”), to deal in the Software without
restriction, including without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

--- 

<div align="right">
<a href="#top">Back to Top ↑</a>
</div>
