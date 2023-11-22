import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie

def app():

    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    #hello = load_lottieurl("https://lottie.host/74a9e5a7-f259-406f-a8df-6660aa351ca5/EWNxjmMvrf.json")
    med = load_lottieurl("https://lottie.host/9694b41a-8349-4225-a616-8157792cd8a3/Kx7PIoIrTO.json")

    st_lottie(med,
            height = 200,
            width = 200,
            speed = 1,
            loop = True,
            quality = 'high')

    st.title("💊📃**About DeepMediChecker**")

    st.write("")

    st.write("Our aim was to develop a web app that would help researchers/scholars/health professionals retrieve information about the type of \
            Drug-Drug Interactions for easy management and help improve the early detection of DDIs as it takes work for researchers and healthcare professionals \
            to review the reports on drug safety and the published articles on Drug-drug Interactions.")

    st.write("To also provide research article recommendations from the existing corpus for their study on the type of DDIs.")

    st.divider()

    st.write("")
    st.write("")    