from etl import data_types, time_series
from visualization import business_question, forecast
import pandas as pd
import streamlit as st


def main():
    # Read data
    data = pd.read_csv('./data/dataset.csv', sep=';')
    data_clean = data_types(data)

    st.title('Just a Little Data Challenge')
    select = st.sidebar.selectbox('Challange', ['Net Revenue Forecast', 'Net Revenue by Year', 'Gross Revenue by Year', 'Boxes by Year', 'Customer Acquisition Channel', 
                                'Nº Customer'])
   
    if select == 'Net Revenue Forecast':
        st.subheader('Forecast')
        data_series = time_series(data_clean)
        forecast(data_series)
    else:
        st.subheader('Business Questions')
        business_question(data_clean, select)


if __name__ == '__main__':
    main()