import streamlit as st
import pandas as pd
import Introduction
import batting
import bowling
import Allrounder


st.set_page_config(
    layout="wide",
    page_icon="static/images/favicon.png",
    page_title="odi rankings- Factly",
)


# setting the logo of "Factly Dashboards"
logo_html = '<a href="https://dashboards.factly.in"><img alt="Logo" src="https://dashboards.factly.in/logo.svg"></a>'
st.sidebar.markdown(logo_html, unsafe_allow_html=True)


st.sidebar.title("Navigate Through Player Type. ")


@st.cache
def load_data():
    data= pd.read_csv('odi_ratings.csv')
    return data

data=load_data()


PAGES = {
    "Introduction": Introduction,
    "Batsmen": batting,
    "Bowlers":bowling,
    "All-rounders":Allrounder
}
selection = st.sidebar.radio("start exploring for more interesting insights created for you.", list(PAGES.keys()))
page = PAGES[selection]
page.app()



# adding link to all dashboards on the sidebar menu

# link_html = '<a href="https://dashboards.factly.in">All Dashboards by Factly</a>'
#
# st.sidebar.markdown(link_html, unsafe_allow_html=True)
#
# st.sidebar.write("**Contact Us:**")
# st.sidebar.write("Email ID : hi@factly.in", unsafe_allow_html=True)
#
# st.sidebar.write("**Sources:**")
# st.sidebar.write("""[https://www.icc-cricket.com/rankings/mens/player-rankings/odi](https://www.icc-cricket.com/rankings/mens/player-rankings/odi) """)
# st.sidebar.write("")
#
# st.sidebar.write("**Disclaimer:**")
# st.sidebar.write(
#     "Data/Information presented here is being done in good faith."
#     " While we have taken all efforts to ensure the accuracy of data/information,"
#     " we ask you to refer to the original data/information sources in case of any discrepancy."
# )
#
#
#
# # to remove the hamburger menu and rename the footer
# hide_streamlit_style = """"
# <style>
#     MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     footer:after {
#         content:'© Factly Media & Research 2021. All rights reserved';
#         visibility: visible;
#         display: block;
#         position: relative;
#         #background-color: red;
#         padding: 5px;
#         top: 2px;
#     }
#     </style>"""






