import streamlit as st
import pandas as pd
from streamlit_metrics import metric, metric_row
import plotly.express as px


def app():
    st.title("All-rounders statistics")
    st.write(
        "#### This page provides complete data on batsmen."
        " You can filter by  date  and take a look at his ranking/rating curve.")
    st.write("\n")

    DATA_URL = (r"C:\Users\mani ratnam\Desktop\Allrounder_data.csv")

    def load_data():
        Allrounder_data = pd.read_csv(DATA_URL)
        return Allrounder_data

    Allrounder_data = load_data()

    dates = Allrounder_data['Date'].tolist()
    # sildebar  is auto hid to make to make the dasboard more responsive.
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
            bat_data = Allrounder_data.loc[
                (Allrounder_data["Date"] >= start_month_year)
                & (Allrounder_data["Date"] <= end_month_year)
                ]

    with st.beta_container():
        left_element, right_element = st.beta_columns(2)

        players = Allrounder_data["Player_name"].unique().tolist()
        players.insert(0, 'Select Player')

        with left_element:

            filtered_player = st.selectbox("Select Player name", players)

        if filtered_player != 'Select Player':
            player_data = Allrounder_data[Allrounder_data['Player_name'] == filtered_player]
            st.write("**SELECTED PLAYER:  {}**".format(filtered_player))

        # else:
        #     pass

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
            st.write("**RATINGS Vs DATE 📈**")

            if filtered_player in players[1:]:
                player_data = Allrounder_data[Allrounder_data['Player_name'] == filtered_player]
                fig = px.line(player_data, x='Date', y='Rating', title=player_data['Player_name'].tolist()[0].upper(),
                              height=600)
                fig.add_scatter(x=player_data['Date'], y=player_data['Rating'])
                fig.update_layout(
                    font_family="Courier New",
                    font_color="green",
                    title_font_family="Times New Roman",
                    title_font_color="blue",
                    legend_title_font_color="green")
                st.plotly_chart(fig)

        with st.beta_container():
            st.write("**RANKINGS Vs DATE 📈**")
            if filtered_player in players[1:]:
                player_data = Allrounder_data[Allrounder_data['Player_name'] == filtered_player]
                fig = px.line(player_data,
                              x='Date',
                              y='Previous_Ranking',
                              title=player_data['Player_name'].tolist()[0].upper(),
                              height=600, width=900
                              )
                fig.add_scatter(x=player_data['Date'],
                                y=player_data['Previous_Ranking']
                                )
                # fig.update_yaxes(autorange="reversed")
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

            # Down here is a code for visualization that is not implemented in the dashboard
            #     st.write('\n')
            #     # st.subheader("PLAYER STATUS:")
            #
            #     if filtered_player != 'Select Player':
            #
            #         selected_player = Allrounder_data[Allrounder_data['Player_name'] == filtered_player]
            #
            #         if selected_player['Date'].tolist()[-1] < Allrounder_data['Date'].tolist()[-1]:
            #             metric("RETIREMENT", "YES")
            #         else:
            #             metric("RETIREMENT", "NO")
