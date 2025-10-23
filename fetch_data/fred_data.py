from pandas_datareader import data as web

# Determines which variable to fetch based on input parameters
def get_fred_variable(variable_name, start_year, end_year):

    # Gets an up-to-date Excel spreadsheet for CPI, UER, or EMHI from FRED website
    if variable_name == "cpi":
        series_ID = "CUUR0300SA0"
        xlsx_name = "CPI"
        sheet_name = "CPI Data"

    elif variable_name == "uer":
        series_ID = "ALLEEC5URN"
        xlsx_name = "UER"
        sheet_name = "UER Data"
        
    elif variable_name == "emhi":
        series_ID = "MHIAL01081A052NCEN"
        xlsx_name = "EMHI"
        sheet_name = "EMHI Data"

    # Query the FRED API
    fred_variable = web.DataReader(series_ID, "fred", start_year, end_year)
    
    # Convert into proper date format
    fred_variable.index = fred_variable.index.strftime("%Y-%m-%d")

    # Save as an Excel file
    fred_variable.to_excel(f"data_downloads/{xlsx_name}.xlsx", sheet_name=sheet_name)