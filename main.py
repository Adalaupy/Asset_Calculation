from flask import Flask,render_template,request
import pandas as pd
import requests
from datetime import date
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np


app = Flask(__name__)



def exchange_rate(Curr,Amt):

    if Curr != "HKD":
        
        response = requests.get('https://api.currencyapi.com/v3/latest?apikey=cur_live_NTtqzaW17MpIrbqjCoTlzNRqSgfi2Yf1FySwH2dj')

        data = response.json()['data']

        HK_rate = data['HKD']['value']
        other_rate = data[Curr]['value']

        Amt_in_HKD =float(Amt) * float(HK_rate) / float(other_rate)

    else:
        
        Amt_in_HKD = float(Amt)
        
    
    return round(Amt_in_HKD,2)



def Summary(df,df_selected,is_Filter):


    if is_Filter == 1:
        
        cal_df = df_selected.copy()

        time_ind = " selected period's "
    
    else:
        latest = df_selected['YearMonth'].max()
        cal_df = df[df['YearMonth'] == int(latest)].copy()

        time_ind = " current "
    
    
    cal_df['New_Amt'] = cal_df.apply(lambda row: row['Amount in HKD'] if row['Type'] == "Asset" else row['Amount in HKD']* -1 ,axis=1)


    Sum_asset = cal_df['New_Amt'].sum()

    cal_df.drop('New_Amt',axis=1)

    
    return round(Sum_asset,2),time_ind





def chart(df,df_selected,is_Filter):

    #pie chart

    if is_Filter == 1:


        df_selected = df_selected
        sum_by_type = df_selected.groupby('Type')['Amount'].sum()

        pie_chart  = plt.figure(figsize=(5,4))
        plt.pie(sum_by_type.values, labels=sum_by_type.index, autopct="%1.1f%%")
        plt.title("Proportion of Amount by Type")

    else:

        latest = df_selected['YearMonth'].max()
        sum_df = df[df['YearMonth'] == int(latest)]
        sum_by_type = sum_df.groupby('Type')['Amount'].sum()

        pie_chart  = plt.figure(figsize=(5,4))
        plt.pie(sum_by_type.values, labels=sum_by_type.index, autopct="%1.1f%%")
        plt.title("Proportion of Amount by Type (the Latest snapshot)")


    pie_file = BytesIO()
    pie_chart.savefig(pie_file,format = 'png')
    pie_file.seek(0)
    pie_file = base64.b64encode(pie_file.getvalue()).decode('utf-8')

    
    

    # Line Chart
    cal_df = df.copy()
    cal_df['YearMonth'] = cal_df['YearMonth'].astype(str)
    cal_df['Amount'] = cal_df.apply(lambda row: row['Amount in HKD'] if row['Type'] == "Asset" else row['Amount in HKD']* -1 ,axis=1)

    sum_by_date = cal_df.groupby('YearMonth')['Amount'].sum().reset_index()
    

    line_chart = plt.figure(figsize=(5,4))
    plt.plot(sum_by_date['YearMonth'], sum_by_date['Amount'])
    plt.title('Change of Amount')
    plt.xlabel('YearMonth')
    plt.ylabel('Amount')
    

    line_file = BytesIO()
    line_chart.savefig(line_file, format='png')
    line_file.seek(0)
    line_file = base64.b64encode(line_file.getvalue()).decode('utf-8')




        
        
    
    
    return pie_file , line_file



    





@app.route('/', methods = ['GET','POST'])
def index():

    is_Filter = 0

    ExcelName = 'Asset.xlsx'
    df = pd.read_excel(ExcelName)
    df = df.sort_values('YearMonth')
    df['Logdate'] = pd.to_datetime( df['Logdate'] ).dt.date


    df_selected = df.copy()    
    
    YearMonth_Option = df['YearMonth'].unique()



    if request.method == "POST":


        # Filter the Year Month
        select_date = request.form.get('YearMonth')
        
        if select_date:

            is_Filter = 1

            df_selected = df[df['YearMonth'] == int(select_date)]

        
        # Insert new Item        
        if request.form['yearmonth_input']:
    
            

            ins_YM = request.form['yearmonth_input']
            ins_src = request.form['source_input']
            ins_type = request.form['type_input']
            ins_amt = request.form['amt_input']
            ins_curr = request.form['curr_input']



            Amt_in_HKD = exchange_rate(ins_curr,ins_amt)
            logdate = date.today().strftime("%Y-%m-%d")



            InsertList = [int(ins_YM),ins_src,ins_type,float(ins_amt),ins_curr,float(Amt_in_HKD),logdate]
            
            df.loc[len(df)] = InsertList
            df = df.sort_values('YearMonth')
            df_selected = df.copy()    

            df.to_excel(ExcelName,index=False)


            YearMonth_Option = df['YearMonth'].unique()

    
    
        
    if len(df) > 0 :
        df = df.sort_values('YearMonth')
        

        # Calculate Total asset
        Sum_asset,time_ind = Summary(df,df_selected,is_Filter)


        PieChart,line_file = chart(df,df_selected,is_Filter)

    else:

        df = ""
        Sum_asset = ""
        PieChart = ""
        line_file = ""
        time_ind = ""

    return render_template('index.html', df = df_selected , YearMonth = YearMonth_Option, Sum_asset = Sum_asset, pie_data = PieChart, line_data = line_file , time_ind = time_ind)






if __name__ == "__main__":
    app.run(debug=True)
