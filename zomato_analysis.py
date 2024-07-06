# import librarys
import pandas as pd
import plotly.express as px
import streamlit as st

df1 = pd.read_csv("zomato.csv")
df2 = pd.read_excel("Country-Code.xlsx")

zomato_df = pd.merge(df1, df2)

# Convert the currency to INR
zomato_df['Currency'] = zomato_df['Currency'].replace({'Botswana Pula(P)': 'INR',
                                                             'Brazilian Real(R$)': 'INR',
                                                             'Dollar($)': 'INR',
                                                             'Emirati Dirham(AED)': 'INR',
                                                             'Indian Rupee(Rs.)': 'INR',
                                                             'Indonesian Rupiah(IDR)': 'INR',
                                                             'NewZealand($)': 'INR',
                                                             'Pounds Sterling(£)': 'INR',
                                                             'Rand(R)': 'INR',
                                                             'Sri Lankan Rupee(LKR)': 'INR',
                                                             'Turkish Lira(TL)': 'INR',
                                                             'US Dollar($)': 'INR',
                                                             'Vietnamese Dong(₫)': 'INR',
                                                             'Botswana Pula(P)': 'INR',
                                                             'Dollar($)': 'INR'})
zomato_df.to_csv('zomato_analysis.csv', index=False)

# Load the dataset
zomato_df = pd.read_csv('zomato_analysis.csv')

#streamlit part
st.set_page_config(layout="wide")
st.title(":red[Zomato Data Analysis and Visualization]")

if 'Country' in zomato_df.columns:
    # Create a dropdown to choose the country
    countries = zomato_df['Country'].unique()
    selected_country = st.selectbox('Select a country', countries)

    # Filter the dataset by country
    df_country = zomato_df[zomato_df['Country'] == selected_country]

    # Create a dropdown to choose the chart type
    chart_type = st.selectbox('Select a chart type', ['Bar Chart', 'Pie Chart','Line chart','scatter plot'])

    # Create the chart based on the selected chart type
    if chart_type == 'Bar Chart':
    # Create a bar chart of the top 5 cuisines
        top_cuisines = df_country['Cuisines'].value_counts().nlargest(5)
        fig = px.bar(x=top_cuisines.index, y=top_cuisines.values,
                    title=f'Top 5 Cuisines in {selected_country}',
                    color=top_cuisines.index,  # This line assigns different colors to each bar
                    labels={'x': 'Cuisine', 'y': 'Cuisines Rating'})  # Adds axis labels for clarity
        
    elif chart_type == 'Pie Chart':
    # Create a pie chart of the distribution of ratings
        fig = px.pie(df_country, names='Aggregate rating', title=f'Distribution of Ratings in {selected_country}')

    elif chart_type == 'Line chart':
    # Create a DataFrame for the top 10 cuisines and their average cost for two
        top_10_cuisines = df_country['Cuisines'].value_counts().nlargest(10).index
        df_top_10_cuisines = df_country[df_country['Cuisines'].isin(top_10_cuisines)]
        avg_cost_per_cuisine = df_top_10_cuisines.groupby('Cuisines')['Average Cost for two'].mean().reset_index()
        # Create a line plot for the top 10 cuisines and their average cost for two
        fig = px.line(avg_cost_per_cuisine, x='Cuisines', y='Average Cost for two',
                    title=f'Top 10 Cuisines and Their Average Cost for Two in {selected_country}',
                    color_discrete_sequence=['#2CA02C'],height=600)
        
    elif chart_type == 'scatter plot':
       # Create a scatter plot of aggregate rating vs. votes
        fig = px.scatter(df_country, x='Votes', y='Aggregate rating',
                        title=f'Relationship Between Rating and Votes in {selected_country}',
                        color='City', size='Average Cost for two', hover_name='Restaurant Name',
                        hover_data=['Cuisines'])

    # Show the chart
    st.plotly_chart(fig)

    # Create a section for further analysis
    st.header(':blue[Further Analysis]')

    # Create a dropdown to choose the city
    cities = df_country['City'].unique()
    selected_city = st.selectbox('Select a city', cities)
    # Filter the dataset by city
    df_city = df_country[df_country['City'] == selected_city]

    # Create a dropdown to choose the cuisine
    cuisines = df_city['Cuisines'].unique()
    selected_cuisine = st.selectbox('Select a cuisine', cuisines)

    # Filter the dataset by cuisine
    df_cuisine = df_city[df_city['Cuisines'] == selected_cuisine]
    st.dataframe(df_cuisine)
