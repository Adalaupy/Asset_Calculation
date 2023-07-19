## Table of contents
* [General Information](#general-information)
* [Step of using](#step-of-using)
* [Installation](#installation)
* [Room for Improvement](#room-for-improvementlimitation)
* [remark](#remark)


# General Information
This Project is created in hope of providing a general overview of my asset as well as keeping a historical financial record, all of the records are saved in an Excel file, through Python-flask, the data and the corresponding charts can be displayed in an HTML page, which also allows us to input some new records.

# Step of Using
1. Execute main.py
```
python main.py
```
2. input new asset/liability items into an Excel file through the HTML input item(Asset.xlsx)
3. all the records in the Excel file will be displayed in the table
4. the amount in your preferred currency will be shown in a new column
5. Filter the particular [Year-Month]
6. there are two charts and total net asset information displayed
- pie chart: the proportion of Asset amount and Liability amount (the filter will be reflected on this graph)
- line chart: how our asset change over time
- Net asset: Asset - Liability (the filter will be reflected on this information)


# Installation
```
pip install -r requirements.txt
```
 

# Room for Improvement/Limitation
- more filtering criteria
- more graphs to provide information
- only insert function but no update

# Remark
- source of currency exchange rate: currencyapi.com
