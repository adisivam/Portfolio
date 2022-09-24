'''
Program Description: Weather app to get the temperature based on city name or zip code
Author: Kesav Adithya Venkidusamy
'''

#Change#:1
#Change(s) Made: Initial version
#Initial version date: 08/09/2021
#Author: Kesav Adithya Venkidusamy
#Due Date: 08/15/2021

#import statements
import requests

#Declaring the variables for API key and url

api_key = 'f49701fc35c7ea36d44e589ce480e139'
url = 'http://api.openweathermap.org/data/2.5/weather'

#Validate if zip/city entered by user is correct or wrong
def validatezipcity(zip_city, zip_city_flag,state_abbv=''):
    '''
    :param zip_city: Zip and city for which temperature needs to be checked
    :param zip_city_flag: Flag to denote if the parameter is zip or city
    :param state_abbv: Abbreviation of state to which city belongs to
    :return: If API returns 200, then this function return True; Else, False
    '''

    #Constructing URL to pass to API requests
    if zip_city_flag.lower() == 'zip':
        url_q = url + '?q=' + str(zip_city) + '&APPID=' + api_key
        response = requests.request("GET", url_q)
    elif zip_city_flag.lower() == 'city':
        url_q = url + '?q=' + str(zip_city+','+state_abbv+',us') + '&APPID=' + api_key
        response = requests.request("GET", url_q)

    #If response code is 200, then print API connection is successful and return True;
    # Else, print error message and return False
    if response.status_code != 200:
        if zip_city_flag.lower() == 'city':
            print("\nNot able to find any city associated with city name '{}' and state abbreviation '{}'. Please check and enter correct value".format(zip_city, state_abbv))
        else:
            print("\nNot able to find any city associated with zip code '{}'. Please check and enter correct value".format(zip_city))
        print('API connection is failed')
        return False
    else:
        print('API connection is successful for the given zip/city')
        return True

#API Call to get the weather for the city/zip entered by user
def weatherapi(zip_city, zip_city_flag,temp_unit):
    '''
    :param zip_city: Zip and city for which temperature needs to be checked
    :param zip_city_flag: Flag to denote if the parameter is zip or city
    :temp_unit: Measure of output temperature
    :return: Dictionary having temperature and city name
    '''

    #Constructing URL to pass to API requests
    if zip_city_flag.lower() == 'zip':
        if temp_unit.upper() == 'F':
            url_q = url + '?q=' + str(zip_city) + '&units=imperial&APPID=' + api_key
        elif temp_unit.upper() == 'C':
            url_q = url + '?q=' + str(zip_city) + '&units=metric&APPID=' + api_key
        else:
            url_q = url + '?q=' + str(zip_city) + '&APPID=' + api_key
    elif zip_city_flag.lower() == 'city':
        if temp_unit.upper() == 'F':
            url_q = url + '?q=' + str(zip_city+','+state_abbv+',us') + '&units=imperial&APPID=' + api_key
        elif temp_unit.upper() == 'C':
            url_q = url + '?q=' + str(zip_city+','+state_abbv+',us') + '&units=metric&APPID=' + api_key
        else:
            url_q = url + '?q=' + str(zip_city + ',' + state_abbv + ',us') + '&APPID=' + api_key

    #Get response and create a dictionary with temperature and city name
    response = requests.request("GET", url_q)
    response_dict = response.json()

    #Add temperature city and country from the response to the dictionary
    temp_detail = response_dict['main']
    temp_detail['city_name'] = response_dict['name']
    temp_detail['country'] = response_dict['sys']['country']
    temp_detail['cloud'] = response_dict['weather'][0]['description']
    return temp_detail


#Pretty print function to print all the values to the output
def pretty_print(temp_dict,zip_city, zip_city_flag, f_c_flag, user):
    '''
    :param temp_dict: Dictionary having temperatues and city name
    :param zip_city: Zip or city entered by the user
    :param zip_city_flag: Zip or city flag to denote if zip_city is zip or city
    :param f_c_flag: Fahreheit/ Celcius flag to denote the output temperature unit
    :param user: User name
    :return: No return value
    '''

    #Printing all the values to the output screen based on user selection
    #Zip/City, Temperatures, Fahrenheit or Celcius, City name
    print('\n#####################################################')
    print('Thanks {} for using Bellevue weather app'.format(user.upper()))
    if zip_city_flag.lower() == 'zip':
        print("City associated with zip code '{}' is '{}'".format(zip_city, temp_dict['city_name']))
        print("The zip code '{}' is located in the country '{}'".format(zip_city, temp_dict['country']))
        print("The weather for the city '{}' is as follows".format(temp_dict['city_name']))
    else:
        print("The city '{}' is located in the country '{}'".format(zip_city,temp_dict['country']))
        print("The weather for given city '{}' is as follows".format(zip_city))
    if (f_c_flag.upper() == 'F'):
        print('The temperatures are shown in Fahrenheit')
    elif (f_c_flag.upper() == 'C'):
        print('The temperatures are shown in Celsius')
    else:
        print('The temperatures are shown in Kelvin')
    print('#####################################################')
    print('Temperature: {} degrees'.format(temp_dict['temp']))
    print('Feels like Temperature: {} degrees'.format(temp_dict['feels_like']))
    print('Minimum Temperature for the day: {} degrees'.format(temp_dict['temp_min']))
    print('Maximum Temperature for the day: {} degrees'.format(temp_dict['temp_max']))
    print('Pressure: {}hPa'.format(temp_dict['pressure']))
    print('Humidity: {}%'.format(temp_dict['humidity']))
    print('Clouds: {}'.format(temp_dict['cloud'].capitalize()))
    print('#####################################################')

    
#Main function
if __name__ == '__main__':

    #User input to get the name of the user and display welcome message
    user_input = 'Y'
    user = input("Please enter your name: ")
    print('Welcome {} to Bellevue weather app'.format(user))

    #User input to ask user if they want to search based on zip or city;
    #For incorrect value, raise an exception
    while user_input.upper() == 'Y':
        while True:
            try:
                zip_city_flag = input("\nPlease confirm if you want to search the weather based on zip or city (zip/city): ")
                if zip_city_flag.lower() in ['zip','city']:
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Please enter the value as either 'zip' or 'city' for the input")

        #Based on value, the user needs to provide the zip code or city;
        #validatezipcity function is called to validate the zip or city entered by user
        #If the zip/city is not valid, it will prompt the user to enter the value again
        while True:
            if zip_city_flag.lower() == 'zip':
                print("\nYou have selected weather search based on zip code")
                try:
                    zip_city = int(input("Please enter the zip code: "))
                    if validatezipcity(zip_city, zip_city_flag):
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Entered zip code '{}' is not valid".format(zip_city))
            else:
                print("\nYou have selected weather search based on city name")
                print("The search is limited to the country USA")
                try:
                    zip_city = str(input("Please enter the city name in US: "))
                    state_abbv = str(input("Please enter the state abbreviation for the city: "))
                    if validatezipcity(zip_city, zip_city_flag, state_abbv):
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Entered city name '{}' and state abbreviation {} is not valid".format(zip_city,state_abbv))


        #User input asking to enter the out temperature unit (Fahrenheit/Celcius/Kelvin);
        while True:
            try:
                f_c_flag = input("\nPlease enter the unit to display output temperature (F/C/K): ")
                if f_c_flag.upper() in ['F','C','K']:
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Unit '{}' provided is not valid. Please enter valid measure (F/C/K)")

        #Call API based on zip/city provided by user
        response = weatherapi(zip_city, zip_city_flag, f_c_flag)

        #Calling pretty print function to print the output
        pretty_print(response, zip_city,zip_city_flag,f_c_flag, user)

        #Asking user if they want to continue searching for another zip/city;
        #If Y, repeat the above process; else, exit the program
        while True:
            try:
                user_input = input('\nDo you want to continue with weather check for another city (Y/N): ')
                if user_input.upper() in ['Y','N']:
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Please enter the value as Y or N for the input")
                continue
