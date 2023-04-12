import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# all the valid months and days for user inputs
month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
day_list = ['all', 'sunday', 'monday', 'tuesday','wednesday', 'thursday', 'friday', 'saturday' ]


def display_raw_data(df):
    i = 0
    while True: 
        show_raw_data = input("Would you like to see a sample 5 rows of raw data for Bike Share? (Y/N): \n").lower()
        if show_raw_data == 'y':
            print(df.iloc[i:i+5])
            i = i + 5
        elif show_raw_data == 'n':
            break
        else:
            print('The input should be Y or N. Please re-enter.')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input_val("Pick a city - chicago, new york city or washington:\n",'c')

    # get user input for month (all, january, february, ... , june)
    month = input_val("Pick a month from (january, february, march, april, may, june) or otherwise enter 'all': \n", 'm')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input_val("Pick a day from (sunday, monday, tuesday, wednesday, thursday, friday, saturday) or otherwise enter 'all': \n", 'd')

    print('-'*40)
    return city, month, day


# user input validation function
def input_val(user_ip, ip_type):
    while True:
        user_entered_ip = input(user_ip).lower()
        try:
            if user_entered_ip in ['chicago', 'new york city', 'washington'] and ip_type == 'c':
                break
            elif user_entered_ip in month_list and ip_type == 'm':
                break
            elif user_entered_ip in day_list and ip_type == 'd':
                break
            else:
                if ip_type == 'c':
                    print(" Input is invalid. Please enter: chicago, new york city or washington")
                if ip_type == 'm':
                    print(" Input is invalid. Please enter: january, february, march, april, may, june or all")
                if ip_type == 'd':
                    print("Input is invalid. Please enter: sunday, monday, tuesday, wednesday, thursday, friday, saturday or all")
        except ValueError:
            print("Wrong input entered. ")
    return user_entered_ip


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
    # load the data for the required city into the dataframe df
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the start time column to datestamp 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month, day of week and hour from Start Time to new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable 
    if month != 'all':
        # use the index of month list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month is: ', df['month'].mode()[0])

    # display the most common day of week
    print('Most common day is: ', df['day_of_week'].mode()[0])

    # display the most common start hour
    print('Most common hour is: ', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used start station is: ", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("Most commonly used end station is: ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    start_end_grp = df.groupby(['Start Station', 'End Station'])
    combination = start_end_grp.size().sort_values(ascending = False).head(1)
    print('Most frequent combination of start station and end station trip is: ', combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is: ', df['Trip Duration'].sum())
    
    # display mean travel time
    print('Mean travel time is: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The different types of users are: ', df['User Type'].value_counts())

    # Display counts of gender
    # Gender and Birth year are not in Washinton
    if city!= 'washington':
        print('Gender count is: ', df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print('Earliest year of birth is:', df['Birth Year'].min())
        print('Latest year of birth is:', df['Birth Year'].max())
        print('Most common year of birth is:', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    else:
        print('Washington city does not have gender and birth information')
        print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
