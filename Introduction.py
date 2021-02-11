import streamlit as st
import pandas as pd
import plotly.express as px


def app():
    st.title("Dashboard for Men's ODI rankings 🏏")
    st.markdown("**This application is a Streamlit app used to analyze the past 5 years' ranking data of  worldwide "
                " men  cricket players  corresponding to their type .**")
    st.write("\n")
    st.write("Our endeavour has always been to make public data more meaningful not just using numbers & charts,"
             "but also by providing the necessary information & context about issues. In this dashboard, we provide "
             "all the information & "
             "data related to the cricket players in the men's category starting from the year 2016 till the end of 2020.")

    st.subheader('About the Data')

    st.write(
        "The data's source is solely the icc website containing odi rankings of the men players and We will be "
        "concentrating on how the players' rankings varied with date as our data's highest granularity is a "
        "particular day of the month of the year "
    )

    def load_data():
        data = pd.read_csv('odi_ratings.csv')

        return data

    data = load_data()
    # st.write(data)

    # st.subheader("Number  of distinct players by Country")
    st.sidebar.markdown("### Number  of distinct players by Country")
    select = st.sidebar.selectbox('Vizualization type', ['Histogram', 'Pie Chart'], key='1')

    unq_players = data.iloc[:, 1:3].drop_duplicates()

    # countries =unique countries list
    countries = list(unq_players['Nationality'].value_counts().keys())
    player_count = list(unq_players['Nationality'].value_counts())
    players_count = pd.DataFrame({'Country': countries, 'Player_count': player_count})
    # st.write(players_count)

    if not st.sidebar.checkbox('Hide', True):
        st.markdown("### Number of players by country in the last 5 years:")
        if select == "Histogram":
            fig = px.bar(players_count, x='Country', y='Player_count',
                         color='Country',
                         height=500)
            st.plotly_chart(fig)
        else:
            fig = px.pie(players_count,
                         values='Player_count',
                         names='Country')
            st.plotly_chart(fig)


    st.subheader("Compare country team strengths by Type")
    with st.beta_container():
        left_element, right_element = st.beta_columns(2)
        with left_element:
            st.subheader("Country1")
            countries.insert(0, 'Select Country')
            country_select = st.selectbox(label="select country", options=countries)

            if country_select != 'Select Country':
                unq_types = data[['Player_name', 'Nationality', 'Type']]
                country_grp = unq_types.groupby(["Nationality"])
                country_types = pd.DataFrame(
                    {'Type': country_grp.get_group(country_select).drop_duplicates()['Type'].value_counts().keys(),
                     'player_count': country_grp.get_group(country_select).drop_duplicates()[
                         'Type'].value_counts()}).reset_index(drop=True)

                fig2 = px.histogram(country_types, x='Type', y='player_count', width=400, height=500)
                st.plotly_chart(fig2)

        with right_element:
            st.subheader("Country2")
            # st.write("\n")
            # st.write("\n")
            # countries.insert(0, 'Select Country')
            country_select = st.selectbox(label="select country", options=countries,key=1)

            if country_select != 'Select Country':
                unq_types = data[['Player_name', 'Nationality', 'Type']]
                country_grp = unq_types.groupby(["Nationality"])
                country_types = pd.DataFrame(
                    {'Type': country_grp.get_group(country_select).drop_duplicates()['Type'].value_counts().keys(),
                     'player_count': country_grp.get_group(country_select).drop_duplicates()[
                         'Type'].value_counts()}).reset_index(drop=True)

                fig2 = px.histogram(country_types, x='Type', y='player_count', width=400, height=500)
                st.plotly_chart(fig2)

            else:
                print('select a valid country')

    link_html = '<a href="https://dashboards.factly.in">All Dashboards by Factly</a>'

    st.sidebar.markdown(link_html, unsafe_allow_html=True)

    st.sidebar.write("**Contact Us:**")
    st.sidebar.write("Email ID : hi@factly.in", unsafe_allow_html=True)

    st.sidebar.write("**Sources:**")
    st.sidebar.write(
        """[https://www.icc-cricket.com/rankings/mens/player-rankings/odi](https://www.icc-cricket.com/rankings/mens/player-rankings/odi) """)
    st.sidebar.write("")

    st.sidebar.write("**Disclaimer:**")
    st.sidebar.write(
        "Data/Information presented here is being done in good faith."
        " While we have taken all efforts to ensure the accuracy of data/information,"
        " we ask you to refer to the original data/information sources in case of any discrepancy."
    )

    # to remove the hamburger menu and rename the footer
    hide_streamlit_style = """"
    <style>
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        footer:after {
            content:'© Factly Media & Research 2021. All rights reserved';
            visibility: visible;
            display: block;
            position: relative;
            #background-color: red;
            padding: 5px;
            top: 2px;
        }
        </style>"""
