import streamlit
import pandas
import requests
import snowflake.connector
from  urllib.error import URLError

#import streamlit
streamlit.title("My Mom's New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣omega 3 & Blueberry Oatmeal')
streamlit.text('🥗kale, Spinach & Rocket Smoothie')
streamlit.text('🍔🥚Hard-Boiled Free Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pands
my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#create he repeatable code block(called a function)
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized
#New Section to Display fruityvice api responce
streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
   else:
       back_from_function = get_fruityvice_data(fruit_choice)
       streamlit.dataframe(back_from_function)
      
      
except URLError as e:
  streamlit.error()
    #streamlit.write('The user entered ', fruit_choice)
#streamlit.stop()

#import snowflake.connector

streamlit.header("Visit our Fruit list - Add your Favorites!")
#Snowflake related function
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
        my_cur.execute('select * from fruit_load_list')
        return my_cur.fetchall()
#Add  button to load the fruit
if streamlit.button('Get Fruit load list!'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   
#Allow the end user to ad a fruit to the list
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values('"+ new_fruit+"')")
      return "Thanks For Adding "+ new_fruit
add_my_fruit = streamlit.text_input('What Fruit Would You Like To Add?')
if streamlit.button('Add a fruit to the list:'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = insert_row_snowflake(add_my_fruit)
   streamlit.text(back_from_function)
   
streamlit.stop() 



















