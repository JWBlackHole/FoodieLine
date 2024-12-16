# FoodieLine Introduction
**FoodieLine** is an intelligent chatbot integrated with the **LINE Messaging API**, designed to provide personalized *restaurant recommendations* based on *user interactions* and *location data*.  
Utilizing **Langchain**, FoodieLine connects **Large Language Models** (LLMs), the **Google Maps API**, and a **SQLite** database to provide dynamic, context-aware responses. This powerful combination ensures that users receive relevant and timely dining suggestions, enhancing their culinary experiences through intelligent, real-time interactions.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Implementation](#implementation)
- [Technologies Used](#technologies-used)

## Features
- **Natural Language Conversations**: Engage users in intuitive and meaningful dialogues using **LLMs** integrated via **LangChain**.
- **Location Message Handling**: *Collect* and *store* user location to provide tailored recommendations.
- **Restaurant Recommendations**: Deliver personalized dining suggestions based on user location, preferred cuisine, and search radius using the **Google Maps API**.
- **SQLite Database**: Efficiently manage and retrieve user location with a lightweight **SQLite** database.

## Project Structure
```bash
FoodieLine
├── app
│   ├── main.py
│   └── module
│       ├── google_map.py
│       ├── model.py
│       └── user_locations.py
├── docs
│   └── introduction.md
├── LICENSE.txt
├── locations.db
├── README.md
└── requirements.txt
```

## Implementation
1. **main.py**:
    - **Application Initialization**: Runs the **Flask** app, initializes the **database**.
    - **Chat Bot Webhook Handling**: Manages webhook requests from **LINE**.
    - **Message Processing**:
        - **Text Messages**: Responds to user text inputs using **LLM**.
        - **Location Message**:  Records *user location data* in the **database** for personalized recommendations.

2. **model.py**:
    - **LLM Integration with LangChain**: Uses **LangChain** to bind **Large Language Models (LLMs)** with **custom tools**.
    - **Custom Tools Development**:
        - **Restaurant Recommendations**: Suggests suitable dining options according to user *preferences* and *location*.

3. **google_map.py**:
    - **Google Maps API interactions**:
        - Search restarants according to preferred *location*, *keyword* and *distance*

4. **user_locations.py**:
    - **Database Implementation**:
        - *Add* and *update* user location
        - *Check* if user location is stored in database

### LangChain Integration
#### About LangChain:  
LangChain offers an elegant framework that enables Large Language Models (LLMs) to access and utilize functions or API calls seamlessly. By leveraging the @tool decorator, developers can expose specific functions to the LLM, allowing it to invoke these tools as needed.

Here's an example of how LangChain is utilized within FoodieLine to implement the restaurant recommendation functionality:
```python
from langchain.agents import tool
from app.services.google_maps import get_near_restaurant
from app.services.database_operations import get_user_location

@tool
def recommand_restaurant(user_id: str, radius: int, keyword: str) -> str:
    """Recommend restaurants according to user needs by calling Google Maps API for real-time information.

    Args:
        user_id (str): User ID
        radius (int): The radius in meters to search for restaurants, default is 1000.
        keyword (str): Keyword to filter restaurants based on user preferences.

    Returns:
        str: A list of recommended restaurants if the user's location is stored; otherwise, prompts the user to provide their location.
    """
    
    user_location = get_user_location(user_id)
    
    if user_location["status"] == "Not Found":
        return "Your location is not recorded yet. Please share your location to receive restaurant recommendations."
    else:
        latitude  = user_location["latitude"]
        longitude = user_location["longitude"]
        return get_near_restaurant(latitude, longitude, radius, keyword)

```


## Technologies Used
- **Flask**: Serves as the web framework to handle HTTP requests and manage the application's routing.
- **LINE Messaging API**: Powers the chatbot's communication capabilities within the LINE platform.
- **LangChain**: A platform that can integrates Large Language Models (LLMs) with custom tools, enhancing the chatbot's conversational intelligence and functionality.
- **Google Maps API**: Provides real-time data for restaurant searches based on user-defined criteria.
- **SQLite**: Offers a lightweight and efficient database solution for managing user location data.