import datetime, pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar

# Creates an estimate of the number of weekly school days in the given range
def get_weekly_schooldays_est(start_year, end_year):
    
    # Generate all school days (weekdays Mon–Fri) for every school year from August to May
    all_days = []
    for year in range(start_year, end_year): # Loop through each school year
        school_year_days = pd.date_range(f"{year}-08-07", f"{year+1}-05-22", freq="B")
        all_days.extend(school_year_days)
    all_days = pd.DatetimeIndex(all_days)

    # Get all U.S. federal holidays observed dates for holidays
    cal = USFederalHolidayCalendar()
    holidays = cal.holidays(start=f"{start_year}-01-01", end=f"{end_year}-12-31")

    # Auburn school breaks
    school_breaks = []
    for year in range(start_year, end_year + 1):

        # Thanksgiving Break (Wed–Fri around 4th Thursday of Nov)
        thanksgiving_break = pd.date_range(f"{year}-11-26", f"{year}-11-29", freq="D")

        # October Holiday + Staff Development/Parent Conference Day (long weekend)
        october_holiday = pd.date_range(f"{year}-10-17", f"{year}-10-20", freq="D")

        # Christmas/Winter Break (~Dec 20 – Jan 3 following year)
        christmas_break = pd.date_range(f"{year}-12-20", f"{year+1}-01-03", freq="D")

        # Spring Break (mid-March)
        spring_break = pd.date_range(f"{year}-03-10", f"{year}-03-14", freq="D")

        # Add them all up
        school_breaks.extend(thanksgiving_break)
        school_breaks.extend(october_holiday)
        school_breaks.extend(christmas_break)
        school_breaks.extend(spring_break)

    # Combine federal holidays + Auburn breaks
    days_off = holidays.union(pd.DatetimeIndex(school_breaks))

    # Remove those days from schooldays
    school_days = all_days[~all_days.isin(days_off)]

    # Group into weeks
    df = pd.DataFrame({"Day": school_days}) # Wrap in a dateframe for organization
    df["DATE"] = df["Day"] - pd.to_timedelta(df["Day"].dt.weekday, unit="d") # Bring every day of the week back to Monday of that week
    weekly = df.groupby("DATE").size().reset_index(name="Schooldays") # Group all dates that have the same week start together

    # Remove summer weeks from total
    weekly = weekly[~weekly["DATE"].dt.month.isin([6, 7])]

    # Save as Excel file
    weekly["DATE"] = weekly["DATE"].dt.strftime("%Y-%m-%d")
    weekly.to_excel("data_downloads/Auburn_Weekly_Schooldays_Estimate.xlsx", sheet_name="School Days", index=False)
