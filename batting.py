import streamlit as st
import pandas as pd
from streamlit_metrics import metric, metric_row
import plotly.express as px
import datetime
import numpy as np
import copy


def app():
    st.title("Batsmen statistics")
    st.write(
        "#### This page provides complete data on batsmen. You can filter by country,date  and take a look at his ranking curve.")
    st.write("\n")

    DATA_URL = (r"C:\Users\mani ratnam\Desktop\batsmen_data.csv")

    def load_data():
        bat_data = pd.read_csv(DATA_URL)
        return bat_data

    bat_data = load_data()

    dates = bat_data['Date'].tolist()

    st.sidebar.markdown("### Show time  slider")
    if not st.sidebar.checkbox('Hide', True):

        with st.beta_container():
            # slider for selecting month and year interval
            start_month_year, end_month_year = st.select_slider(
                label="Select Time Period",
                options=dates,
                value=(dates[0], dates[-1]),
                format_func=lambda x: pd.to_datetime(x).strftime("%Y,%b")
            )

        if start_month_year and end_month_year:
            bat_data = bat_data.loc[
                (bat_data["Date"] >= start_month_year)
                & (bat_data["Date"] <= end_month_year)
                ]

    with st.beta_container():
        left_element, right_element = st.beta_columns(2)
        # players = unique players list with 0 as select option
        players = bat_data["Player_name"].unique().tolist()
        players.insert(0, 'Select Player')

        with left_element:

            filtered_player = st.selectbox("Select Player name", players)

        if filtered_player != 'Select Player':
            player_data = bat_data[bat_data['Player_name'] == filtered_player]
            st.write("**SELECTED PLAYER:  {}**".format(filtered_player.upper()))

        # else:
        #     pass
        st.write('\n')

        with  right_element:
            if filtered_player in players[1:]:

                metric("COUNTRY", player_data['Nationality'].tolist()[0])

            else:
                metric("please select player first", 'COUNTRY')

        st.write("**RATING  METRICS 🔢 :**")
        if filtered_player in players[1:]:
            metric_row(
                {"Avg.Rating": "{:.3f}".format(player_data['Rating'].mean()),
                 "Best Rating": player_data['Best_rating'].tolist()[0],
                 "Rating standard deviation": "{:.3f}".format(player_data['Rating'].std())

                 }
            )

        st.write("\n")
        st.write("\n")

        with st.beta_container():


            # col1, col2 = st.beta_columns(2)
            # with col1:
            st.write("\n")
            st.write("**RATINGS Vs DATE 📈**")

            if filtered_player in players[1:]:
                player_data = bat_data[bat_data['Player_name'] == filtered_player]
                fig = px.line(player_data, x='Date', y='Rating',
                              title=player_data['Player_name'].tolist()[0].upper(),
                              height=600, width=900)
                fig.add_scatter(x=player_data['Date'], y=player_data['Rating'])
                # fig.update_yaxes(autorange="reversed")
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)
                fig.update_layout(
                    font_family="Courier New",
                    font_color="green",
                    # title_font_family="Times New Roman",
                    title_font_color="black",
                    legend_title_font_color="black"
                )

                st.plotly_chart(fig)

        with st.beta_container():
            st.write("\n")
            st.write("**RANKINGS Vs DATE 📈**")

            if filtered_player in players[1:]:
                player_data = bat_data[bat_data['Player_name'] == filtered_player]
                fig = px.line(player_data, x='Date', y='Previous_Ranking',
                              title=player_data['Player_name'].tolist()[0].upper(),
                              height=600, width=900)
                fig.add_scatter(x=player_data['Date'], y=player_data['Previous_Ranking'])
                fig.update_yaxes(autorange="reversed")
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)
                fig.update_layout(
                    font_family="Courier New",
                    font_color="green",
                    # title_font_family="Times New Roman",
                    title_font_color="black",
                    legend_title_font_color="black"
                )

                st.plotly_chart(fig)


                # with col2:




                #     st.write('\n')
                #     # st.subheader("PLAYER STATUS:")
                #
                #     if filtered_player != 'Select Player':
                #
                #         selected_player = bat_data[bat_data['Player_name'] == filtered_player]
                #
                #         if selected_player['Date'].tolist()[-1] < bat_data['Date'].tolist()[-1]:
                #             metric("RETIREMENT", "YES")
                #         else:
                #             metric("RETIREMENT", "NO")

        # st.sidebar.markdown("### Compare Players")
        # if not st.sidebar.checkbox('Hide', True, key=1):
        #
        #     with st.beta_container():
        #         player1, player2 = st.beta_columns(2)
        #
        #         with player1:
        #             st.subheader("## Select Player 1")
        #             filtered_player = st.selectbox("Select Player", players, key=1)
        #
        #             if filtered_player != 'Select Player':
        #                 pass


