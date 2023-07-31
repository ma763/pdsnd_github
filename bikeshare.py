import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = CITY_DATA.keys()
months = ["january", "february", "march", "april", "may", "june",
                    "july", "august", "september", "october", "november", "december", "all"]
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input("Enter a city (chicago, new york city, washington): ").strip().lower()
    while city not in cities:
        print("Invalid city. Please enter 'chicago', 'new york city', or 'washington'.")
        city = input("Enter a city (chicago, new york city, washington): ").strip().lower()
    month = input("Enter a month (January to December, or 'all'): ").strip().lower()
    while month not in months:
        print("Invalid month. Please enter a valid month name or 'all'.")
        month = input("Enter a month (January to December, or 'all'): ").strip().lower()
    day = input("Enter a day of the week (Monday to Sunday, or 'all'): ").strip().lower()
    while day not in days:
        print("Invalid day of the week. Please enter a valid day or 'all'.")
        day = input("Enter a day of the week (Monday to Sunday, or 'all'): ").strip().lower()
    return city, month, day

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while view_data=='yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()
    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # TO DO: display the most common month
    print('The most common month is '+str(months[df['month'].mode()[0]]).title())
    # TO DO: display the most common day of week
    print('The most common day of week is '+str(df['day_of_week'].mode()[0]))
    # TO DO: display the most common start hour
    print('The most common start hour is '+str(df['Start Time'].dt.hour.mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # TO DO: display most commonly used start station
    print('The most commonly used start station is '+str(df['Start Station'].mode()[0]))
    # TO DO: display most commonly used end station
    print('The most commonly used end station is '+str(df['End Station'].mode()[0]))
    # TO DO: display most frequent combination of start station and end station trip
    df['Start End Station Combination'] = df['Start Station']+' - '+df['End Station']
    print('The most most frequent combination of start station and end station trip is '+str(df['Start End Station Combination'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # TO DO: display total travel time
    def convert_seconds_to_time(seconds):
        # Calculate hours, minutes, and seconds
        hours = seconds // 3600
        remaining_seconds = seconds % 3600
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        return hours, minutes, seconds
    total_travel_time = df['Trip Duration'].sum()
    hours, minutes, seconds = convert_seconds_to_time(total_travel_time)
    print(f"The total travel time is {hours} hours, {minutes} minutes, and {seconds} seconds.")
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    hours, minutes, seconds = convert_seconds_to_time(mean_travel_time)
    print(f"The mean travel time is {hours} hours, {minutes} minutes, and {seconds} seconds.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # TO DO: Display counts of user types
    print('The different user types are:')
    for index, count in df['User Type'].value_counts().items():
        print(f"    {count} users with the user type of {index}")
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print('The counts of gender are:')
        for index, count in df['Gender'].value_counts().items():
            print(f"    {count} users with gender {index}")
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('The earliest year of birth is '+str(int(df['Birth Year'].min())))
        print('The most recent year of birth is '+str(int(df['Birth Year'].max())))
        print('The most common year of birth is '+str(int(df['Birth Year'].mode()[0])))
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
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()