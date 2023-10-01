import plotly.express as px
import streamlit as st
from statsmodels.tsa.arima.model   import ARIMA
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



def business_question(data, graph=None):
    # Aponte resultados de vendas por ano: Gross Revenue, Net Revenue, Boxes
    # Gross Revenue
    if graph == 'Gross Revenue by Year':
        aux = data[['gross_revenue', 'year']].groupby('year').sum().reset_index().copy()
        fig = px.bar(aux, x='year', y='gross_revenue', title='Gross Revenue by Year')
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Gross Revenue'
        )   
        st.plotly_chart(fig)

        # Table
        aux.columns = ['Year', 'Gross Revenue']
        aux['Gross Revenue'] = aux['Gross Revenue'].map('$ {:,.2f}'.format)
        st.table(aux)

    ## Net Revenue 
    elif graph == 'Net Revenue by Year':
        aux = data[['net_revenue', 'year']].groupby('year').sum().reset_index().copy()
        fig = px.bar(aux, x='year', y='net_revenue', title='Net Revenue by Year')
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Net Revenue'
        )   
        st.plotly_chart(fig)

        # Table
        aux.columns = ['Year', 'Net Revenue']
        aux['Net Revenue'] = aux['Net Revenue'].map('$ {:,.2f}'.format)
        st.table(aux)

    # Boxes
    elif graph == 'Boxes by Year':
        aux = data[['boxes', 'year']].groupby('year').sum().reset_index().copy()
        fig = px.bar(aux, x='year', y='boxes', title='Boxes by Year')
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Boxes'
        )   
        st.plotly_chart(fig)

        # Table
        aux.columns = ['Year', 'Boxes']
        st.table(aux)

    elif graph == 'Customer Acquisition Channel':
        #  Qual customer_acquisition_channel teve maior Ticket Médio em 2013 e em 2015?
        aux = data[data['year'].isin([2013, 2015])].copy()
        aux = aux[['year', 'gross_revenue', 'customer_acquisition_channel']].groupby(['year', 'customer_acquisition_channel']).mean().reset_index()
        fig = px.bar(aux, x='year', y='gross_revenue', color='customer_acquisition_channel', barmode='group', title='Average Ticket (2013, 2015)')
        st.plotly_chart(fig)
        
        # Table
        customers = round(pd.crosstab(index=aux['year'], columns=aux['customer_acquisition_channel'], values=aux['gross_revenue'], aggfunc='mean'), 1)
        customers['Paid Marketing'] = customers['Paid Marketing'].map('$ {:,.2f}'.format)
        customers['Referral'] = customers['Referral'].map('$ {:,.2f}'.format)
        st.table(customers)        
        

    elif graph == 'Nº Customer':
        # Número de clientes únicos por Ano e comparativo desse resultado 2013x2015
        # Slice Year
        aux_13_15 = data[data['year'].isin([2013, 2015])]
        # Count unique
        n_customers = aux_13_15.groupby('year').agg({'customer_id': pd.Series.nunique}).reset_index().copy()
        fig = px.bar(n_customers, x='year', y='customer_id', title='Customers by Year (2013 and 2015)')
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Customer'
        )   
        st.plotly_chart(fig)
        n_customers.columns = ['Year', 'Nº Customers']
        st.table(n_customers)


def forecast(data):
    # Model Definitino
    modelo_arima = ARIMA(data['net_revenue'], order=[2,1,0]).fit()
    # Forecast
    yhat_arima = modelo_arima.forecast(6)
    # Visualization
    fig = px.line(yhat_arima, x=yhat_arima.index, y=yhat_arima.values, title='Net Revenue Forecast')
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='$'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Total performance
    scenarios = pd.DataFrame({'Predictions': yhat_arima})
    scenarios['Worst Scenario'] = scenarios['Predictions'] - (scenarios['Predictions'] * 0.12)
    scenarios['Best Scenario'] = scenarios['Predictions'] + (scenarios['Predictions'] * 0.12)
    scenarios = pd.DataFrame(round(scenarios.sum())).reset_index().rename(columns={'index': 'Scenario', 0: 'Total 6 Months'})
    scenarios['Total 6 Months'] = scenarios['Total 6 Months'].map('$ {:,.2f}'.format)
    st.table(scenarios)
