import streamlit as st
from PIL import Image
import sqlite3
import pandas as pd
import pickle

model = pickle.load(open('naive_model.pkl', 'rb'))

conn = sqlite3.connect("dbase.db")
cursor = conn.cursor()


def add_doctor(doctorname, specialization, mobilenumber):
    cursor.execute("INSERT INTO doctordb(doctorname, specialization, mobileno) VALUES (?,?)", (doctorname,
                   specialization, mobilenumber))
    conn.commit()


def create_doctor_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS doctordb(doctorname TEXT,specialization TEXT,hospital TEXT,mobileno NUMBER)')


def add_doctor_data(doctorname, specialization, hospital, mobileno):
    cursor.execute('INSERT INTO doctordb(doctorname,specialization,hospital,mobileno) VALUES (?,?,?,?)', (doctorname, specialization, hospital, mobileno))
    conn.commit()


def view_user():
    cursor.execute("SELECT * FROM userdb")
    df = pd.DataFrame(cursor.fetchall(), columns=['username', 'password'])
    st.dataframe(df)


def view_doctor():
    cursor.execute("SELECT * FROM doctordb")
    df = pd.DataFrame(cursor.fetchall(), columns=['doctorname', 'specialization', 'mobileno'])
    st.dataframe(df)


def view_training_data():
    data = pd.read_csv('HeartDataSet.csv')
    st.dataframe(data)


def create_admin_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS admindb(username TEXT,password TEXT)')


def create_user_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS userdb(username TEXT,password TEXT)')


def login_admin(username, password):
    cursor.execute('SELECT * FROM admindb WHERE username =? AND password = ?', (username, password))
    data = cursor.fetchall()
    return data


def login_user(username, password):
    cursor.execute('SELECT * FROM userdb WHERE username =? AND password = ?', (username, password))
    data = cursor.fetchall()
    return data


def add_userdata(username, password):
    cursor.execute("SELECT EXISTS(SELECT * FROM userdb WHERE username=? AND password=?)", (username, password))
    check = cursor.fetchone()
    if check[0]:
        st.warning("user already exists")
        return 0
    else:
        cursor.execute('INSERT INTO userdb(username,password) VALUES (?,?)', (username, password))
        conn.commit()
        return 1


def prediction(age, gender, chest_pain_type, blood_pressure, cholesterol, blood_sugar, ecg, heart_rate,
               exercise_angina, oldpeak, ST_slope):
    if gender == 'Male':
        gender = 1
    else:
        gender = 0
    if chest_pain_type == 'Typical Angina':
        chest_pain_type = 1
    elif chest_pain_type == 'Atypical Angina':
        chest_pain_type = 2
    elif chest_pain_type == 'Non-Anginal Pain':
        chest_pain_type = 3
    else:
        chest_pain_type = 4
    if blood_sugar == '<120 mg/dl':
        blood_sugar = 0
    else:
        blood_sugar = 1
    if ecg == 'Low Rate':
        ecg = 1
    elif ecg == 'Normal':
        ecg = 2
    else:
        ecg = 3
    if exercise_angina == 'Yes':
        exercise_angina = 1
    else:
        exercise_angina = 0
    if ST_slope == 'Upsloping':
        ST_slope = 1
    elif ST_slope == 'Flat':
        ST_slope = 2
    else:
        ST_slope = 3
    result = model.predict([[age, gender, chest_pain_type, blood_pressure, cholesterol, blood_sugar, ecg,
                             heart_rate, exercise_angina, oldpeak, ST_slope]])
    # st.write(result)
    if result:
        st.write("### Had a Risk :disappointed: Need to Consult Doctor :hospital: ###")
        with st.expander("Suggestion to Reduce Effect"):
            st.write("## Common Measures ##")
            st.markdown("""<ul>
            <li>Avoid junk food</li>
            <li>Less intake of caffeine</li>
            <li>Maintain healthy weight</li>
            </ul>""", unsafe_allow_html=True)
            if blood_sugar == 1:
                st.markdown("""<table border="1"><tr><td>Blood Sugar</td>
                <td>>=120 mg/dl</td>
                <td><ul>
                        <li>Follow Low Sugar Diet</li>
                        <li>Take Frequent checkups</li>
                    </ul>
                </td>
                </tr></table> """, unsafe_allow_html=True)
            if blood_pressure > 130:
                st.markdown("""<table border="1"><tr><td>Blood Pressure</td>
                                <td> Not Normal</td>
                                <td><ul>
                                        <li>Follow Healthy Diet</li>
                                        <li>Take Frequent checkups</li>
                                        <li>Reduce Stress</li>
                                    </ul>
                                </td>
                                </tr></table> """, unsafe_allow_html=True)
            if chest_pain_type == 1:
                st.markdown("""<table border="1"><tr><td>Chest Pain</td>
                                                <td> Typical </td>
                                                <td><ul>
                                                        <li>Relax your body</li>
                                                        <li>Don't take unusual breathing</li>
                                                        <li>Reduce Stress</li>
                                                        <li>Do Regular Exercise</li>
                                                    </ul>
                                                </td>
                                                </tr></table> """, unsafe_allow_html=True)
            elif chest_pain_type == 2:
                st.markdown("""<table border="1"><tr><td>Chest Pain</td>
                                                                <td> Atypical </td>
                                                                <td><ul>                                    
                                                                        <li>Reduce Stress</li>
                                                                        <li>Do Regular Exercise</li>
                                                                        <li>Reduce high Cholesterol Foods</li>
                                                                    </ul>
                                                                </td>
                                                                </tr></table> """, unsafe_allow_html=True)
            elif chest_pain_type == 3:
                st.markdown("""<table border="1"><tr><td>Chest Pain</td>
                                                 <td> Non-Anginal </td>
                                                 <td><ul>                                    
                                                     <li>Take proper sleep</li>
                                                     <li>Do Regular Exercise</li>
                                                     <li>Reduce high Cholesterol Foods</li>
                                                     </ul>
                                                 </td>
                                                 </tr></table> """, unsafe_allow_html=True)
            else:
                st.markdown("""<table border="1"><tr><td>Chest Pain</td>
                                                                <td>Asymptomatic</td>
                                                                <td><ul>         
                                                                    <li>Reduce high Cholesterol Foods</li>                           
                                                                    <li>Take proper sleep</li>
                                                                    <li>Do Regular Exercise</li>
                                                                    <li>Take frequent checkups</li>
                                                                    </ul>
                                                                </td>
                                                                </tr></table> """, unsafe_allow_html=True)
    else:
        st.write("### :smiley: Happy to GO... ###")
        with st.expander("Preventive Measures for Heart Diseases"):
            st.markdown("""<ul><li>Control your blood pressure.</li><li>Avoid smoking and using tobacco 
            products.</li><li> Keep your total cholesterol healthy. </li><li>  Keep your blood sugar healthy. </li>
            <li>  Be physically active every day. </li></ul>""", unsafe_allow_html=True)


def admin_page():
    modules = ["Add Doctor", "View User", "View Doctor", "View Training Data"]
    goto = st.radio("Go To", modules)
    if goto == "Add Doctor":
        doctorname = st.text_input("Doctor Name")
        specialization = st.text_input("Specialization")
        hospital = st.text_input("Hospital Name")
        mobileno = st.text_input("Mobile Number")
        if st.button("Add Doctor"):
            create_doctor_table()
            add_doctor_data(doctorname, specialization, hospital, mobileno)
            st.success("You have successfully added doctor.Go to the Login Menu to login")
    elif goto == "View User":
        view_user()
    elif goto == "View Doctor":
        view_doctor()
    else:
        view_training_data()


def login_page():
    modules = ["Prediction", "View Doctor"]
    goto = st.radio("Go To", modules)
    if goto == "Prediction":
        st.title("Prediction Analysis")
        with st.form(key='form', clear_on_submit=True):
            age = st.slider("Age", 15, 99)
            gender = st.selectbox("Gender", ['Male', 'Female'])
            chest_pain_type = st.selectbox("Chest Pain Type",
                                           ['Typical Angina', 'Atypical Angina', 'Non-Anginal Pain', 'Asymptomatic'])
            blood_pressure = st.slider("Blood Pressure at Rest Mode", 110, 200)
            cholesterol = st.slider("Cholesterol Level", 100, 450)
            blood_sugar = st.selectbox("Blood Sugar Level", ['>=120 mg/dl', '<120 mg/dl'])
            ecg = st.selectbox("Rest ECG", ['Low Rate', 'Normal', 'Abnormal'])
            heart_rate = st.slider("Max Heart Rate", 60, 210)
            exercise_angina = st.selectbox("Exercise Angina", ['Yes', 'No'])
            oldpeak = st.slider("Oldpeak", 0.0, 6.0, step=0.1)
            ST_slope = st.selectbox("ST Slope", ['Upsloping', 'Flat', 'Downsloping'])
            predict = st.form_submit_button("Predict")
        if predict:
            prediction(age, gender, chest_pain_type, blood_pressure, cholesterol, blood_sugar, ecg, heart_rate,
                       exercise_angina, oldpeak, ST_slope)
    else:
        view_doctor()


def db_main():
    home = ["Home", "Admin", "Login", "Signup"]
    st.sidebar.title("Credentials")
    choice = st.sidebar.selectbox("", home)
    if choice == "Home":
        with st.expander("Sitemap"):
            st.subheader("SiteMap")
            st.write("##### :heavy_check_mark: Sidebar Contents #####")
            st.write("###### :heavy_minus_sign: Credentials :closed_lock_with_key: ##### ")
            st.write("Superuser Login")
            st.write("User Login")
            st.write("User Signup")
            st.write("##### :heavy_check_mark: Superuser Contents :guardsman: #####")
            st.write("Add Doctor")
            st.write("View User")
            st.write("View Doctor")
            st.write("View Training Data")
            st.write("##### :heavy_check_mark: User Contents :busts_in_silhouette: #####")
            st.write("Prediction")
            st.write("View Doctor")
    elif choice == "Admin":
        # st.subheader("Admin Login")
        admin_name = st.sidebar.text_input("Username")
        admin_password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.checkbox("AdminLogin"):
            create_admin_table()
            result = login_admin(admin_name, admin_password)
            if result:
                admin_page()
            else:
                st.warning("Wrong Credentials")
            # query = "SELECT * FROM admindb"
            # cursor.execute(query)
            # data = cursor.fetchall()
            # if data[0][0] == admin_name and data[0][1] == admin_password:
            #     st.write("successful db")
            # else:
            #     st.write("not successful")

    elif choice == "Login":
        # st.subheader("User Login")
        user_name = st.sidebar.text_input("Username")
        user_pass = st.sidebar.text_input("Password", type="password")
        if st.sidebar.checkbox("UserLogin"):
            create_user_table()
            result = login_user(user_name, user_pass)
            if result:
                login_page()
            else:
                st.warning("Wrong Credentials")

            # cursor.execute("SELECT * FROM userdb WHERE username = ? AND password = ?", (user_name,user_pass))
            # data = cursor.fetchall()
            # if data:
            #     st.write("successfully logged in")
            # else:
            #     st.write("wrong credentials")

    else:
        # st.subheader("User Signup")
        user_name1 = st.sidebar.text_input("Username")
        user_pass1 = st.sidebar.text_input("Password", type="password")
        if st.sidebar.checkbox("Signup"):
            if user_name1 == "" or user_pass1 == "":
                st.warning("Enter Valid Details")
            else:
                create_user_table()
                check = add_userdata(user_name1, user_pass1)
                if check:
                    st.success("You have successfully created an Account.Go to the Login Page in Credentials at sidebar")


def main():
    st.title("HeartDisease Prediction")
    title_image = Image.open('title.png')
    st.image(title_image)
    db_main()


if __name__ == "__main__":
    main()
