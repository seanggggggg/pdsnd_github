import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
# First change here: just add a comment line
# Second change comment
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("which city do you want to look at \n")
        if city.lower() in ['new york city', 'washington', 'chicago']:
            break
        else:
            print('You input a wrong city name, try it again')
            continue

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month do you want to get input for, January, February,....,June? If you have no specific preference, plz enter 'all' \n")
        if month.title() in ['January', 'February', 'March', 'April', 'May', 'June', 'All']:
            break
        else:
            print('you input a wrong month, plz try it again')
            continue          

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day do you want to get input for, Monday, Tuesday,....,Sunday? If you have no specific preference, plz enter 'all' \n")
        if day.title() in ['All','Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
            break
        else:
            print('you input a wrong day, plz try it again')
            continue                  

    print('-'*40)
    return city.lower(), month.title(), day.title()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    data = pd.read_csv(CITY_DATA[city.lower()])  # Select the correspondig city data
    # From the data, we noticed that the time data are not in datetime format, hence let's first convert that to datetime format, for future conversion into corresponding data month and day
    data['Start Time']= pd.to_datetime(data['Start Time'])
    data['month'] = data['Start Time'].dt.month  
    data['Day'] = data['Start Time'].dt.weekday_name
    
    # Now, we have got all those corresponding data for relevant information (including month name and day name)
    # What we need to do now is to correpondingly sift out the corresponding information for future usage
    if month.title() != 'All':
        # Note: dt.month --> returning a number, and we now need to convert month name into the index
        monthdict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6}
        target = monthdict[month]
        data =  data[data['month']==target] 
    
    # Now, let's deal with day:
    if day.title() !='All':
        data = data[data['Day']==day.title()]

    return data


def time_stats(data):
    """Displays statistics on the most frequent times of travel."""
    # Now, we are assuming that df is the filtered one
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    mostmonth = data['month'].value_counts(ascending=False).idxmax()
    print('most common month is ',mostmonth)

    # TO DO: display the most common day of week
    mostdayofweek = data['Day'].value_counts(ascending=False).idxmax()
    print('most common day is ',mostdayofweek)

    # TO DO: display the most common start hour
    data['hour'] = data['Start Time'].dt.hour
    mosthour = data['hour'].value_counts(ascending=False).idxmax()
    print("most common hour is ",mosthour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(data):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    moststart = data['Start Station'].value_counts(ascending=False).idxmax()
    print('most commonly used start station is ',moststart)

    # TO DO: display most commonly used end station
    mostend = data['End Station'].value_counts(ascending=False).idxmax()
    print('most commonly used end station is ',mostend)

    # TO DO: display most frequent combination of start station and end station trip
    temp = data.groupby(['Start Station','End Station']).size().sort_values(ascending=False).idxmax()
    print('most frequent combination is ',temp)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(data):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total = data['Trip Duration'].sum()/(60*60)
    print('total travel time is ',total,' hours')

    # TO DO: display mean travel time
    mean = data['Trip Duration'].mean()/60
    print('mean travel time:', mean, " minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(data):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    types = data['User Type'].value_counts()
    print('user types information is as following \n', types,'\n')

    # TO DO: Display counts of gender
    # Note here sometimes Gender column is not included:
    try:
      gender = data['Gender'].value_counts()
      print('gender count information is as following \n', gender)
    except:
      print("\n Not Available")

    # TO DO: Display earliest, most recent, and most common year of birth
    # Similarly to above:
    try:
      early = data['Birth Year'].min()
      print('\n earliest year is :', early)
    except:
      print("\n earliest year information not available")

    try:
      recent = data['Birth Year'].max()
      print('\n most recent year is :', recent)
    except:
      print("\n Most recent year information not available")

    try:
      common = data['Birth Year'].value_counts().idxmax()
      print('\n most common year is :', common)
    except:
      print("\n Most common year infromation not available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        answer = input('\nWould you like to see the raw data? Enter yes or no.\n')
        while answer.lower() == 'yes':
            print(df.head(5))
            answer = input('\nWould you like to see the raw data? Enter yes or no.\n')
            df = df.iloc[6:,:]
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
