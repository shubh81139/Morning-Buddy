import streamlit as st
from datetime import date
import random
from application import temperature_of_city , get_news, news_summarizer , smarter_planner

# --- Page Configuration ---
st.set_page_config(
    page_title="Your Morning Buddy", 
    page_icon="☀️",
    layout="centered"
)

# --- Helper Functions ---
def get_random_quote():
    """Returns a random morning quote."""
    quotes = [
        "When you open your eyes in the morning, remember how powerful it is to have another chance to live, to learn, to grow, to love.",
        "Each morning you wake is proof that life still believes in you and your journey.",
        "When the sun rises, let your worries set and your hopes rise higher.",
        "Every morning is a gentle reminder that you are stronger than yesterday’s struggles.",
        "As you step into the morning light, carry gratitude in your heart and courage in your mind.",
        "Waking up each day is life’s way of telling you that your purpose is not yet complete.",
        "Let the quiet of the morning remind you of the peace you can create within yourself.",
        "Each sunrise brings a new opportunity to become a better version of who you were yesterday.",
        "In the morning, take a deep breath and appreciate the simple gift of being alive.",
        "When you rise in the morning, rise with faith that today holds something beautiful for you.",
        "Every new morning is a blank page waiting for your story to unfold.",
        "As the day begins, remind yourself that you have the strength to handle whatever comes.",
        "Morning light teaches us that darkness is temporary and hope always returns.",
        "Start your morning with positive thoughts, and watch how your day transforms.",
        "Each morning is life’s invitation to move forward with renewed energy.",
        "When you wake up, choose peace over pressure and gratitude over complaints.",
        "The morning breeze carries new beginnings for those who are willing to embrace them.",
        "With every sunrise, remember that you are gifted another chance to chase your dreams.",
        "Morning is a time to reflect on how precious life truly is.",
        "When you arise, fill your heart with hope and your mind with purpose.",
        "Every morning gives you a chance to leave yesterday’s worries behind.",
        "As you welcome the new day, remind yourself of your endless possibilities.",
        "The beauty of the morning lies in its promise of a fresh start.",
        "When you open your eyes to the day, open your heart to new opportunities.",
        "Each morning reminds us that resilience is rewarded with another beginning.",
        "Start the day believing that something wonderful is about to happen.",
        "Morning moments of silence often bring the loudest clarity.",
        "When the sun rises, let your motivation rise with it.",
        "Every new day begins with the courage to step out of bed.",
        "Morning teaches us patience, as every great day starts slowly.",
        "As you greet the morning, greet yourself with kindness and encouragement.",
        "When you wake up, remember how far you have already come.",
        "Morning is a reminder that life always offers second chances.",
        "Each sunrise paints the sky with hope for those who look up.",
        "When you arise, take a moment to appreciate the gift of time.",
        "The calm of the morning prepares the mind for the challenges ahead.",
        "With every new dawn, life whispers that you are capable of greatness.",
        "Morning is the perfect time to reset your thoughts and refresh your goals.",
        "When you open your eyes, open them to gratitude and positivity.",
        "Each morning is a small miracle that deserves a thankful heart.",
        "Start your day with a smile, and let it guide you through the hours ahead.",
        "When you rise, rise with determination to make the day meaningful.",
        "The morning sun reminds us that light always follows darkness.",
        "Each day begins with the simple but powerful act of waking up.",
        "Morning is an opportunity to align your heart with your intentions.",
        "When you wake, remind yourself that today is a gift, not a guarantee.",
        "The freshness of the morning carries the promise of new achievements.",
        "As you step into the day, carry hope like a guiding light.",
        "Every sunrise is life’s way of saying, keep going.",
        "When you arise in the morning, remember how fortunate you are to experience another day to breathe, to think, to feel, and to love.",
    ]
    return random.choice(quotes)

def get_random_image():
    """Returns a random morning-themed image URL."""
    image_urls = [
        "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8",
        "https://images.unsplash.com/photo-1500382017468-9049fed747ef",
        "https://images.unsplash.com/photo-1494548162494-384bba4ab999",
        "https://images.unsplash.com/photo-1520038410233-7141be7e6f97",
        "https://images.unsplash.com/photo-1441974231531-c6227db76b6e",
        "https://images.unsplash.com/photo-1508575478422-c401c540a858"
    ]
    return random.choice(image_urls)


# --- Page Definitions ---

def home_page():
    """Displays the home page with a quote and image."""
    st.title("☀️ Your Morning Buddy")
    st.markdown("---")
    st.subheader("A Thought for Your Day")
    st.info(f'"{get_random_quote()}"')
    st.image(get_random_image(), caption="A beautiful morning to start your day", use_container_width=True)
    st.markdown("---")
    st.write("Use the sidebar on the left to get your daily updates!")

def weather_news_page():
    """This page displays the weather and news by city."""
    st.header("Get Weather of the city")
    city = st.text_input("Enter your city name:")

    if st.button("Fetch Information"):
        if city:
            temperature_output= temperature_of_city(city)
            st.subheader(f"Weather Info: {temperature_output}")
            st.success("Weather fetched successfully ✅")
        else:
            st.error("Please enter a valid city name.")

def interest_news_page():
    """Displays the page for getting news by interest."""
    st.header("Get News Based on Your Interests")
    interest = st.text_input("Enter your area of interest (e.g., Technology, Sports, Health):", "Technology")

    if st.button("Fetch News"):
        if interest:
            articles = get_news(interest)
            title = []
            url = []
            image_url = []
            for i in articles:
                title.append(i["title"])
                url.append(i["url"])
                image_url.append(i["urlToImage"])

            if not articles:
                st.error("No news found.")
            col1, col2,col3,col4, col5 = st.columns(5)
            with col1:
                st.subheader(title[0])
                st.markdown("-----")
                st.image(image_url[0])
                st.markdown("-----")
                st.write("Read full article Here",url[0])
                st.markdown("-----")
                st.write(news_summarizer(url[0]))

            with col2:
                st.subheader(title[1])
                st.markdown("-----")
                st.image(image_url[1])
                st.markdown("-----")
                st.write("Read full article Here", url[1])
                st.markdown("-----")
                st.write(news_summarizer(url[1]))

            with col3:
                st.subheader(title[2])
                st.markdown("-----")
                st.image(image_url[2])
                st.markdown("-----")
                st.write("Read full article Here", url[2])
                st.markdown("-----")
                st.write(news_summarizer(url[2]))

            with col4:
                st.subheader(title[3])
                st.markdown("-----")
                st.image(image_url[3])
                st.markdown("-----")
                st.write("Read full article Here", url[3])
                st.markdown("-----")
                st.write(news_summarizer(url[3]))

            with col5:
                st.subheader(title[4])
                st.markdown("-----")
                st.image(image_url[4])
                st.markdown("-----")
                st.write("Read full article Here", url[4])
                st.markdown("-----")
                st.write(news_summarizer(url[4]))

        else:
            st.error("Please enter an area of interest.")


def schedule_page():
    """Displays the page for viewing the day's schedule."""
    st.header("Your Smart Planner ")
    city = st.text_input("Enter your city name:")
    print(city)
    if st.button("Let's Plan"):
        if city:
            smart_plan = smarter_planner(city)
            st.subheader(smart_plan)
            st.success("Have a Happy day.")
        else:
            st.error("Please enter a city name.")


# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
st.sidebar.markdown("---")
page_option = st.sidebar.radio("Choose a page:", ("Home", "Get Weather of your City", "News by Interest","Smart Planner"))
st.sidebar.markdown("---")


# --- Page Routing ---
if page_option == "Home":
    home_page()
elif page_option == "Get Weather of your City":
    weather_news_page()
elif page_option == "News by Interest":
    interest_news_page()
elif page_option =="Smart Planner":
    schedule_page()
