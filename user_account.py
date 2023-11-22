import streamlit as st
import mysql.connector
from config import db_config
import hashlib

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

def create_usertable():
    cursor.execute('CREATE TABLE IF NOT EXISTS usertable(email VARCHAR(200) PRIMARY KEY, username VARCHAR(200), password VARCHAR(200), profession VARCHAR(200));')

def add_userdata(email, username, password, profession):
    try:
        if not email or not username or not password or not profession:
            st.warning("All fields are mandatory. Please provide values for all fields.")
            return
        
        create_usertable()

        cursor.execute('SELECT username FROM usertable WHERE email = %s;', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            st.warning("Email already exists. Please choose a different email.")
        else:
            hashed_password = make_hashes(password)
            cursor.execute('INSERT INTO usertable(email, username, password, profession) VALUES(%s, %s, %s, %s);', (email, username, hashed_password, profession))
            conn.commit()
            st.success("You have successfully created a valid Account")
            st.markdown('Please Login using your Email and Password')

    except mysql.connector.Error as e:
        st.warning(f"An error occurred: {e}")

def login_user(email, password):
    hashed_password = make_hashes(password)
    cursor.execute('SELECT * FROM usertable WHERE email = %s AND password = %s;', (email, hashed_password))
    data = cursor.fetchall()
    return data

def app():
    st.title('Welcome to :orange[DeepMediChecker] 💊')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False

    def user_auth(email, password):
        user_data = login_user(email, password)

        if user_data:
            st.success('Login Successful')
            st.session_state.username = user_data[0][1]
            st.session_state.useremail = user_data[0][0]
            st.session_state.is_logged_in = True
            st.session_state.signedout = True
            st.session_state.signout = True
        else:
            st.warning('Login Failed...Incorrect Email or Password')

    def user_signout():
        st.session_state.is_logged_in = False
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''

    if not st.session_state.is_logged_in:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign Up'])

        if choice == 'Login':
            email = st.text_input('Enter Email Address', key="email_login")
            password = st.text_input('Enter Password', type='password', key="password_login")

            if st.button('Login'):
                user_auth(email, password)
        else:
            email = st.text_input('Enter Email Address', key="email_signup")
            profession = st.text_input('Enter your Profession')
            username = st.text_input('Enter Username')
            password = st.text_input("Enter Password", type='password', key="password_signup")

            if st.button('Create my Account'):
                add_userdata(email, username, password, profession)
    else:
        st.text('Name: ' + st.session_state.username)
        st.text('Email ID: ' + st.session_state.useremail)
        st.button('Sign Out', on_click=user_signout)
