import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import datetime
import capm_function




st.set_page_config(page_title = "CAPM " , page_icon = "chart_with_upwards-trend" , layout = 'wide')

st.title("Capital Asset pricing Model")

#getting input from user
col1,col2 = st.columns([1,1])

with col1:
          stock_list = st.multiselect("Choose 4 Stocks" , ('TSLA','APPL','NFLX','MSFT','MGM','AMZN','NVDA','GOOGL'),['TSLA','APPL','AMZN','GOOGL'])
with col2 :
          year = st.number_input("Number of Years" , 1 ,100)

#downloding data for sp500


 



end = datetime.date.today()
start = datetime.date(datetime.date.today().year-year, datetime.date.today().month,datetime.date.today().day)

SP500 = web.DataReader(['sp500'],'fred',start,end)

# print(SP500.tail())

stocks_df = pd.DataFrame()

for stock in stock_list:
        data = yf.download(stock , period = f'{year}y')
        stocks_df[f'{stock}'] = data['Close']

stocks_df.reset_index(inplace=True)
SP500.reset_index(inplace= True)
SP500.columns = ['Date' , 'sp500']
stocks_df['Date'] = stocks_df['Date'].astype('datetime64[ns]')
stocks_df['Date'] = stocks_df['Date'].apply(lambda x : str(x)[:10])
stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
stocks_df = pd.merge(stocks_df , SP500 , on ='Date' , how='inner')

col1,col2 = st.columns([1,1])
with col1:
        st.markdown("### Dataframe Head")
        st.dataframe(stocks_df.head() , use_container_width= True)
       
with col2:
        st.markdown("### Dataframe Tail")
        st.dataframe(stocks_df.tail() , use_container_width= True)


col1 , col2 = st.columns([1,1])
with col1:
        st.markdown("### Price of all the stocks")
        st.plotly_chart(capm_function.interactive_plot(stocks_df))
        
with col2:
        capm_function.normalize(stocks_df)
        st.markdown("### Price of all the stocks(Normalized)")
        st.plotly_chart(capm_function.interactive_plot(capm_function.normalize(stocks_df)))


stocks_daily_return = capm_function.daily_return(stocks_df)
print(stocks_daily_return.head())

beta = {}
alpha= {}

for i in stocks_daily_return.columns:
        if i !='Date' and i != 'sp500':
                b,a = capm_function.calculate_beta(stocks_daily_return,i)

                beta[i] = b
                alpha[i] = a


beta_df = pd.DataFrame(columns=['stock','Beta Value'])
beta_df['stock'] = beta.keys()
beta_df['Beta Value'] = [str(round(i,2)) for i in beta.values()]

with col1:
        st.markdown('### Calculated Beta value')
        st.dataframe(beta_df ,use_container_width= True)

rf = 0
rm = stocks_daily_return['sp500'].mean()*252

return_df = pd.DataFrame()
return_value = []

for stock,value in beta.items():
        return_value.append(str(round(rf+(value*(rm - rf)),2)))
return_df['stock'] = stock_list

return_df['Return Value'] = return_value

with col2:
        st.markdown('### Calculated Return using CAPM')

        st.dataframe(return_df , use_container_width=True)






