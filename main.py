import streamlit as st
from streamlit_option_menu import option_menu
import home, user_account, about, ddi, article_explorer

st.set_page_config(
    page_title = "DeepMediChecker",)

class MultiApp:

    def __init__(self):
        self.apps = []
    
    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

def run():

    with st.sidebar:
        app = option_menu(
            menu_title = 'DeepMediChecker',
            options = ['Home', 'Account', 'About', 'DDI', 'Article Explorer'],
            icons = ['house-fill', 'person-fill', 'question-circle-fill', 'capsule-pill', 'collection-fill'],
            menu_icon = 'box',
            default_index = 1,
            styles = {
                "container": {"padding": "5!important","background-color":'#FFCC70'}, 
            "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#5C5470"},
        "nav-link-selected": {"background-color": "213555"},})


    if app == 'Home':
        home.app()
    if app == "Account":
        user_account.app()
    if app == "About":
        about.app()
    if app == "DDI":
        ddi.app()
    if app == "Article Explorer":
        article_explorer.app()



if __name__ == '__main__':
    run()
        