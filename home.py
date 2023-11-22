import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie

def app():

    # Function to load Lottie animation from URL
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    
        # Load Lottie animations
    #hello = load_lottieurl("https://lottie.host/74a9e5a7-f259-406f-a8df-6660aa351ca5/EWNxjmMvrf.json")
    us = load_lottieurl("https://lottie.host/f5045a7b-1bf2-4585-a877-82c68e9e0c9a/qOR8S9jGwX.json")
    robo = load_lottieurl("https://lottie.host/5cb5e7ad-8eab-4194-a7cd-4883705cdd34/SKkYvQnEVk.json")

    # Display the title with CSS animation
    st.markdown(
        """
        <style>
        .title-wrapper {
            text-align: center;
        }
        .title {
            font-size: 4rem;
            color: #FE0000;
            font-weight: bold;
            animation: pulsate 2s ease-out, glow 1s linear infinite;
            animation-iteration-count: infinite;
            opacity: 0.5;
        }
        @keyframes pulsate {
            0% { transform: scale(1); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }
        @keyframes glow {
            0% { box-shadow: 0 0 5px orange; }
            50% { box-shadow: 0 0 20px orange; }
            100% { box-shadow: 0 0 5px orange; }
        }
        </style>
        <div class="title-wrapper"><div class="title">DeepMediChecker</div></div>
        """,
        unsafe_allow_html=True
    )

    # Display the first Lottie animation
    st_lottie(robo,
            height=200,
            width=200,
            speed=1,
            loop=True,
            quality='high')


    st.write("")
    st.markdown("This is **Harsha** and **Madiha**!")

    # Display the introductory text
    st.write("We present to you an application we created to make it easy for users that include researchers, scholars, and health professionals to:")
    st.write("Check the type/class of Drug-Drug interaction: crucial to know about the combination of drugs \
                that can be consumed together and their adverse effects. It is important to understand the interactions as it can result in \
                increased toxicity and development of adverse reactions that may endanger a patient's health.")
    st.divider()

    # Display the section about pharmacovigilance in an expander
    st.subheader("But wait, let us understand the standard terms first!")
    with st.expander("Know about Pharmacovigilance"):
        st.markdown("**Pharmacovigilance:** ")
        st.write("Pharmacovigilance (PV) plays a critical role in mitigating and managing the effects of ADRs.\
                Pharmacovigilance provides an alarm signal through the early detection of new ADRs. It plays \
                a crucial role in ensuring the safety and efficacy of medications, particularly after they have been \
                released to the market. The primary objective of pharmacovigilance is to identify and minimize risks associated with \
                pharmaceutical products, including adverse drug reactions (ADRs) and drug-drug interactions (DDIs), among others.")

    st.divider()
    st.header(":orange[Explore the web application]🧑‍🚀")

    st.subheader("You want to start with the :red['About'] page first to understand what our work is about 🤓")
    st.write("")
    st.subheader(":red[Sign Up] first if you have stumbled across for the first time here, or :green[log in] if you have been here before!")
    st.write("")
    #st.subheader("But if you are a curious mind, then, jump right in and check out how this works! 🧐")
    
    

    # Display the second Lottie animation
    st_lottie(us,
            height=300,
            width=300,
            speed=1,
            loop=True,
            quality='high')

    # Display the final message
    st.write("Thank you! 🤗")


