import streamlit as st
from functions import generatePrediction

DESIRED_WIDTH = 500

# def show_about_me_dialog():
#     st.write('Hello.')

# Apply custom CSS for a narrower sidebar
st.markdown(
    """
    <style>
    /* Adjust sidebar width */
    [data-testid="stSidebar"] {
        min-width: 250px; /* Set your desired width */
        max-width: 250px;
    }
    [data-testid="stAudio"] > audio {{
        width: {DESIRED_WIDTH}px !important;
    }}
    .centered-image-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }    
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- Show Dialogs --------------------
@st.dialog("The Big Picture", width="large")
def show_big_picture():
    text_content = """
# Human Influence on Climate is Undeniable
* ***Key Finding:*** It is unequivocal that human activities, especially emissions of greenhouse gases like CO₂, CH₄, and N₂O, are the dominant cause of observed climate changes since the industrial era.
* ***Implications:*** Policies must focus on reducing emissions to mitigate further warming.

# Global Warming Has Already Reached Alarming Levels
* The global surface temperature has increased by 1.09°C since pre-industrial times (1850–1900).
* Recent warming trends are unprecedented in the last 2000 years.
* ***Projections:*** Without drastic emissions cuts, we are likely to exceed 1.5°C of warming by the early 2030s.

# Climate Impacts Are Worsening
* ***Extreme Weather:*** Increased frequency and intensity of heatwaves, heavy rainfall, droughts, and tropical cyclones are directly linked to human-induced climate change.
* ***Rising Sea Levels:*** Sea levels rose faster in the last century than at any time in the past 3000 years, with further acceleration expected.
* ***Ocean and Cryosphere Changes:*** Oceans are warming, acidifying, and losing oxygen, while ice sheets and glaciers are melting at increasing rates.

# The Carbon Budget is Shrinking
* To limit warming to 1.5°C, humanity\’s remaining carbon budget is rapidly depleting.
* Even with net-zero CO₂ emissions, some climate changes—like sea level rise—are irreversible on human time scales.

# Regional Climate Variability is Critical
* Climate impacts are not uniform; regions will experience warming, sea level rise, and extreme events differently.
* ***Interactive Tools:*** Resources like the IPCC's Interactive Atlas are designed to provide localized climate projections.

# Tipping Points and Irreversibility
* Some systems, like the melting of large ice sheets or loss of biodiversity, may reach points of no return, leading to abrupt and irreversible changes.

# The Importance of Immediate Action
* ***Short-Lived Climate Forcers:*** Reducing emissions of methane and aerosols can have near-term climate and air quality benefits.
* ***Net Zero Targets:*** Achieving global net-zero emissions is crucial to stabilizing temperatures and limiting catastrophic outcomes.

# Enhanced Scientific Understanding
* Advances in climate models, observational techniques, and paleoclimate evidence have improved confidence in predictions.
* Climate sensitivity estimates (response to CO₂ doubling) have narrowed, reducing uncertainty in projections.
"""
    st.subheader("An overview...", divider="gray")
    st.markdown(text_content)

@st.dialog("EISENMAN, IAN", width="large")
def show_about_me_dialog():
    text_content = """
**Research Profile** - Climate Sciences, Ice in the Climate System, Modeling and State Estimation of the Oceans, Atmosphere, and Climate, Past Climate Change, Physical Oceanography
"""
    st.subheader("Professor", divider="gray")
    st.image("img/ian-headshot.jpg")
    st.markdown(text_content)

# This IPCC Working Group I contribution to the Sixth Assessment Report's Technical Summary assesses the current state of climate science. It details observed changes in global and regional climate, attributing many to human influence, and presents future projections under various emissions scenarios. The report highlights advancements in climate models and observational data, leading to increased confidence in understanding climate change. Specific attention is given to regional impacts, including changes in extreme weather events and sea level rise. The findings emphasize the urgency of mitigation efforts to limit the severity of future climate change and its associated risks.


# -------------------- Page Setup --------------------
PAGE = "🌡️ ClimateChangeGPT"

with st.sidebar:
    st.image("img/climage-change-report-cover.png", caption="Climate Change 2021: The Physical Science Basis")
    if st.sidebar.button("The Big Picture"):
        show_big_picture()

    if st.sidebar.button("Report Author"):
        show_about_me_dialog()

    st.write('---')

    st.markdown("[Technical Summary](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_TS.pdf)")

# -------------------- Page Header --------------------
st.header(PAGE, divider=True)

# -------------------- Chatbot --------------------
with st.container(border=True, height=200):
    st.subheader(f"Ask a climate change question...", divider=None)
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input(f"What can I explain about climate change?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        #PROPOSITION = st.session_state.selected_prop

        with st.spinner(f'Generating response (may take 1+ minutes)...'):
            response= generatePrediction(prompt)

            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response)

            # Add response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

# -------------------- Audio Player --------------------
container = st.container(border=True)
container.subheader(f"... or listen as our hosts make climate science accessible.", divider=None)
container.audio("img/climate-change-summary.mp3", format="audio/mpeg", loop=True, autoplay=True)
container.image("img/podcast-logo.jpg", width=500)

