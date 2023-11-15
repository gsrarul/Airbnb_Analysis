import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

data = pd.read_csv(r"C:\Users\arulkumar\Desktop\MLGuvi\Airbnb_Analysis\airbnb.csv")

st.set_page_config(layout="wide", page_title="airbnb-analysis")

st.markdown("<h1 style='text-align: center; color: red;'>Airbnb Analysis</h1>", unsafe_allow_html=True)
st.divider()

col1,col2 = st.columns((1,4))

with col1:
    option1 = st.selectbox(("Select a country"),("All","Australia","Brazil","Canada","China","Portugal","Spain","Turkey","United States"))
    if option1 != "All":
        option2 = st.selectbox(("Select an option"),("Total rooms booked","Price range across seasons","Most reviewed & rated hosts","Availability & demanded hosts across seasons"))
with col2:
    if option1 == "All":
        fig = plt.figure(figsize=(10,6))
        sns.countplot(data=data,x="country")
        plt.title("Total number of rooms booked in each country")
        st.pyplot(fig)

        fig = plt.figure(figsize=(10,6))
        sns.countplot(data=data,x="room_type", hue="country")
        plt.title("Number of rooms booked in each category across countries")
        st.pyplot(fig)

        fig = plt.figure(figsize=(15,10))
        sns.barplot(data=data, x="room_type", y="price",hue="country", palette="pastel")
        plt.title("Price range across countries")
        st.pyplot(fig)
    else:
        df = data.query(f'country == "{option1}"')
        cities = df['city'].unique()
        if option2 == "Total rooms booked":
            fig = plt.figure(figsize=(10,6))
            sns.countplot(data=df, x="room_type", hue="city", palette="Set2")
            plt.title(f"{option1} : Number of rooms as per category booked in each city")
            st.pyplot(fig)

        elif option2 == "Price range across seasons":
            fig = plt.figure(figsize=(10,6))
            sns.lineplot(data=df,x="review_date", y="price", hue="city")
            plt.title(f"{option1} : Price range in each month across cities")
            plt.xlabel("Month")
            st.pyplot(fig)

        elif option2 == "Most reviewed & rated hosts":
            st.subheader("Most reviewed and rated hosts in each city")
            for city in cities:
                df1 = df.query(f'city == "{city}" & rating >= 80.0').sort_values(by=['number_of_reviews'], ascending=False)        
                fig = plt.figure(figsize=(10,6))
                sns.barplot(data=df1.head(),x="host_name", y="number_of_reviews")
                plt.title(f"Country: {option1} City: {city}")
                st.pyplot(fig)
        
        elif option2 == "Availability & demanded hosts across seasons":
            st.subheader("Availability of each hosts in cities-month wise")
            for city in cities:
                df1 = df.query(f'city == "{city}" & rating >= 80.0 & availability_365 >= availability_365.mean()').sort_values(by=['number_of_reviews'], ascending=False)        
                st.caption("These hosts are most reviewed and rated as well")
                fig = plt.figure(figsize=(10,6))
                sns.barplot(data=df1.head(),x="review_date", y="availability_365", hue="host_name")
                plt.title(f"Country: {option1} City: {city}")
                plt.xlabel("Month")
                st.pyplot(fig)

            st.subheader("Hosts which are in demand in cities-month wise")
            for city in cities:
                df1 = df.query(f'city == "{city}" & rating >= 80.0 & availability_365 < availability_365.mean()').sort_values(by=['number_of_reviews'], ascending=False)        
                st.caption("These hosts are most reviewed and rated as well")
                fig = plt.figure(figsize=(10,6))
                sns.barplot(data=df1.head(),x="review_date", y="availability_365", hue="host_name")
                plt.title(f"Country: {option1} City: {city}")
                plt.xlabel("Month")
                st.pyplot(fig)