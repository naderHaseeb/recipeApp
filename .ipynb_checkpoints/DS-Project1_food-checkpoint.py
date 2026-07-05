import streamlit as st
import pandas as pd
from helper import random_meal
from helper import search_meal
from helper import search_mealbying
from helper import save_meal
from helper import shopping_list
from helper import meal_recommend
from helper import scale_recipe

st.title("CookBook")
st.write("Be Your Best Chef")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #fbfaf4;
        color: #353327;
    }

    section[data-testid="stSidebar"] {
        background-color: #eeeee5;
        border-right: 1px solid #d7d4c8;
    }

    h1, h2, h3 {
        color: #363426;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        background-color: #f0eee6;
        color: #333126;
        border: 1px solid #d4d0c4;
        border-radius: 12px;
    }

    .stButton > button {
        background-color: #e8e4d9;
        color: #363426;
        border: 1px solid #d2cec1;
        border-radius: 12px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #dcd7c9;
        color: #252319;
    }
    </style>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    add_radio = st.radio(
        "Choose Your Service",
        ("Create New Recipe", "Search","View All recipe","View a random recipe", "Shopping List","Meal Recommendation" , "Scale Recipe")   
    )
if add_radio == "Create New Recipe":
    st.subheader(" Add your New Recipe")
    form = st.form("my_form")
    title = form.text_input("Dish Name", "")
    txt_ingredients = form.text_area("Ingredients needed for your dish")
    ptime= form.number_input("Preparation time needed (in minutes)",min_value=0, step=1)
    txt_instructions = form.text_area("How to prepare your dish")
    
    difficulty = form.selectbox(
    "How difficult is it to prepare the dish?",
    ("Easy", "Medium", "Hard"),
)
    category = form.selectbox(
    "When is this meal prepared for?",
    ("Breakfast", "Lunch", "Dinner","Dessert"),
)
    rating= form.slider("Rate your dish",1,5)
    submitted = form.form_submit_button("Add Recipe")
    if submitted:
        save_meal(
            title,
            txt_ingredients,
            ptime,
            txt_instructions,
            difficulty,
            category,
            rating
        )
    st.success("Recipe added successfully!")
    st.write("### Your added recipe:")
    st.write("**Dish Name:**", title)
    st.write("**Ingredients:**", txt_ingredients)
    st.write("**Preparation Time:**", ptime, "minutes")
    st.write("**Instructions:**", txt_instructions)
    st.write("**Difficulty:**", difficulty)
    st.write("**Category:**", category)
    st.write("**Rating:**", rating)

elif add_radio == "Search":
    st.subheader(" Search Recipes")
    tosearch = st.text_input("Search for the recipe:")
    st.dataframe(search_mealbying(tosearch))
    

elif add_radio == "View All recipe":
    df = pd.read_csv("meals_recipes.csv")
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    st.subheader(" View All Recipes")
    add_selectbox = st.selectbox(
        "What meal are you planning to prepare?",
        ("Breakfast", "Lunch", "Dinner","Dessert")
    )
    filtered_df = df[df["category"] == add_selectbox]
    st.dataframe(filtered_df)
    #df=pd.read_csv('meals_recipes.csv')
    #df[['name','prep_time']]
    
elif add_radio == "View a random recipe":
    st.subheader(" Random Recipe")
    if st.button("give me a random meal"):
        st.dataframe(random_meal())
        st.balloons()


elif add_radio == "Shopping List":
    st.subheader("Generate Shopping List")
    toshop = st.text_input("Search for the recipe:")
    if st.button("Generate"):
        st.dataframe(shopping_list(toshop))
        st.balloons()
        st.balloons()
        st.balloons()
        st.balloons()
        st.balloons()
        st.balloons()
        st.balloons()
        st.balloons()
        st.balloons()
        st.balloons()
        st.balloons()
        st.balloons()






if "key" not in st.session_state:
    st.session_state["key"] = 0

if add_radio == "Meal Recommendation":
    st.subheader("Meal Recommendation")
    df = pd.read_csv("meals_recipes.csv")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    if st.button("Recommend me a meal"):
        recommended_meal, next_index = meal_recommend(df, st.session_state['key'])
        if recommended_meal is not None:
            st.session_state['key'] = next_index
            st.write(recommended_meal)
        else:
            st.error("No meals found in the dataset.")


elif add_radio == "Scale Recipe":
    st.subheader("Scale Ingredient Quantities")

    df = pd.read_csv("meals_recipes.csv")
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    meal_names = df["name"].tolist()

    selected_meal = st.selectbox("Choose a recipe:", meal_names)

    desired_persons = st.number_input(
        "How many persons/servings do you want?",
        min_value=1,
        value=2
    )

    if st.button("Scale Recipe"):
        scaled_ingredients = scale_recipe(selected_meal, desired_persons)

        st.write("Scaled ingredients:")

        for ingredient in scaled_ingredients:
            st.write("- " + ingredient)