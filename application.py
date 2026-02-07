import datetime
from logging import config
from dotenv import load_dotenv  
import os
import requests

from functools import partial

from google import genai
from google.genai import types  

load_dotenv()

os.environ["GOOGLE_API_KEY"] = "AIzaSyCRQPLhvqPvfYaD5lHOaje0VVQew8LZ76k"
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key: 
    raise ValueError("API key Not Found")    

client = genai.Client(api_key = api_key)  

# Function To Get Weather of a City :
def get_weather(city:str):
    """Fetches current weather for a given city using Google GenAI. 
       By taking the argument city as input which is of type string and 
       returns the weather details as a string. """
          
    try:
        api_key_we = "1e763287ab379ad10676c727165dc179"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key_we}"  
        response = requests.get(url)    
        return response.json()  
    except requests.exceptions.RequestException as e:
        return {"Error": str(e)}
    

# Gemini code to use the function to get the detail of the city.
def temperature_of_city(city):
    system_instruction = ''' 
        You are given weather data in JSON format from the OpenWeather API.
        Your job is to convert it into a clear, human-friendly weather update.  
        
        Guidelines:
        1. Always mention the city and country.
        2. Convert temperature from Kelvin to Celsius (°C), rounded to 1 decimal.
        3. Include: current temperature, feels-like temperature, main weather description,
            humidity, wind speed, and sunrise/sunset times (converted from UNIX timestamp).
        4. Use natural, conversational language.
        5. Based on the current conditions, suggest what the person should carry or wear.
            - If rain/clouds: suggest umbrella/raincoat.
            - If very hot (>30°C): suggest light cotton clothes, sunglasses, stay hydrated.
            - If cold (<15°C): suggest warm clothes, jacket.
            - If windy: suggest windbreaker, secure loose items.
            - If humid: suggest breathable clothes, water bottle.
        6. If any field is missing, gracefully ignore it.
        '''
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"Generate a clear,friendly weather report with temperature in Celsius in °C, humidity, wind, sunrise/sunset for the {city} and practical suggestions on what to wear or carry.",
        config=types.GenerateContentConfig(system_instruction = system_instruction, tools=[get_weather])
    )
    return (response.candidates[0].content.parts[0].text)   


# Function To Get News Based on Interest :
def get_news(topic:str):
    """Fetches latest news headline using Google GenAI. 
       By taking the argument topic(technology, sports, health) as input which is of type string and 
       returns the news details as a string. """
          
    try:
        api_key_news = "72ffc4b0-55d1-45df-9f9c-067be738a836"
        url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key_news}&pageSize=5&sortBy=publishedAt" 
        response = requests.get(url)    
        return response.json().get("articles", []) 
    except requests.exceptions.RequestException as e:
        return {"Error": str(e)}

# Function To Summarize News Article :
def news_summarizer(url):
    """Summarizes the news article from the given URL using Google GenAI. 
       By taking the argument url as input which is of type string and 
       returns the summarized news details as a string. """
          
    system_instruction = ''' 
        You are given a news article URL.
        Your job is to read the article and provide a concise summary.
        
        Guidelines:
        1. Summarize the main points of the article in 3-4 sentences.
        2. Use clear and simple language.
        3. Avoid personal opinions; stick to facts from the article.
        4. If the article cannot be accessed, respond with "Article not accessible."
        '''
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"Summarize the news article from this URL: {url}, don't add sentences like from where the article is , in this article etc .Just give clear and crisp summary.", 
        config=types.GenerateContentConfig(system_instruction = system_instruction, tools=[get_news])
    )
    return (response.candidates[0].content.parts[0].text)

# Function to get forecast of entire day of a city and place to visit in the city :

def get_forecasted_weather(city:str):
    """Fetches forecasted weather and the tourist place for a given city using Google GenAI. 
       By taking the argument city as input which is of type string.
    """
          
    try:
        grounding_tool = types.Tool(
            google_search = types.GoogleSearch()
        )
        
        
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents = f"""Provide a detailed weather for {city} on {datetime.date.today()}.Then also list the top recommended place to visit in the {city}on the same date.
            Formate the response clearly so it can be used by  another planning agent.""",
            config = types.GenerateContentConfig(
                     tools=[grounding_tool]) 
        )
            
        
        return (response.candidates[0].content.parts[0].text)       

    except Exception as e:
      return {"Error": str(e)}
    
    
# Function to find Loacl Events based on city and date :   
def find_local_events(city:str):
    """Fetches local events for a given city using API. 
       By taking the argument city as input which is of type string.
    """
          
    try:
        api_key_events = "d876c17f6728ee40fd525b9a69df3a8ec029313f4cad2292e8988dbd6f353cba"
        url = f"https://serpapi.com/search.json?engine=google_events&q=Events in {city}&api_key={api_key_events}"
        response = requests.get(url)    
        return response.json()    # Because all the data is in the json format  
    except requests.exceptions.RequestException as e:
        return {"Error": str(e)}
    
# FUNCTION TO GET SMARTER PLANNER:
def smarter_planner(city:str):
    """Generates a smarter daily schedule for a given city and date using Google GenAI. 
       By taking the argument city and date as input which is of type string.
    """
    # default to today's date when none provided
    date = datetime.date.today().isoformat()
    
    weather_forecast = get_forecasted_weather(city)
    events = find_local_events(city)
        
    prompt  = f"""You are a smart travel and event planner assistant.
    Your job is to create a personalized day itinerary for the user in a given {city} on {date}.

    You are given:

    Weather forecast for the {city} (with temperature, rain chances, humidity, etc.).

    Upcoming events in the {city} (with title, date, time, venue, description, and link).

    List of recommended places to visit in the {city}.


    Instructions:

    Always use weather conditions to decide between indoor and outdoor activities.

    Organize the plan chronologically (Morning → Afternoon → Evening).

    Mix tourist attractions + events + leisure breaks so the day feels balanced.

    When recommending events, check if the event timing fits the user’s availability.

    Always include event links when mentioning them.

    Suggest lunch/dinner breaks with general recommendations (local cuisine or malls).

    If multiple good options exist (e.g., 2 events at the same time), present them as choices.

    Keep the tone friendly and actionable, like a local guide making the plan.
    Always give the events happening in the city.

    Input Example:

    Weather Forecast:
    On Saturday, August 23, 2025, Chandigarh is expected to be cloudy with a maximum temperature ranging from 30°C to 34°C (86°F to 93°F) and 
    a minimum temperature between 25°C and 26°C (77°F to 79°F). There is a 25% to 65% chance of rain during the day and a 40% to 45% chance of rain at night.
    The humidity is anticipated to be around 82% to 86%.

    Places to Visit:

    Rock Garden

    Sukhna Lake

    Rose Garden

    Elante Mall

    Events:

    🎤 Halki Halki Fati by Vikas Kush Sharma
    📅 Sat, Aug 23, 5:30 – 8:00 PM
    📍 The Laugh Club, Chandigarh
    🔗 https://allevents.in/chandigarh/halki-halki-fati-by-vikas-kush-sharma/3900027700476104

    🎤 Founders Meet | Chandigarh
    📅 Sat, Aug 23, 4 – 7 PM
    📍 Innovation Mission Punjab
    🔗 https://www.district.in/events/founders-meet-chandigarh-august-23-aug23-2025-buy-tickets

    🎤 Saturday Comedy Evening At Tagore Theatre
    📅 Sat, Aug 23, 7 – 9:30 PM
    📍 Tagore Theatre, Chandigarh
    🔗 https://www.shoutlo.com/events/saturday-comedy-evening-chandigarh

    User’s Available Time:
    9:00 AM – 9:00 PM

    Output Example:

    ✨ Your Personalized Day Plan for Chandigarh (Aug 23, 2025):

    🌤️ Morning (9:00 AM – 12:00 PM)

    Begin your day at Sukhna Lake with a peaceful lakeside walk (perfect in cloudy weather).

    Visit the artistic Rock Garden, which is outdoors but comfortable in today’s mild temperature.

    🍴 Lunch (12:30 PM – 2:00 PM)

    Try Chandigarh’s local food at Pal Dhaba, or if it rains, head to Elante Mall for indoor dining.

    🎭 Afternoon (2:30 PM – 5:30 PM)

    If you’re into startups and networking, attend Founders Meet | Chandigarh (4–7 PM) 👉 Event Link
    .

    Otherwise, enjoy a stroll at the Rose Garden.

    🎤 Evening Entertainment (6:00 PM – 9:00 PM)

    Comedy lovers can catch Halki Halki Fati by Vikas Kush Sharma (5:30–8:00 PM) 👉 Event Link
    .

    Alternatively, laugh your heart out at Saturday Comedy Evening At Tagore Theatre (7–9:30 PM) 👉 Event Link
    .

    ✅ This plan balances sightseeing, food, and entertainment while considering today’s cloudy weather.
    """      
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents = prompt, 
        config = types.GenerateContentConfig(
            tools=[find_local_events,  partial(get_forecasted_weather, city)]
            
        )
    )
    
    return (response.candidates[0].content.parts[0].text)
