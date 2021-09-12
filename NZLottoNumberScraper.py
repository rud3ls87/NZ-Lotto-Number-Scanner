import requests
from bs4 import BeautifulSoup
import pandas as pd

# This functio Displays ASCII art banner at the start of the program
def display_banner():
    print(r'''
 _   _                 _                 _____
| \ | |               | |               /  ___|
|  \| |_   _ _ __ ___ | |__   ___ _ __  \ `--.  ___ _ __ __ _ _ __   ___ _ __
| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  `--. \/ __| '__/ _` | '_ \ / _ \ '__|
| |\  | |_| | | | | | | |_) |  __/ |    /\__/ / (__| | | (_| | |_) |  __/ |
\_| \_/\__,_|_| |_| |_|_.__/ \___|_|    \____/ \___|_|  \__,_| .__/ \___|_|
                                                             | |
                                                             |_|
New Zealand Lotto Number Scraper v1.0
Coded by Rudy Mostert on Python 3.8.5
rudy.oncourse@gmail.com

    ''')


# This function specifies the page we will extracting the data/results from
def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'} #lets the host know that we are not a bot
    url = f'https://home.nzcity.co.nz/lotto/lotto.aspx?draw={page}' # Each page contains a new set of results
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup # This is our raw data

# This function loops through all tables that contain results on the page, finds each balls number as well the date of the draw
def transform(soup):
    number_tables = soup.find_all('table', class_ = 'lottomain') # Finds all result tables
    for item in number_tables:
        ball1_data = soup.find('img', id = 'ctl00_ContentPlaceHolder1_ball1', alt = True) # Results are all images so the alt text is selected
        ball2_data = soup.find('img', id = 'ctl00_ContentPlaceHolder1_ball2', alt = True)
        ball3_data = soup.find('img', id = 'ctl00_ContentPlaceHolder1_ball3', alt = True)
        ball4_data = soup.find('img', id = 'ctl00_ContentPlaceHolder1_ball4', alt = True)
        ball5_data = soup.find('img', id = 'ctl00_ContentPlaceHolder1_ball5', alt = True)
        ball6_data = soup.find('img', id = 'ctl00_ContentPlaceHolder1_ball6', alt = True)
        bonusBall_data = soup.find('img', id = 'ctl00_ContentPlaceHolder1_bonus1', alt = True)
        # A dictionary of the results is created
        lotto_numbers = {
            'ball1' : ball1_data['alt'],
            'ball2' : ball2_data['alt'],
            'ball3' : ball3_data['alt'],
            'ball4' : ball4_data['alt'],
            'ball5' : ball5_data['alt'],
            'ball6' : ball6_data['alt'],
            'bonusBall' : bonusBall_data['alt'].replace('Bonus number ', '')
        }
    draw_date = soup.find(id = 'ctl00_ContentPlaceHolder1_LottoDrawDate') # The draw date is situated outside of the draw results table in the main part of the soup
    lotto_date = {
        'drawDate' : draw_date.string # The draw date is changed to a string and added to a dictionary
    }
    total_results = {
        **lotto_date, **lotto_numbers # The two dictionaries of the resutls and dates of draws are combined
    }
    results.append(total_results) # The new dictionary is appened to the results list
    return

 # This function looks at the latest draw number to determine how many times to run the for loop to get the results data
def totalDraws():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}
    url = f'https://home.nzcity.co.nz/lotto/lotto.aspx' # The main homepage of the NZ lotto results, it has the last draw number
    r = requests.get(url, headers)
    main_page_soup = BeautifulSoup(r.content, 'html.parser')
    latest_draw = main_page_soup.find(id = 'ctl00_ContentPlaceHolder1_LottoDrawNumber').string # The label id on the main page that contains the latest draw number. It is changed to a string as a label is initially returned
    return latest_draw

# This function is the main function that runs the extract and transform functions
def mainloop():
    for i in range((total_num_draws - (history_weeks * 2)), total_num_draws, 1): # This loop loops through the total number of draws/pages. It starts at the specified user input history(*2 becuase 2 entries per week) and goes up to the lastest(newest) draw.
        print(f'Getting draw result number {i} of {total_num_draws -1} total draws.')
        c = extract(i) # Extracts all the data from i page number
        transform(c) # Transforms the data we need
    return

# This function saves the results to a CSV file
def saveToCsv(results):
    df = pd.DataFrame(results) # Creates the dataframe
    df.index = df.index + 1 # Inital index is 0, this changes it to 1 for easier data processing purposes
    print(df.head())
    df.to_csv('results.csv') # The dataframe is saved to a .csv file for data analysis
    return

if __name__ == "__main__":
    display_banner()
    history_weeks = int(input('How many weeks do you want to go back? Min 1 week, Max 260 weeks due to host request limit. There are two draws per week (Saturday and Wednesday), so 1 week will yield 2 records. Input amount of weeks: '))# 2 draws paer week, going back 5 years is 520 entries
    results = [] # A list of the results
    total_num_draws = int(totalDraws()) + 1 # The +1 is added because of python iteration starting at 0. This is done so that it returns results for the latest results.
    totalDraws()
    print()
    mainloop()
    print()
    print('Here is a sample of your dataset:')
    print()
    saveToCsv(results)
    print()
    print('Thanks for trying out the NZ lotto number scraper, the full .csv results are in the same folder as the scraper.')
