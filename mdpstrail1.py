# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 09:11:39 2024

@author: Akshay Ravella
"""

import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import time
from PIL import Image
import pandas as pd

st.set_page_config(page_title="Multiple Disease Prediction System", page_icon=":stethoscope:")

# loading the saved models
diabetes_model = pickle.load(open('diabetes_trained_model.sav', 'rb'))
cardiovascular_model = pickle.load(open('cardiovascular_trained_model.sav', 'rb'))
lungcancer_model = pickle.load(open('lungcancer_trained_model.sav', 'rb'))

# sidebar for navigation
with st.sidebar:
    selected = option_menu('Main Menu',
                          ['Home',
                           'Diabetes Prediction',
                           'Heart Disease Prediction',
                           'Lung Cancer Prediction',
                           'Others'],
                          icons=['house','activity', 'heart', 'person', 'three-dots'],
                          default_index=0)

def send_disease_diagnosis_email(name, email, disease, diagnosis):
    sender_name = "noreply.mdps"
    sender_email = "akshayravella1@gmail.com"  
    sender_password = "fuyq wyjl cgnn wbpw"  

    subject = f"Thank You for using Multiple Disease Prediction Web App - {disease} Diagnosis"
    color = "red" if diagnosis == "Positive" else "green"
    webpapp_url = "https://multiple-disease-prediction-system-by-team-a1.streamlit.app/"
    
    
    
    banner_urls = {
    'Diabetes': 'https://d2jx2rerrg6sh3.cloudfront.net/images/Article_Images/ImageForArticle_22744_16565132428524067.jpg',
    'Heart Disease': 'https://www.labiotech.eu/wp-content/uploads/2023/05/Cure-for-cardiovascular-diseases.jpg',
    'Lung Cancer': 'https://img.freepik.com/vetores-premium/pneumologia-pequenos-medicos-examinando-os-pulmoes-tuberculose-pneumonia-tratamento-ou-diagnostico-do-cancer-de-pulmao-inspecao-de-orgaos-internos-em-busca-de-doencas-doencas-ou-problemas-do-sistema-respiratorio_458444-446.jpg?w=1380'
    }
    
    banner = """<!-- Insert the banner image -->
    <img src="{}" alt="Banner Image" style="max-width: 100%; height: auto; margin-top: 20px;">
    """.format(banner_urls.get(disease, ''))
    
    # Image attachment paths
    attachment_paths = {
        'Diabetes': 'DIA2.jpg',
        'Heart Disease': 'HeartDisease.jpg',
        'Lung Cancer': 'LungCancer.jpg'
    }
    
    # Attach images
    image_attachment = MIMEImage(open(attachment_paths.get(disease), 'rb').read())
    image_attachment.add_header('Content-ID', f'<{disease}_image>')
    image_attachment.add_header('Content-Disposition', f'inline; filename="{disease}_infographics.jpg"')
    
    if disease == 'Diabetes':
        tips = """
        <p><strong><u>Tips for Diabetic Patients:</u></strong></p>
        <ol>
            <li><strong>Monitor Blood Sugar Levels:</strong><br>
            - Regularly check your blood glucose levels as advised by your healthcare provider.</li>
            <li><strong>Medication Adherence:</strong><br>
            - Take medications as prescribed by your healthcare provider.</li>
            <li><strong>Balanced Nutrition:</strong><br>
            - Adopt a diet rich in whole grains, lean proteins, fruits, and vegetables.</li>
            <li><strong>Regular Exercise:</strong><br>
            - Engage in physical activity like brisk walking, swimming, or cycling.</li>
            <li><strong>Mindful Stress Management:</strong><br>
            - Practice stress-reducing techniques, such as mindfulness, meditation, or yoga.</li>
        </ol>
        <p><strong><u>Tips for Diabetes Prevention:</u></strong></p>
        <ol>
            <li><strong>Healthy Dietary Choices:</strong><br>
            - Consume a well-balanced diet with a focus on fruits, vegetables, whole grains, and lean proteins.<br>
            - Limit the intake of processed foods, sugary drinks, and high-fat items.</li>
            <li><strong>Regular Physical Activity:</strong><br>
            - Engage in regular physical activity to maintain a healthy weight and improve insulin sensitivity.</li>
            <li><strong>Weight Management:</strong><br>
            - Aim for a body mass index (BMI) within the normal range.<br>
            - Even a small reduction in weight can significantly lower the risk of diabetes.</li>
            <li><strong>Reduce Sedentary Time:</strong><br>
            - Minimize sitting time and incorporate more movement into your daily routine.</li>
            <li><strong>Routine Health Check-ups:</strong><br>
            - Schedule regular check-ups to monitor overall health and detect any potential issues early on.</li>
        </ol>
        <p>**It's important to note that these tips should be personalized based on individual health conditions and preferences. Consultation with healthcare professionals is crucial for tailored advice and management.</p>
        """
    elif disease == 'Heart Disease':
        tips = """
    <p><strong><u>Tips for Heart Health:</u></strong></p>
    <ol>
        <li><strong>Heart-Healthy Diet:</strong><br>
        - Choose a diet rich in fruits, vegetables, whole grains, and lean proteins.<br>
        - Limit saturated and trans fats, cholesterol, and sodium.</li>
        <li><strong>Regular Exercise:</strong><br>
        - Engage in aerobic exercises like walking, jogging, or swimming for at least 150 minutes per week.<br>
        - Include strength training exercises to improve overall cardiovascular health.</li>
        <li><strong>Manage Blood Pressure:</strong><br>
        - Monitor blood pressure regularly and follow your healthcare provider's recommendations.<br>
        - Maintain a healthy weight and limit alcohol intake.</li>
        <li><strong>Quit Smoking:</strong><br>
        - If you smoke, quit. Smoking is a major risk factor for heart disease.</li>
        <li><strong>Manage Stress:</strong><br>
        - Practice stress-reducing techniques such as deep breathing, meditation, or yoga.</li>
    </ol>
    <p><strong><u>Preventing Heart Disease:</u></strong></p>
    <ol>
        <li><strong>Regular Health Check-ups:</strong><br>
        - Monitor cholesterol levels, blood pressure, and other cardiovascular risk factors.<br>
        - Follow your healthcare provider's advice for preventive screenings.</li>
        <li><strong>Limit Alcohol Intake:</strong><br>
        - If you drink alcohol, do so in moderation.</li>
        <li><strong>Maintain Optimal Blood Sugar Levels:</strong><br>
        - Keep blood sugar levels within the recommended range, as diabetes can contribute to heart disease.</li>
        <li><strong>Stay Hydrated:</strong><br>
        - Maintain proper hydration for overall health and heart function.</li>
    </ol>
    <p>**Note: Individualized advice from healthcare professionals is essential for optimal heart health.</p>
    """
    elif disease == "Lung Cancer":
        tips = """
    <p><strong><u>Tips for Lung Cancer:</u></strong></p>
    <ol>
        <li><strong>Avoid Smoking:</strong><br>
        - The most significant risk factor for lung cancer is smoking. Quitting smoking is the best preventive measure.</li>
        <li><strong>Radon Exposure:</strong><br>
        - Test your home for radon, a naturally occurring gas that can contribute to lung cancer.</li>
        <li><strong>Protect Against Workplace Carcinogens:</strong><br>
        - If you work in an industry with exposure to carcinogens, use protective equipment and follow safety guidelines.</li>
        <li><strong>Healthy Diet:</strong><br>
        - Consume a diet rich in fruits and vegetables, which may have protective effects against certain cancers.</li>
        <li><strong>Regular Exercise:</strong><br>
        - Engage in regular physical activity to maintain overall health.</li>
    </ol>
    <p><strong><u>Early Detection and Screening:</u></strong></p>
    <ol>
        <li><strong>Know the Symptoms:</strong><br>
        - Be aware of symptoms like persistent cough, chest pain, and unexplained weight loss. Consult a healthcare professional if you experience these.</li>
        <li><strong>Limit Alcohol Consumption:</strong><br>
        - If you consume alcohol, do so in moderation. Excessive alcohol intake is associated with an increased risk of various cancers, including lung cancer.</li>
        <li><strong>Regular Health Check-ups:</strong><br>
        - Schedule regular check-ups with your healthcare provider for early detection of potential health issues, including lung cancer.</li>
        <li><strong>Awareness and Education:</strong><br>
        - Stay informed about lung cancer risks and symptoms. Early awareness and seeking medical attention promptly can improve treatment outcomes.</li>
    </ol>
    <p>**Note: Individuals with specific risk factors or concerns should consult with healthcare professionals for personalized advice and management.</p>
    """
        

    body = f"Dear {name},<br><br>Thank you for using our Multiple Disease Prediction Web APP!<br><br><b>{disease} Test Result:</b> <b style='color:{color}'>{diagnosis}</b>{banner}{tips}<br>Connect with us for more information.<br><br>Web App Url: {webpapp_url}<br><br>Best regards,<br>Team A1"

    message = MIMEMultipart()
    message["From"] = f"{sender_name} <{sender_email}>"
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))
    
    # Attach the image to the email
    message.attach(image_attachment)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())

if selected == 'Home':
    
    
    image = Image.open("webapplogo6.png")
    st.image(image, use_column_width=True)
    st.markdown("""
    <p style='text-align:justify;'>
    This Web Application is designed to help users predict the likelihood of developing certain diseases based on their input features.
    With the use of trained and tested machine learning models, we provide predictions for <b>Diabetes</b>, <b>Heart Disease</b> and <b>Lung Cancer</b>.
    </p>
    """,unsafe_allow_html=True)
    
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image('https://img.freepik.com/premium-vector/doctors-testing-blood-glucose-using-glucometer-hypoglycemia-diabetes-diagnosis-laboratory-equipment-syringe-physician-measuring-sugar-level_284092-2708.jpg', use_column_width=True, caption='Diabetes Prediction')
        st.markdown(
        "<style>img{height:150px;}</style>",
        unsafe_allow_html=True
        )

    with col2:
        st.image('https://www.heart.org/-/media/Images/Around-the-AHA/2022-Top-10_SC.jpg', use_column_width=True, caption='Heart Disease Prediction')
        st.markdown(
        "<style>img{height:150px;}</style>",
        unsafe_allow_html=True
        )

    with col3:
        st.image('https://img.freepik.com/premium-vector/tiny-pulmonologists-examining-lungs-flat-vector-illustration-doctors-checking-respiratory-system-asthma-tuberculosis-diseases-diagnostic-internal-human-organs-medicine-healthcare-concept_74855-25361.jpg?w=2000', use_column_width=True, caption='Lung Cancer Prediction')
        st.markdown(
        "<style>img{height:150px;}</style>",
        unsafe_allow_html=True
        )
    
    st.subheader("*How to Use:*")
    st.write("""
    - Navigate to the Main Menu(>) located in the top-left corner of the screen.
    - Click on the desired tab among 'Diabetes Prediction', 'Heart Disease', and 'Lung Cancer' to access prediction tools for specific diseases.
    - Enter relevant information as requested in the input fields.
    - Click on the "Test Result" button to obtain predictions based on the provided data.
    """)
    st.subheader("*Disclaimer:*")
    st.write("""
    - This Web App may not provide accurate predictions at all times. When in doubt, please enter the values again and verify the predictions.
    - You are requested to provide your Name and Email for sending details about your test results. Rest assured, your information is safe and will be kept confidential.
    - It is important to note that individuals with specific risk factors or concerns should consult with healthcare professionals for personalized advice and management.
    """)   
    

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    
    tab1, tab2= st.tabs(["🩸Diabetes Diagnosis", "📋About Diabetes"])
    
    with tab2:
        st.header("All You Need to Know About Diabetes!",divider='rainbow')
        st.markdown("""
        <p style='text-align:justify;'>
        ● Diabetes is a chronic condition that affects how your body utilizes blood sugar (glucose). Insulin, a hormone produced by the pancreas, helps regulate glucose levels. 
        In diabetes, the body either doesn't produce enough insulin or can't effectively use the insulin it produces. As a result, glucose builds up in the bloodstream, leading to various health complications.
        </p>
        """, unsafe_allow_html=True)
        st.markdown("""
        <p style='text-align:justify;'>
        ● There are two main types of diabetes: Type 1 and Type 2. Type 1 diabetes occurs when the immune system mistakenly attacks and destroys insulin-producing cells in the pancreas. 
        Type 2 diabetes, more common in adults, occurs when the body becomes resistant to insulin or doesn't produce enough to maintain normal glucose levels.
        Both types can lead to elevated blood sugar levels, causing symptoms such as excessive thirst, frequent urination, fatigue, and blurred vision etc.
        </p>
        """, unsafe_allow_html=True)
        st.write("● Below table provides target blood glucose level ranges:")
        image = Image.open("type12.png")
        st.image(image, use_column_width=True)
        st.write("● Below table provides Blood sugar levels in diagnosing diabetes:")
        image = Image.open("diabdignosis.png")
        st.image(image, use_column_width=True)
        
        with open("DIA2.jpg", "rb") as file:
            btn = st.download_button(
                label="Download Diabetes Infographics",
                data=file,
                file_name="Diabetes_Infographics.png",
                mime="image/png"
              )
        
        
        
    with tab1:
        # page title
        st.title('Diabetes Prediction')  
        
        name = st.text_input("Enter Your Name")
        email = st.text_input("Enter Your Email")
        if not name or not email:
            st.warning('Please enter both Name and Email to proceed!', icon="⚠️")
            st.stop()

        if not email.endswith('@gmail.com'):
            st.error("Invalid email address!", icon="❌")
            st.stop()
            
        # getting the input data from the user
        col1, col2, col3 = st.columns(3)
        with col1:
            sex = st.selectbox('Gender',('Male','Female'))
        with col2:
            Pregnancies = st.text_input('Number of Pregnancies')
        with col3:
            Glucose = st.text_input('Glucose Level')
        with col1:
            BloodPressure = st.text_input('Blood Pressure Value')
        with col2:
            SkinThickness = st.text_input('Skin Thickness Value')
        with col3:
            Insulin = st.text_input('Insulin Level')
        with col1:
            BMI = st.text_input('BMI value')
        with col2:
            DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function Value')
        with col3:
            Age = st.text_input('Enter Your Age')
        # code for Prediction
        diab_diagnosis = ''
        # creating a button for Prediction
        if st.button('Diabetes Test Result'):
            diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
            if diab_prediction[0] == 1:
                diab_diagnosis = 'Test Result: Positive'
                send_disease_diagnosis_email(name, email, 'Diabetes', 'Positive')
                with st.spinner('Please wait, loading...'):
                    time.sleep(2)
                    st.error(diab_diagnosis)
            else:
                diab_diagnosis = 'Test Result: Negative'
                send_disease_diagnosis_email(name, email, 'Diabetes', 'Negative')
                with st.spinner('Please wait, loading...'):
                    time.sleep(2)
                    st.success(diab_diagnosis)
            
            with st.expander("**Click here to see Test Report**"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write("**Patient Name**: ",name)
                with col2:
                    st.write("**Gender**: ",sex)
                with col3:
                    st.write("**Age**: ",Age)
                test_report_diabetes = {
                'Parameter Name': ['Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness', 'Insulin', 'BMI', 'Diabetes Pedigree Function'],
                'Patient Values': [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction],
                'Normal Range': ['0-10', '70-125', '120/80', '8-25', '25-250', '18.5-24.9', '< 1'],
                'Unit': ['Number', 'mg/dL', 'mmHg', 'mm', 'mIU/L', 'kg/m^2', 'No units']
                }
    
                # Displaying the table                             
                st.table(pd.DataFrame(test_report_diabetes))    
                st.info('Do check your email for more details, Thank You.', icon="ℹ️")
                
# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    
    tab1, tab2= st.tabs(["🫀Heart Diagnosis", "📋About Heart Disease"])
    
    with tab2:
        st.header("All You Need to Know About Heart Disease!",divider='rainbow')
        st.write("Heart disease, also known as cardiovascular disease (CVD), is a group of conditions that affect the heart and blood vessels.")
        st.subheader("What are the symptoms of heart disease?")
        st.write("Sometimes heart disease may be “silent” and not diagnosed until a person experiences signs or symptoms of a heart attack, heart failure, or an arrhythmia.")
        st.subheader("What are the risk factors for heart disease?")
        st.markdown("""
        <p style='text-align:justify;'>
        High blood pressure, high blood cholesterol, and smoking are key risk factors for heart disease. Several other medical conditions and lifestyle choices can also put people at a higher risk for heart disease, including:
        </p>
        """, unsafe_allow_html=True)
        st.write("• Diabetes")
        st.write("• Overweight and obesity")
        st.write("• Unhealthy diet")
        st.write("• Physical inactivity")
        st.write("• Excessive alcohol use")
        with open("HeartDisease.jpg", "rb") as file:
            btn = st.download_button(
                label="Download HeartDisease Infographics",
                data=file,
                file_name="CVD_Infographics.png",
                mime="image/png"
              )
        
    
    with tab1:
        # page title
        st.title('Heart Disease Prediction')
        
        name = st.text_input("Enter Your Name")
        email = st.text_input("Enter Your Email")
        if not name or not email:
            st.warning('Please enter both Name and Email to proceed!', icon="⚠️")
            st.stop()

        if not email.endswith('@gmail.com'):
            st.error("Invalid email address!", icon="❌")
            st.stop()
            
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.text_input('Enter your Age')
        with col2:
            gender = st.selectbox('Select your Gender',('Male','Female'))
            if(gender=='Male'):
                 gender=2
            else:
                 gender=1
        with col3:
            height = st.text_input('Enter your Height (in centimeters)')
        with col1:
            weight = st.text_input('Enter your Weight (in kilograms)')
        with col2:
            ap_hi = st.text_input('Enter your Systolic Blood Pressure')
        with col3:
            ap_lo = st.text_input('Enter your Diastolic Blood Pressure')
        with col1:
            cholesterol = st.selectbox('Select your Cholesterol Level',('Normal','Above Normal','High'))
            if(cholesterol=='Normal'):
                cholesterol=1
            elif(cholesterol=='Above Normal'):
                cholesterol=2
            else:
                cholesterol=3
        with col2:
            gluc = st.selectbox('Select your Glucose Level',('Normal','Above Normal','High'))
            if(gluc=='Normal'):
                gluc=1
            elif(gluc=='Above Normal'):
                gluc=2
            else:
                gluc=3
        with col3:
            smoke = st.selectbox('Do you smoke?',('Yes','No'))
            if(smoke=='Yes'):
                smoke=1
            else:
                smoke=0
        with col1:
            alco = st.selectbox('Do you consume alcohol?',('Yes','No'))
            if(alco=='Yes'):
                alco=1
            else:
                alco=0
        with col2:
            active = st.selectbox('Select your Physical Activity Level',('Low','Moderate','High'))
            if(active=='Low'):
                active=0
            elif(active=='Moderate'):
                active=1
            else:
                active=1
        with col3:
            verification = st.selectbox('Have you verified all the values?',('Yes','No'))
        
        # code for Prediction
        heart_diagnosis = '' 
        # creating a button for Prediction
        if st.button('Heart Disease Test Result'):
            user_input = [age,gender,height,weight,ap_hi,ap_lo,cholesterol,gluc,smoke,alco,active]
            user_input = [float(x) for x in user_input]
            heart_prediction = cardiovascular_model.predict([user_input])
            if heart_prediction[0] == 1:
                heart_diagnosis = 'Test Result: Positive'
                send_disease_diagnosis_email(name, email, 'Heart Disease', 'Positive')
                with st.spinner('Please wait, loading...'):
                    time.sleep(2)
                    st.error(heart_diagnosis)                    
            else:
                heart_diagnosis = 'Test Result: Negative'
                send_disease_diagnosis_email(name, email, 'Heart Disease', 'Negative')
                with st.spinner('Please wait, loading...'):
                    time.sleep(2)
                    st.success(heart_diagnosis)
            
            with st.expander("**Click here to see Test Report**"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write("**Patient Name**: ",name)
                with col2:
                    st.write("**Gender**: ",'Male' if gender == 2 else 'Female')
                with col3:
                    st.write("**Age**: ",age)
                test_report_heart_disease = {
                'Parameter Name': ['Height', 'Weight', 'Systolic Blood Pressure (mmHg)', 'Diastolic Blood Pressure (mmHg)', 'Cholesterol', 'Glucose', 'Smoking', 'Alcohol Intake', 'Physical Activity'],
                'Patient Value': [height, weight, ap_hi, ap_lo, 'Normal' if cholesterol == 1 else 'Above Normal' if cholesterol == 2 else 'High', 'Normal' if gluc == 1 else 'Above Normal' if gluc == 2 else 'High', 'Yes' if smoke == 1 else 'No', 'Yes' if alco == 1 else 'No', 'Low' if active == 0 else 'Moderate - High'],
                'Normal Range': ['>160 cm', '55-79 kg', '90-120 mmHg', '60-90 mmHg', 'Normal - Above Normal', 'Normal', 'No', 'No', 'Moderate - High'],
                
                }
                
                               
                st.table(pd.DataFrame(test_report_heart_disease))
                st.info('Do check your email for more details, Thank You.', icon="ℹ️")

      
        
# Lung Cancer Prediction Page
if selected == "Lung Cancer Prediction":
    
    tab1, tab2= st.tabs(["🫁Lung Cancer Diagnosis", "📋About Lung Cancer"])
    
    with tab2:
        
        st.header("All You Need to Know About Lung Cancer!",divider='rainbow')
        st.write("● Cancer is a disease in which cells in the body grow out of control. When cancer starts in the lungs, it is called lung cancer.")
        st.markdown("""
        <p style='text-align:justify;'>
        ● Lung cancer begins in the lungs and may spread to lymph nodes or other organs in the body, such as the brain. 
        Cancer from other organs also may spread to the lungs. When cancer cells spread from one organ to another, they are called metastases.
        </p>
        """, unsafe_allow_html=True)
        st.subheader("What Are the Symptoms of Lung Cancer?")
        st.markdown("""
        <p style='text-align:justify;'>
        Different people have different symptoms for lung cancer. Some people have symptoms related to the lungs. Some people whose lung cancer has spread to other parts of the body (metastasized) have symptoms specific to that part of the body. 
        Some people just have general symptoms of not feeling well. Most people with lung cancer don’t have symptoms until the cancer is advanced. Lung cancer symptoms may include
        </p>
        """, unsafe_allow_html=True)
        st.write("• Coughing that gets worse or doesn’t go away.")
        st.write("• Chest pain.")
        st.write("• Shortness of breath.")
        st.write("• Wheezing.")
        st.write("• Feeling very tired all the time.")
        st.write("• Weight loss with no known cause.")
        with open("LungCancer.jpg", "rb") as file:
            btn = st.download_button(
                label="Download Lung Cancer Infographics",
                data=file,
                file_name="LungCancer_Infographics.png",
                mime="image/png"
              )
        
        
        
    with tab1:
        
        # page title
        st.title("Lung Cancer Prediction")
        
        name = st.text_input("Enter Your Name")
        email = st.text_input("Enter Your Email")
        if not name or not email:
            st.warning('Please enter both Name and Email to proceed!', icon="⚠️")
            st.stop()

        if not email.endswith('@gmail.com'):
            st.error("Invalid email address!", icon="❌")
            st.stop()
            
        col1, col2, col3, col4, col5 = st.columns(5)
        with col2:
            GENDER = st.selectbox('Select your Gender',('Male','Female'))
            if(GENDER=='Male'):
                 GENDER=1
            else:
                 GENDER=0
        with col1:
            AGE = st.text_input(' Enter your Age')
        with col3:
            SMOKING = st.selectbox('Do you smoke?',('Yes','No'))
            if(SMOKING=='Yes'):
                SMOKING=1
            else:
                SMOKING=0
        with col4:
            YELLOW_FINGERS = st.selectbox('Have yellow fingers?',('Yes','No'))
            if(YELLOW_FINGERS=='Yes'):
                YELLOW_FINGERS=1
            else:
                YELLOW_FINGERS=0
        with col5:
            ANXIETY	 = st.selectbox('Anxiety?',('Yes','No'))
            if(ANXIETY	=='Yes'):
                ANXIETY	=1
            else:
                ANXIETY	=0
        with col1:
            PEER_PRESSURE = st.selectbox('Do you feel peer pressure?',('Yes','No'))
            if(PEER_PRESSURE=='Yes'):
                PEER_PRESSURE=1
            else:
                PEER_PRESSURE=0
        with col2:
            CHRONIC_DISEASE = st.selectbox('Do you have any chronic diseases?',('Yes','No'))
            if(CHRONIC_DISEASE=='Yes'):
                CHRONIC_DISEASE=1
            else:
                CHRONIC_DISEASE=0
        with col3:
            FATIGUE = st.selectbox('Do you experience fatigue?',('Yes','No'))
            if(FATIGUE=='Yes'):
                FATIGUE=1
            else:
                FATIGUE=0
        with col4:
            ALLERGY = st.selectbox('Do you have any allergies? ',('Yes','No'))
            if(ALLERGY=='Yes'):
                ALLERGY=1
            else:
                ALLERGY=0
        with col5:
            WHEEZING = st.selectbox('Do you experience wheezing?',('Yes','No'))
            if(WHEEZING=='Yes'):
                WHEEZING=1
            else:
                WHEEZING=0
        with col1:
            ALCOHOL_CONSUMING = st.selectbox('Do you consume alcohol?',('Yes','No'))
            if(ALCOHOL_CONSUMING=='Yes'):
                ALCOHOL_CONSUMING=1
            else:
                ALCOHOL_CONSUMING=0
        with col2:
            COUGHING = st.selectbox('Do you have a persistent cough?',('Yes','No'))
            if(COUGHING=='Yes'):
                COUGHING=1
            else:
                COUGHING=0
        with col3:
            SHORTNESS_OF_BREATH = st.selectbox('Do you experience shortness of breath?',('Yes','No'))
            if(SHORTNESS_OF_BREATH=='Yes'):
                SHORTNESS_OF_BREATH=1
            else:
                SHORTNESS_OF_BREATH=0
        with col4:
            SWALLOWING_DIFFICULTY = st.selectbox('Do you have difficulty swallowing?',('Yes','No'))
            if(SWALLOWING_DIFFICULTY=='Yes'):
                SWALLOWING_DIFFICULTY=1
            else:
                SWALLOWING_DIFFICULTY=0
        with col5:
            CHEST_PAIN = st.selectbox('Do you experience chest pain?',('Yes','No'))
            if(CHEST_PAIN=='Yes'):
                CHEST_PAIN=1
            else:
                CHEST_PAIN=0
        
        # code for Prediction
        lungcancer_diagnosis = ''
        # creating a button for Prediction
        if st.button("Lung Cancer Test Result"):
            user_input = [GENDER, AGE, SMOKING, YELLOW_FINGERS, ANXIETY, PEER_PRESSURE, CHRONIC_DISEASE, FATIGUE, ALLERGY, WHEEZING, ALCOHOL_CONSUMING, COUGHING, SHORTNESS_OF_BREATH, SWALLOWING_DIFFICULTY, CHEST_PAIN]
            user_input = [float(x) for x in user_input]
            lungcancer_prediction = lungcancer_model.predict([user_input])
            if lungcancer_prediction[0] == 1:
                lungcancer_diagnosis = "Test Result: Positive"
                send_disease_diagnosis_email(name, email, 'Lung Cancer', 'Positive')
                with st.spinner('Please wait, loading...'):
                    time.sleep(2)
                    st.error(lungcancer_diagnosis)
            else:
                lungcancer_diagnosis = "Test Result: Negative"
                send_disease_diagnosis_email(name, email, 'Lung Cancer', 'Negative')
                with st.spinner('Please wait, loading...'):
                    time.sleep(2)
                    st.success(lungcancer_diagnosis)
                    
            
            with st.expander("**Click here to see Test Report**"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write("**Patient Name**: ",name)
                with col2:
                    st.write("**Gender**: ",'Male' if GENDER == 1 else 'Female')
                with col3:
                    st.write("**Age**: ",AGE)
                
                lungcancer_test_report = {
                'Parameter Name': ['Smoking', 'Yellow Fingers', 'Anxiety', 'Peer Pressure', 'Chronic Disease', 'Fatigue', 'Allergy', 'Wheezing', 'Alcohol Consuming', 'Coughing', 'Shortness of Breath', 'Swallowing Difficulty', 'Chest Pain'],
                'Patient Value': ['Yes' if SMOKING == 1 else 'No', 'Yes' if YELLOW_FINGERS == 1 else 'No', 'Yes' if ANXIETY == 1 else 'No', 'Yes' if PEER_PRESSURE == 1 else 'No', 'Yes' if CHRONIC_DISEASE == 1 else 'No', 'Yes' if FATIGUE == 1 else 'No', 'Yes' if ALLERGY == 1 else 'No', 'Yes' if WHEEZING == 1 else 'No', 'Yes' if ALCOHOL_CONSUMING == 1 else 'No', 'Yes' if COUGHING == 1 else 'No', 'Yes' if SHORTNESS_OF_BREATH == 1 else 'No', 'Yes' if SWALLOWING_DIFFICULTY == 1 else 'No', 'Yes' if CHEST_PAIN == 1 else 'No'],
                'Normal Value': ['No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No']
                }
                
                # Displaying the table
                st.table(pd.DataFrame(lungcancer_test_report))
                st.info('Do check your email for more details, Thank You.', icon="ℹ️")
        
    
            

if selected == "Others":
    tab1, tab2, tab3 = st.tabs(["🧑‍🧑‍🧒‍🧒About Us","💬 Feedback", "📩 Contact"])
    
    with tab1:
        st.subheader("Discover Our Team", divider='rainbow')
        st.write("As a team of passionate individuals, we embarked on a journey to create a user-friendly and efficient application to predict diseases such as *Diabetes*, *Heart Disease* and *Lung Cancer*.")
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Team Members:**")
            st.write("• R. Akshay")
            st.write("• K. Pragna")
            st.write("• T. Jasritha")
            st.write("• G. Durga Prasad")
        with col2:
            st.info("**Guide:**")
            st.write("• Dr. CH. Pulla Rao, M.Tech, Ph.D")
            st.write("• Our mentor and guide, whose invaluable support and expertise have been instrumental in shaping this project.")
        st.divider()
        st.markdown("""
        <p style='text-align:justify;'>
        Throughout the development process, we have combined our diverse skills and knowledge to deliver a robust and accurate disease prediction system. 
        We are committed to promoting health awareness and providing a valuable tool for individuals to assess their health risks.
        </p>
        """, unsafe_allow_html=True)
        st.success("Thank you for choosing our Multiple Disease Prediction Web App. We hope it proves to be a valuable resource for you and others.")
        st.balloons()
        

        
    with tab2:
        import requests
        st.subheader("Your Feedback is Valuable!", divider='rainbow')
        
        def send_rating(rating_value):
            access_key_web3forms = "d5fb081b-63d5-4ab1-947a-a2d8d019bdcd"
            url = "https://api.web3forms.com/submit"
            data = {
                'access_key': access_key_web3forms,
                'rating': '★' * rating_value
            }
            response = requests.post(url, data=data)
            if response.status_code == 200:
                st.success("Thanks for rating!")
            else:
                st.error("Failed to send rating, Please try again.")
                st.markdown(f"If you continue to persist with the same issue, you can send your rating by [clicking here](https://app.formbricks.com/s/cltpfumwa0nm4czmeixlfgxu1)", unsafe_allow_html=True)
        
        # A rating scale using buttons
        st.write("Please rate your overall experience in using our Web App")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Send rating when a button is clicked
        if col1.button("★"):
            send_rating(1)
        elif col2.button("★★"):
            send_rating(2)
        elif col3.button("★★★"):
            send_rating(3)
        elif col4.button("★★★★"):
            send_rating(4)
        elif col5.button("★★★★★"):
            send_rating(5)
        
        #user feedback
        access_key = "701c8b0b-5c2d-4684-970f-85bf6a537d49"
        user_message = st.text_area("Have questions or suggestions? We'd love to hear from you.", height=80, placeholder="Type here...")
        
        if st.button("Submit"):
            url = "https://api.web3forms.com/submit"
            data = {
                'access_key': access_key,
                'feedback': user_message
                }
            response = requests.post(url, data=data)
            if response.status_code == 200:
                st.success("Feedback sent successfully, Thank you!")
            
            else:
                st.error("Failed to send message, Please try again.")
                st.markdown(f"If you continue to persist with the same issue, you can submit your feedback by [clicking here](https://app.formbricks.com/s/cltk8kyjh3ytlrfnjf2prdavt)", unsafe_allow_html=True)
                
    with tab3:
        
        st.subheader("Reach Out to Us", divider = 'rainbow')
        team_contacts = {
        "Akshay": "akshayravella1@gmail.com",
        "Pragna": "kolakaluripragna@gmail.com",
        "Jasritha": "jasritha02@gmail.com",
        "Durga Prasad": "durgaprasadgottipalli@gmail.com",        
        }

        # Displaying contact details using st.write
        for member, email in team_contacts.items():
            st.write(f"{member}: [{email}](mailto:{email})")
            
                   

# Set background image using HTML and CSS
st.markdown(
    f"""
    <style>
        body {{
            background: url('https://equineteurope.org/wp-content/uploads/2021/06/illustration.jpg') no-repeat center center fixed;
            background-size: cover;
            opacity: 0.875;
        }}
    </style>
    """,
    unsafe_allow_html=True
)    
    
       






        
       


  