import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # get user input for city (chicago, new york city, washington).
    print('Eexplore some US bikeshare data')
    city = input('\nWhich city do you want to analyze? Please choose from Chicago, New York City and Washington: ').lower()
    while city not in ['chicago', 'new york city', 'washington']:
        print('\n{} does not exist in the database.\n'.format(city))
        city = input('\nPlease tell me about which city (chicago, new york city, washington) you want to analyze: ').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('\nPlease select which month (all, january, february, ... , june): ').lower()
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while month not in months:
        print('\n{} does not exist in the database.\n'.format(month))
        month = input('\nPlease select which month (all, january, february, ... , june): ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nPlease select which day of week (all, monday, tuesday, ... sunday): ').lower()
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while day not in days:
        print('\n{} does not exist in the database.\n'.format(day))
        day = input('\nPlease select which day of week (all, monday, tuesday, ... sunday): ').lower()

    print('-'*40)
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

    # read data for selected city, month and day and convert the datetype of date
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name #weekdya_name might not work for newer Pandas

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df.month == month]

    if day != 'all':
        df = df[df.day_of_week == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month: ', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day: ', common_day)

    # display the most common start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    print('Them most common start hour: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_sta = df['Start Station'].mode()[0]
    print('The most commonly used start station: ', common_start_sta)

    # display most commonly used end station
    common_end_sta = df['End Station'].mode()[0]
    print('The most commonly used end station: ', common_end_sta)

    # display most frequent combination of start station and end station trip
    combination_sta = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most frequent combination of start station and end station trip:\n', combination_sta)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    total_travel_time = df['Travel Time'].sum(axis=0)
    print('Total travel time: ', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Travel Time'].mean(axis=0)
    print('Mean travel time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        print('Earliest year of birth: ', df['Birth Year'].min())
        print('Most reach year of birth: ', df['Birth Year'].max())
        print('Most common year of birht: ', df['Birth Year'].mode()[0])
    except:
        print('The dataset dones not have info about birth year') # some of the dataset lack this

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

        more = input('\nDo you want to see the raw data? Enter yes or no.\n')
        i = 5
        while more.lower() == 'yes':
            print(df[i-5:i])
            i += 5
            more = input('\nDo you want to see more data? Enter yes or no.\n')


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
