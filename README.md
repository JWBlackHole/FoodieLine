# FoodieLine: An LLM-Based Chatbot with Restaurant Recommendations

**FoodieLine** is a *dynamic* and *intelligent* chatbot built on the **LINE Messaging API**, designed to enhance your dining experiences through personalized restaurant recommendations. Leveraging advanced language models and seamless integration with **Google Maps API**, FoodieLine not only engages in meaningful text conversations but also utilizes your location data to suggest the best eateries tailored to your preferences.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#License)

## Features
- **Text Message Handling**: Engage in natural conversations with users using a **LLM**.
- **Location Message Handling**: Collect and store user location data to provide tailored recommendations.
- **Restaurant Recommendations**: Deliver personalized dining suggestions based on user location, preferred cuisine, and search radius using the **Google Maps API**.
- **SQLite Database**: Efficiently manage and retrieve user location data with a lightweight **SQLite** database.

## Installation
1. **Clone the Repository**
```bash
git clone https://github.com/JWBlackHole/FooddieLine.git
cd FoodieLine
```
2. **Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Configuration
To run this project, we need **LINE Messaging API**, **OpenAI API** and **Google Map API**, please ensure all api keys are availabe in your **system environment variables**.
```bash
# LINE Messaging API credentials
export LINE_CHANNEL_ACCESS_TOKEN="your_line_channel_access_token"
export LINE_CHANNEL_SECRET="your_line_channel_secret"

# OpenAI API Key
export OPENAI_API_KEY="your_openai_api_key"

# Google Maps API Key
export GOOGLE_MAP_API_KEY="your_google_maps_api_key"
```

## Usage
We now have a powerful LLM-based chatbot that goes beyond just text messaging. With its integration of the Google Maps API, you can ask it for restaurant recommendations in various ways.

Here are three examples, but the possibilities are endless: 
1. I’m hungry now. Could you recommend some restaurants within a 5-minute walking distance?

2. If I want to try some Indian dishes, what would you recommend me to eat?

3. Today, I’d like to try some pasta or pizza. Which restaurant would you recommend?

## License
This project is licensed under the [MIT License](https://mit-license.org/).

<hr>
Developed with ❤️ by JWBlackHole