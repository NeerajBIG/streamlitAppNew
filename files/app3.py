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
from datetime import datetime, timedelta
from streamlit_cookies_controller import CookieController
import streamlit.components.v1 as components

controller = CookieController()

db = MySQLDatabase(
    host='sql5.freesqldatabase.com',
    user='sql5801118',
    password='mqgWHRyzR1',
    database='sql5801118'
)


# user_data = {}

# Send registration email to user
def send_email_user(user, email, password):
    sender_email = "neeraj1wayitsol@gmail.com"  # Replace with your email
    sender_password = "gwgc ioef ymbx yybo"  # Replace with your email password
    recipient_email = email

    subject = "Registration Confirmation"
    body = f"Hello {user}, \n\nYour registration is successful! You will receive confirmation email once approved by admin. \n\n Your access details are as follows \n\nEmail: {email}\nPassword: {password}\nlink: https://bigauto.streamlit.app/\n\nThank you for signing up."

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


# Send registration email
def send_email_admin(user, email, password):
    sender_email = "neeraj1wayitsol@gmail.com"  # Replace with your email
    sender_password = "gwgc ioef ymbx yybo"  # Replace with your email password
    recipient_email = email

    subject = "New Registration for approval"
    body = f"Hello Admin, \n\n Someone just registered! Please confirm user's request. \n\n Link to admin portal is as follows \n\n link: https://bigauto.streamlit.app/\n\nThank you for signing up."

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
                    st.success(
                        f"Signup successful! You will receive confirmation email once approved by admin. Thanks {result[0]['name']}!")

                    st.text("Send Email to Admin")
                    send_email_user(name, email, password)  # Send registration email
                    time.sleep(2)

                    st.rerun()
            else:
                st.error("This email address is already registered.", icon="🚨")
            db.close()


# # Function to store session in browser storage for each user
# def set_browser_session(user_data):
#     # Get session storage object
#     session_storage = SessionStorage()
#
#     # Store the user data as an array of sessions (if more than one user logs in)
#     existing_sessions = session_storage.getItem("active_sessions")
#
#     if existing_sessions is None:
#         existing_sessions = []
#
#     # Add the new user's session to the list
#     existing_sessions.append(user_data)
#
#     # Save it back to session storage
#     session_storage.setItem("active_sessions", existing_sessions)

# Login logic
def login():
    st.title("Login.")
    email = st.text_input("Enter your Email")
    password = st.text_input("Enter your Password", type="password")

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
                # st.session_state.user_name = result[0]['name']
                # st.session_state.user_role = result[0]['role']

                current_datetime = datetime.now()
                st.text(current_datetime)
                insert_query = "INSERT INTO SessionDetails (userid, SessionActive, SessionTime) VALUES (%s, %s, %s)"
                insert_params = (result[0]['id'], '1', current_datetime)
                db.insert_data(insert_query, insert_params)

                # # SELECT query to verify data
                # select_query = "SELECT * FROM SessionDetails WHERE userid = %s"
                # params = (result[0]['id'],)
                # result = db.fetch_data(select_query, params)
                # st.text(result)

                expires = datetime.now() + timedelta(days=365 * 10)
                controller.set('user_role', result[0]['role'], expires=expires)
                controller.set('user_name', result[0]['name'], expires=expires)

                #st.rerun()

            db.close()


# Show homepage before login
def show_homepage():
    text = "BIG Automation Tool"
    num_chars = len(text)
    flashing_html = "".join([
        f'<span class="flashing-text">{char}</span>' if char != " " else '<span class="flashing-text">&nbsp;</span>'
        for char in text
    ])
    animation_delays = "\n".join(
        [f".flashing-text:nth-child({i + 1}) {{ animation-delay: {i * 0.2}s; }}" for i in range(num_chars)])

    st.markdown(f"""
            <style>
                .flashing-text {{
                    font-size: 60px;
                    font-weight: none;
                    color: navy;  
                    display: inline-block;
                    opacity: 1;
                    animation: flash 1s forwards;
                }}

                {animation_delays}

                @keyframes flash {{
                    0% {{ opacity: 1; }}
                    50% {{ opacity: 0; }}
                    100% {{ opacity: 1; }}
                }}
            </style>
        """, unsafe_allow_html=True)
    st.markdown(f'<p>{flashing_html}</p>', unsafe_allow_html=True)

    st.title(f"Hi, {controller.get('cookie_name')}!")
    st.write(f"Please signup to explore features.")


# Show homepage after login
def show_homepageQA():
    text = "BIG Automation Tool"
    num_chars = len(text)
    flashing_html = "".join([
        f'<span class="flashing-text">{char}</span>' if char != " " else '<span class="flashing-text">&nbsp;</span>'
        for char in text
    ])
    animation_delays = "\n".join(
        [f".flashing-text:nth-child({i + 1}) {{ animation-delay: {i * 0.2}s; }}" for i in range(num_chars)])

    st.markdown(f"""
            <style>
                .flashing-text {{
                    font-size: 60px;
                    font-weight: none;
                    color: navy;  
                    display: inline-block;
                    opacity: 1;
                    animation: flash 1s forwards;
                }}

                {animation_delays}

                @keyframes flash {{
                    0% {{ opacity: 1; }}
                    50% {{ opacity: 0; }}
                    100% {{ opacity: 1; }}
                }}
            </style>
        """, unsafe_allow_html=True)
    st.markdown(f'<p>{flashing_html}</p>', unsafe_allow_html=True)

    if controller.get('cookie_name') == "QA":
        userNameFound = controller.get('cookie_name')
        st.title(f"Welcome, {controller.get('cookie_name')}!")
        st.write(f"Your Role: {controller.get('cookie_name')}")

        cookie = controller.get('cookie_name')
        st.write(cookie)

        # set_browser_session(user_data)
        # session_storage = SessionStorage()
        # active_sessions = session_storage.getItem("active_sessions")
        #
        # if active_sessions:
        #     # Display info for all active users
        #     for session in active_sessions:
        #         st.write(f"Logged in as: {session['name']} (Role: {session['role']})")
        # else:
        #     st.write("No active users found.")

        # session_storage = SessionStorage()
        # data = session_storage.getItem("my_data")
        # if data is None:
        #     data = {"name": "Guesta"}
        #     session_storage.setItem("my_data", data)
        # session_storage.setItem("my_data", {"name": userNameFound})
        # st.write(session_storage.getItem("my_data"))
    else:
        st.write("You need to log in first!")


# Show homepage after login by Admin
def show_homepageAdmin():
    text = "BIG Automation Tool"
    num_chars = len(text)
    flashing_html = "".join([
        f'<span class="flashing-text">{char}</span>' if char != " " else '<span class="flashing-text">&nbsp;</span>'
        for char in text
    ])
    animation_delays = "\n".join(
        [f".flashing-text:nth-child({i + 1}) {{ animation-delay: {i * 0.2}s; }}" for i in range(num_chars)])

    st.markdown(f"""
            <style>
                .flashing-text {{
                    font-size: 60px;
                    font-weight: none;
                    color: navy;  
                    display: inline-block;
                    opacity: 1;
                    animation: flash 1s forwards;
                }}

                {animation_delays}

                @keyframes flash {{
                    0% {{ opacity: 1; }}
                    50% {{ opacity: 0; }}
                    100% {{ opacity: 1; }}
                }}
            </style>
        """, unsafe_allow_html=True)
    st.markdown(f'<p>{flashing_html}</p>', unsafe_allow_html=True)

    if controller.get('cookie_name') == "Admin":
        st.title(f"Welcome, {controller.get('cookie_name')}!")
        st.write(f"Your Role: {controller.get('cookie_name')}")
    else:
        st.write("You need to log in first!")


# Show users page after login by Admin
def show_usersAdmin():
    if controller.get('cookie_name') == "Admin":
        st.text("All User List")
        db.connect()

        option_1 = st.radio("Choose a user listing", ["All Active", "Pending Approval"])
        if option_1 == "All Active":
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

                selected_row = df[df['email'] == selected_email].iloc[
                    0]  # Get the row corresponding to the selected email
                selected_id = selected_row['id']
                selected_role = selected_row['role']

                if selected_role != "Admin":

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

                            if result[0]['email'] == selected_email and result[0]['verified'] == 2:
                                st.success(f"Account disabled successful!")
                                time.sleep(2)

                            st.rerun()

            st.text("Active User List")
            st.dataframe(df, height=300)
        elif option_1 == "Pending Approval":
            # SELECT query (fetching data)
            select_query = "SELECT * FROM users WHERE verified = %s"
            params = ("0",)
            result = db.fetch_data(select_query, params)

            if len(result) > 0:
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

                    selected_row = df[df['email'] == selected_email].iloc[
                        0]  # Get the row corresponding to the selected email
                    selected_id = selected_row['id']
                    selected_role = selected_row['role']

                    if selected_role != "Admin":
                        col1, col2, col3 = st.columns(3)

                        # Display ID and Role
                        with col1:
                            st.write(f"Selected ID: {selected_id}")
                        with col2:
                            st.write(f"Selected Role: {selected_role}")

                        with col3:
                            if st.button("Approve Record"):
                                # Example UPDATE query (updating data)
                                update_query = "UPDATE users SET verified = %s WHERE email = %s"
                                update_params = ('1', selected_email)
                                db.update_data(update_query, update_params)

                                # SELECT query to verify data
                                select_query = "SELECT * FROM users WHERE email = %s"
                                params = (selected_email,)
                                result = db.fetch_data(select_query, params)

                                if result[0]['email'] == selected_email and result[0]['verified'] == 1:
                                    st.success(f"Account approved successful!")
                                    time.sleep(2)
                                st.rerun()

                st.text("Active User List")
                st.dataframe(df, height=300)
            else:
                st.error("No record found")

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
    page = st.sidebar.radio("Choose a page", ["Home", "Learning"])
    if page == "Home":
        show_homepageQA()
    elif page == "My Data":
        st.text("Add a new page here for QA user")

    # Logout button
    if st.sidebar.button("Logout"):
        try:
            controller.remove("cookie_name")
            controller.remove("cookie_name1")
            controller.remove("user_cookie")
            controller.set('user_role', "Guest")
            controller.set('user_name', "Unknown")
        except:
            pass
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

    # Logout button
    if st.sidebar.button("Logout"):
        try:
            controller.remove("cookie_name")
            controller.remove("cookie_name1")
            controller.remove("user_cookie")
            controller.set('user_role', "Guest")
            controller.set('user_name', "Unknown")
        except:
            pass
        st.sidebar.success("You have been logged out!")
        time.sleep(2)
        streamlit_js_eval(js_expressions="parent.window.location.reload()")


# Main function to control the app flow
def main():
    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #ff9559; /* French Navy color */
            color: white; /* Text color */
        }
        </style>""", unsafe_allow_html=True)

    # st.write(controller.getAll())
    # st.text(controller.get('cookie_name'))

    # cookie_value = st.query_params().get("cookieValue", ["default_value"])[0]
    # st.write(f"Current Cookie Value 2 : {cookie_value}")

    # st.text(controller.get('identity'))
    # if str(controller.get('identity')) == 'None':
    #     st.text("dskjdddddddddd")
    #     controller.set('cookie_name', 'Guest')
    #     controller.set('identity', 'IdentityChanged')
    cookie = controller.get('cookie_name1')
    st.text(cookie)
    st.write(controller.getAll())
    if controller.get('user_role') == 'Guest':
        sidebar_navigation()
    elif controller.get('user_role') == 'QA':
        sidebar_navigationQA()
    elif controller.get('user_role') == 'Admin':
        sidebar_navigationAdmin()


if __name__ == '__main__':
    main()
