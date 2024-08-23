import pandas as pd
import numpy as np
import streamlit as st
import pickle
import tensorflow as tf
from sklearn.preprocessing import StandardScaler,LabelEncoder,OneHotEncoder

#Load the trained model
model= tf.keras.models.load_model('model.h5')

#Load trained model, scaler pickle,one hot
with open('label_encoder_gender.pkl','rb') as file:
    label_encoder_gender=pickle.load(file)
with open('oneHot_encoder_geography.pkl','rb') as file:
    onehot_encoder_geography=pickle.load(file)
with open('scaler.pkl','rb') as file:
    scaler=pickle.load(file)

#Streamlit app
st.title('Customer Churn Prediction')
#user input
geography=st.selectbox('Geography',onehot_encoder_geography.categories_[0])
gender=st.selectbox('Gender',label_encoder_gender.classes_)
age=st.slider('Age',18,95)
balance=st.number_input('Balance')
credit_score=st.number_input('Credit Score')
estimated_salary=st.number_input('Estimated Salary')
tenure=st.slider('Tenure',0,10)
num_of_products=st.slider('Num Of Products',1,5)
has_cr_card=st.selectbox('Has Credit Card',[0,1])
is_active_member=st.selectbox('Is Active Member',[0,1])

#Prepare dataframe
input_data=pd.DataFrame({
    #'Geography': [],
    'CreditScore': [credit_score],
    'Gender': [label_encoder_gender.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary],
    })

geo_encoder= onehot_encoder_geography.transform([[geography]])
geo_encoder_df=pd.DataFrame(geo_encoder,columns=onehot_encoder_geography.get_feature_names_out(['Geography']))


#Merging one hot encoding to input data
input_data=pd.concat([input_data.reset_index(drop=True),geo_encoder_df],axis=1)

#Scale the input Data
input_scaled=scaler.transform(input_data)

#Predict churn

prediction= model.predict(input_scaled)
prediction_prob=prediction[0][0]

st.write(f'Churn Probability is {prediction_prob:.2f}')

if prediction_prob >0.5:
    st.write('The customer is likely to churn.')
else:
    st.write('The customer is not likely to churn.')