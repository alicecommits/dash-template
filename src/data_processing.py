# importing libraries ----------------------------------------------------
import pandas as pd
pd.options.display.max_columns # display all df columns when printing
from datetime import datetime # for date formatting

DEBUG_df = False # for debug prints

# -------------------------- importing formatted dataframe -------------------------- #
import data_parsing_from_file
df = data_parsing_from_file.df


# ----------------------------------------------------------------------------------- #
# ------------------------------ date / time formatting ----------------------------- #

date_str_pattern = "%a, %d %b %Y, %H:%M:%S %Z" # to change given date format

# converts date str --> date object
df['some_datetime_obj'] = df.apply(lambda row: datetime.strptime(
    row["some_date_field"], date_str_pattern), axis = 1)

# extracts date into date and time columns as key(s) when merging
# note: datetime obj --> str useful to use to other dataframes 
# on datetime-based key
df[['date', 'date_str', 'time', 'time_str']] = df.apply(
    lambda row: [row['some_datetime_obj'].date(),
                 row['some_datetime_obj'].strftime('%Y-%b-%d'),
                 row['some_datetime_obj'].time(),
                 row['some_datetime_obj'].strftime('%H:%M:%S')], 
                 axis = 1, 
                 result_type ='expand')
df = df.sort_values(by=['time'], ascending = True)

# pd.to_datetime generates an object recognized by Dash overlay plots, 
# for a fixed datetime-based x-axis
df['time_pdobj'] = pd.to_datetime(df['time'],
                                    format ='%H:%M:%S', 
                                    errors = 'coerce')
if DEBUG_df:
    print('df after time formatting: ', df)

# ---------------------- formatting qty from str --> int ----------------------------- #
df["some_qty_field"] = df.apply(lambda row: int(row["some_qty_field"]), axis = 1)
if DEBUG_df:
    # should print <class 'numpy.int64'>
    print('type of qty field entries: ', type(df["some_qty_field"].iloc[0]))
    # print 1st 5 elts - change the nb for more or less.
    nb_to_preview = 5 
    print(f'preview df 1st {nb_to_preview} elts after qty str --> int: ', 
          df.head(nb_to_preview))

# ----------------------------------------------------------------------------------- #
# deep copying df at that stage for :
# > grouping by date (df_2_gb)
# > single daily plots
df_2 = df.copy() # default deep copy is True
if DEBUG_df:
    print('df_2 deep copied: ', df_2)

# ------------------data prep for use in overlay plots ------------------------------ #
# Grouping by date (date will be our Series, representing each plot)
df_gb = df_2.groupby("date", group_keys=True)
if DEBUG_df:
    print(df_gb)
    gb_groups = df_gb.groups
    print(gb_groups.keys())


# ----------------------------------------------------------------------------------- #
# ------------- data prep for use in Dash single plots + drop-down ------------------- #

# /!\ Although readable and easy to use, dispatching one master df into other dfs 
# is not memory-efficient.
def dispatch_daily_df(a_df, day_col_name):
    """
    > Inputs: a dataframe a_df, the name of the column containing the days
    > Output: a dict where { key = day : value = df d data points for the day }
    """
    dispatched_daily_df_dict = {}

    # to find the list of days contained in a_df without repeating the day
    days_series_unique = a_df[day_col_name].drop_duplicates()
    # append .sort_values(ascending = True) optionally
    
    for i, day in enumerate(days_series_unique):
        if DEBUG_df:
            print(f'processing {day} content as day number {i}...')
        
        df_for_a_day = a_df[ ( a_df[day_col_name] == day ) ] # filter per day
        dispatched_daily_df_dict[str(day)] = df_for_a_day

    return dispatched_daily_df_dict

df_dispatched_in_dict = dispatch_daily_df(df_2, 'date')
if DEBUG_df:
    print(df_dispatched_in_dict)


# ------------------------------------------------------------------------------------------------- #
# ----- APPENDICE : Alternative workaround to have a fully recognized ["00:00", "23:59]" axis ------
# For Dash, using pd.to_datetime instead of datetime module methods 
# solved the plotting difficulties
# In simple plotly graphs (e.g. living in Jupyter notebooks), 
# merging df (left) to a minuts_range of freq=1s (right) worked.

'''
Goal: overlay daily plots altogether
- For the overlay to be possible, the time column must contain 
all values in min on a certain time range.
- If the value is missing for a certain hh:mm time, 
then the value against it must be 'nan'
- this can be achieved by outer merging `df` (on the left)
to a time column (on the right) were the delta between
each entry is dt=1 min (seconds removed, '%H:%M' string used.)
'''

'''
minuts_df = pd.DataFrame(data = pd.date_range("00:00", "23:59", freq="1s").time, 
                         columns=["minuts_range"])
minuts_df['minuts_range_str'] = minuts_df.apply(
    lambda row: row['minuts_range'].strftime('%H:%M:%S'), axis = 1)
if DEBUG_df:
    print('minuts df: ', minuts_df.tail(5))

# Merging stage: IMPORTANT: LEFT = THE DF
# RIGHT = THE MINUTS DF ABOVE!
# NOT THE OTHER WAY AROUND
df = df.merge(minuts_df, how='outer', 
              right_on='minuts_range_str', 
              left_on='time_str')

if DEBUG_df:
    # to print 10 first elts
    print(f'df --> min merged 1st {nb_to_preview} elts: ', df.head(nb_to_preview))
    # to print 10 last elts
    print(f'df --> min merged last {nb_to_preview} elts: ', df.tail(nb_to_preview))

# conversion minuts_range_str --> minuts_range_obj
# pd.to_datetime is a datetime 'util' recognized by Dash, 
# not datetime module. Only using pd.to_datetime seems  
# to format the x axis appropriately to overlay the plots
time_pattern = "%H:%M"

df['minuts_range_pdobj'] = pd.to_datetime(df['minuts_range_str'],
                                          format ='%H:%M:%S', 
                                          errors = 'coerce')

# Dash pd.to_datetime conversion needed anyway
#df['minuts_range_pdobj'] = pd.to_datetime(df['minuts_range_str'], format = time_pattern)
df_overlay = df.sort_values(by=['minuts_range_pdobj'], ascending=True)

if DEBUG_df:
    print('pd.datetime time obj type: ', type(df['minuts_range_pdobj'].iloc[0]))
    print('final df for overlaid plots: ', df_overlay)
'''