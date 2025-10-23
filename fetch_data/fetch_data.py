import datetime
from fred_data import get_fred_variable
from schooldays import get_weekly_schooldays_est
from snap_data import get_latest_snap_zip

# Update all data sources with one function
def update_all(start_year = 2015, end_year = None):
    
    # Get all data from 2015 to today by default
    if end_year is None:
        end_year = datetime.date.today().year

    # Fetches Consumer Price Index for All Urban Consumers
    get_fred_variable("cpi", start_year, end_year)

    # Fetches Unemployment Rate in Lee County, AL
    get_fred_variable("uer", start_year, end_year)

    # Fetches Estimate of Median Household Income for Lee County, AL
    get_fred_variable("emhi", start_year, end_year)

    # Generates an estimate for the number of weekly school days in given period
    get_weekly_schooldays_est(start_year, end_year)

    # Fetches the latest ZIP file for SNAP data
    get_latest_snap_zip()