import os, sys
import time
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from streamlit_js_eval import streamlit_js_eval
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from files.mySQLConnector import MySQLDatabase
import re
import pandas as pd


db = MySQLDatabase(
        host='sql5.freesqldatabase.com',
        user='sql5801118',
        password='mqgWHRyzR1',
        database='sql5801118'
)

# Send registration email
def send_email(email, password):
    sender_email = "teamqa59@gmail.com"  # Replace with your email
    sender_password = "Gagan@0309"  # Replace with your email password
    recipient_email = email

    subject = "Registration Confirmation"
    body = f"Hello, \n\nYour registration is successful! \n\nEmail: {email}\nPassword: {password}\n\nThank you for signing up."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Set up the server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
    except Exception as e:
        st.error(f"Error sending email: {e}")

# Signup logic
def signup():
    st.title("Signup")

    name = st.text_input("Enter your Name")
    email = st.text_input("Enter your Email")
    role = st.selectbox("Select Role", ['Select', 'QA', 'Admin'])
    password = st.text_input("Enter your Password", type="password")
    confirm_password = st.text_input("Confirm your Password", type="password")

    st.markdown("""
                <style>
                div.stButton > button:first-child {
                    background-color: #022658; /* French Navy color */
                    color: white; /* Text color */
                }
                </style>""", unsafe_allow_html=True)

    if st.button("Signup"):
        if not name or not email or not password or not confirm_password or role == "Select":
            st.error("All fields are required!", icon="🚨")
        elif bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email)) != True:
            st.error("Invalid email address", icon="🚨")
        elif password != confirm_password:
            st.error("Passwords do not match.", icon="🚨")
        else:
            db.connect()

            # SELECT query (fetching data)
            select_query = "SELECT * FROM users WHERE email = %s"
            params = (email,)
            result = db.fetch_data(select_query, params)
            time.sleep(2)
            if len(result) == 0:
                # INSERT query (inserting data)
                insert_query = "INSERT INTO users (name, email, role, password, verified) VALUES (%s, %s, %s, %s, %s)"
                insert_params = (name, email, role, confirm_password, '0')
                db.insert_data(insert_query, insert_params)

                st.text("Please wait")

                time.sleep(5)

                # Example SELECT query (fetching data)
                select_query = "SELECT * FROM users WHERE email = %s"
                params = (email,)
                result = db.fetch_data(select_query, params)

                if len(result) == 0:
                    st.error("Signup failed! You will receive signup details once verified.", icon="🚨")
                elif len(result) == 1:
                    st.success(f"Signup successful! You will receive confirmation email once approved by admin. Thanks {result[0]['name']}!")

                    st.text("Send Email to Admin")
                    #send_email(email, password)  # Send registration email
                    time.sleep(2)

                    st.rerun()
            else:
                st.error("This email address is already registered.", icon="🚨")
            db.close()

# Login logic
def login():
    st.title("Login")
    email = st.text_input("Enter your Email")
    password = st.text_input("Enter your Password", type="password")

    st.markdown("""
                <style>
                div.stButton > button:first-child {
                    background-color: #022658; /* French Navy color */
                    color: white; /* Text color */
                }
                </style>""", unsafe_allow_html=True)

    if st.button("Login"):
        if not email or not password:
            st.error("All fields are required!", icon="🚨")
        else:
            db.connect()

            # SELECT query (fetching data)
            select_query = "SELECT * FROM users WHERE email = %s"
            params = (email,)
            result = db.fetch_data(select_query, params)

            if len(result) == 0:
                st.error("Login failed! Unknown username or password.", icon="🚨")

            elif result[0]['email'] == email and result[0]['verified'] == 0:
                st.error(f"Hi, {result[0]['name']}! You account is pending approval and is not yet active for login.")

            elif result[0]['email'] == email and result[0]['verified'] == 1 and result[0]['password'] != password:
                st.error("Login failed! Invalid username or password.", icon="🚨")

            elif result[0]['email'] == email and result[0]['verified'] == 2 and result[0]['password'] == password:
                st.error("Account Disabled", icon="🚨")

            elif result[0]['email'] == email and result[0]['verified'] == 1 and result[0]['password'] == password:
                st.success(f"Login successful! Welcome back, {result[0]['name']}!")

                # Storing the user's name and role in session state
                st.session_state.user_name = result[0]['name']
                st.session_state.user_role = result[0]['role']

                time.sleep(2)
                st.rerun()

            db.close()

# Show homepage before login
def show_homepage():
    st.title(f"Hi, {st.session_state.user_name}!")
    st.write(f"Your are a guest user. Please signup to explore BIG automation tool.")

# Show homepage after login
def show_homepageQA():
    if 'user_name' in st.session_state:
        st.title(f"Welcome, {st.session_state.user_name}!")
        st.write(f"Your Role: {st.session_state.user_role}")
        st.text(st.session_state)
    else:
        st.write("You need to log in first!")

# Show homepage after login by Admin
def show_homepageAdmin():
    if 'user_name' in st.session_state:
        st.title(f"Welcome Admin, {st.session_state.user_name}!")
        st.write(f"Your Role: {st.session_state.user_role}")
        st.text(st.session_state)
    else:
        st.write("You need to log in first!")

# Show users page after login by Admin
def show_usersAdmin():
    if 'user_name' in st.session_state:
        st.text("Show table of all users here.")
        db.connect()

        # SELECT query (fetching data)
        select_query = "SELECT * FROM users WHERE verified = %s"
        params = ("1",)
        result = db.fetch_data(select_query, params)

        df = pd.DataFrame(result)

        st.markdown("""
            <style>
                /* Make column headers bold */
                .dataframe thead th {
                    font-weight: bold !important;
                    text-align: left !important;
                }

                /* Left-align text in the table cells */
                .dataframe tbody tr th, .dataframe tbody tr td {
                    text-align: left !important;
                }

                /* Make the dataframe scrollable horizontally if it overflows */
                .stDataFrame div {
                    overflow-x: auto !important;
                }
            </style>
        """, unsafe_allow_html=True)

        email_options = df['email'].tolist()  # Get all emails
        email_options.insert(0, "Select")  # Add "Select" as the first option

        selected_email = st.selectbox("Select an Email", email_options, key="email_selectbox")

        if selected_email != "Select":

            selected_row = df[df['email'] == selected_email].iloc[0]  # Get the row corresponding to the selected email
            selected_id = selected_row['id']
            selected_role = selected_row['role']

            if selected_role != "Admin":
                st.markdown("""
                <style>
                div.stButton > button:first-child {
                    background-color: #FF0000; /* red color */
                    color: white; /* Text color */
                }
                </style>""", unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)

                # Display ID and Role
                with col1:
                    st.write(f"Selected ID: {selected_id}")
                with col2:
                    st.write(f"Selected Role: {selected_role}")

                with col3:
                    if st.button("Disable Record"):
                        # Example UPDATE query (updating data)
                        update_query = "UPDATE users SET verified = %s WHERE email = %s"
                        update_params = ('2', selected_email)
                        db.update_data(update_query, update_params)

                        # SELECT query to verify data
                        select_query = "SELECT * FROM users WHERE email = %s"
                        params = (selected_email,)
                        result = db.fetch_data(select_query, params)

                        if result[0]['email'] == selected_email and result[0]['verified'] == 2 :
                            st.success(f"Account disabled successful!")
                            time.sleep(2)

                        st.rerun()

        st.text("Active User List")
        st.dataframe(df, height=300)

    else:
        st.write("You need to log in first!")

# Sidebar navigation
def sidebar_navigation():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose a page", ["Home", "Signup", "Login"])
    if page == "Home":
        show_homepage()
    elif page == "Signup":
        signup()
    elif page == "Login":
        login()

def sidebar_navigationQA():

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose a page", ["Home", "My Data"])
    if page == "Home":
        show_homepageQA()
    elif page == "My Data":
        st.text("Add a new page here for QA user")

    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #022658; /* French Navy color */
            color: white; /* Text color */
        }
        </style>""", unsafe_allow_html=True)
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state['user_role'] = 'Guest'
        st.session_state['user_name'] = 'Guest User'

        st.sidebar.success("You have been logged out!")
        time.sleep(2)
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

def sidebar_navigationAdmin():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose a page", ["Home", "All Users"])
    if page == "Home":
        show_homepageAdmin()
    elif page == "All Users":
        show_usersAdmin()

    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #022658; /* French Navy color */
            color: white; /* Text color */
        }
        </style>""", unsafe_allow_html=True)
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state['user_role'] = 'Guest'
        st.session_state['user_name'] = 'Guest User'

        st.sidebar.success("You have been logged out!")
        time.sleep(2)
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

# Main function to control the app flow
def main():
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #022658; /* Red color */
        color: white; /* Text color */
    }
    </style>""", unsafe_allow_html=True)

    # Ensure session state is initialized
    if 'user_role' not in st.session_state:
        st.session_state['user_role'] = 'Guest'
    if 'user_name' not in st.session_state:
        st.session_state['user_name'] = 'Guest User'

    if st.session_state['user_role'] == 'Guest':
        sidebar_navigation()
    elif st.session_state['user_role'] == 'QA':
        sidebar_navigationQA()
    elif st.session_state['user_role'] == 'Admin':
        sidebar_navigationAdmin()


if __name__ == '__main__':
    main()
