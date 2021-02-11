import streamlit as st
import pandas as pd
from streamlit_metrics import metric, metric_row
import plotly.express as px




def app():

    st.title("Bowlers statistics")
    st.write(
        "#### This page provides complete data on bowlers. You can filter by country, date  and take a look at his ranking curve.")
    st.write("\n")
    DATA_URL = (r"C:\Users\mani ratnam\Desktop\bowler_data.csv")

    def load_data():
        bowler_data = pd.read_csv(DATA_URL)
        return  bowler_data

    bowler_data = load_data()

    dates = bowler_data['Date'].tolist()

    st.sidebar.markdown("### Show time  slider")
    if not st.sidebar.checkbox('Hide', True):

        with st.beta_container():
            # slider for selecting month and year interval
            start_month_year, end_month_year = st.select_slider(
                label="Select Time Period",
                options=dates,
                value=(dates[0], dates[-1]),
                format_func=lambda x: pd.to_datetime(x).strftime(" %Y,%b")
            )

        if start_month_year and end_month_year:

            bowler_data = bowler_data.loc[
                (bowler_data["Date"] >= start_month_year)
                & (bowler_data["Date"] <= end_month_year)
            ]

    with st.beta_container():
        left_element, right_element = st.beta_columns(2)

        players = bowler_data["Player_name"].unique().tolist()
        players.insert(0, 'Select Player')

        with left_element:

            filtered_player = st.selectbox("Select Player name", players)


        if filtered_player != 'Select Player':
            st.write("**SELECTED PLAYER:  {}**".format(filtered_player.upper()))
            player_data = bowler_data[bowler_data['Player_name'] == filtered_player]

        else:
            pass
        st.write("\n")

        with right_element:
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

    with st.beta_container():

        # col1,col2 = st.beta_columns(2)

        # with col1:
        st.write("**RATINGS Vs DATE 📈**")

        if filtered_player in players[1:]:
            player_data = bowler_data[bowler_data['Player_name'] == filtered_player]
            fig = px.line(player_data, x='Date', y='Rating', title=player_data['Player_name'].tolist()[0].upper(), height=600,
                          width=900)
            fig.add_scatter(x=player_data['Date'], y=player_data['Rating'])
            fig.update_yaxes(autorange="reversed")
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                font_family="Courier New",
                font_color="green",
                title_font_family="Times New Roman",
                title_font_color="blue",
                legend_title_font_color="green"
            )
            st.plotly_chart(fig)

        with st.beta_container():
            st.write("**RANKINGS Vs DATE 📈**")

            if filtered_player in players[1:]:
                player_data = bowler_data[bowler_data['Player_name'] == filtered_player]
                fig = px.line(player_data,
                              x='Date',
                              y='Previous_Ranking',
                              title=player_data['Player_name'].tolist()[0].upper(), height=600, width=900
                              )
                fig.add_scatter(x=player_data['Date'],
                                y=player_data['Previous_Ranking']
                                )
                fig.update_yaxes(autorange="reversed")
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)
                fig.update_layout(
                    font_family="Courier New",
                    font_color="green",
                    title_font_family="Times New Roman",
                    title_font_color="blue",
                    legend_title_font_color="green"
                )
                st.plotly_chart(fig)







            # with col2:
            #     st.write('\n')
            #     # st.subheader("PLAYER STATUS:")
            #
            #     if filtered_player != 'Select Player':
            #
            #         selected_player = bowler_data[bowler_data['Player_name'] == filtered_player]
            #
            #         if selected_player['Date'].tolist()[-1] < bowler_data['Date'].tolist()[-1]:
            #             metric("RETIREMENT", "YES")
            #         else:
            #             metric("RETIREMENT", "NO")

