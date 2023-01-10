from selenium import webdriver
import csv
import datetime
import time
import pandas as pd


#newshit

def synergy_login(credentials):
    """
    Function takes in a credentials text file, first row account name, second row password. It navigates a selenium session to synergy sports and uses the given credentials to login
    """
    with open(credentials, 'r') as file:
        cred = file.readlines()

    driver.get('https://www.synergysportstech.com/Synergy/Sport/Basketball/web/teamsst/Video/QuantifiedPlayer2.aspx')
    driver.execute_script("document.body.style.zoom='100%'")

    a = driver.find_element_by_id('txtUserName')
    a.send_keys(cred[0])
    print("Email Id entered...")
    b = driver.find_element_by_id('txtPassword')
    b.send_keys(cred[1])
    print("Password entered...")
    c = driver.find_element_by_id('btnLogin')
    c.click()

#newshit

def scrape_url(url, rows=40):
    """
    This function takes the URL of and appends the player stats to the pre-defined list
    """
    driver.get(url)
    for table_id in range(11,23):
        for r in range(3, int(rows)+1):
        # print(url, r)
            try:
                playtype_path = '/html/body/div[2]/table['+str(table_id)+']/tbody/tr[1]/td[1]'
                playtype = driver.find_element_by_xpath(playtype_path).text

                player_path = '/html/body/div[2]/table['+str(table_id)+']/tbody/tr['+str(r)+']/td[1]'
                player = driver.find_element_by_xpath(player_path).text

                percentoftime_path = '/html/body/div[2]/table['+str(table_id)+']/tbody/tr['+str(r)+']/td[2]'
                percentoftime = driver.find_element_by_xpath(percentoftime_path).text

                possessions_path = '/html/body/div[2]/table['+str(table_id)+']/tbody/tr['+str(r)+']/td[3]'
                possessions = driver.find_element_by_xpath(possessions_path).text

                points_path = '/html/body/div[2]/table['+str(table_id)+']/tbody/tr['+str(r)+']/td[4]'
                points = driver.find_element_by_xpath(points_path).text

                ppp_path = '/html/body/div[2]/table['+str(table_id)+']/tbody/tr['+str(r)+']/td[5]'
                ppp = driver.find_element_by_xpath(ppp_path).text

                fgm_path = '/html/body/div[2]/table['+str(table_id)+']/tbody/tr['+str(r)+']/td[9]'
                fgm = driver.find_element_by_xpath(fgm_path).text

                fga_path = '/html/body/div[2]/table['+str(table_id)+']/tbody/tr['+str(r)+']/td[10]'
                fga = driver.find_element_by_xpath(fga_path).text

                afg_path = '/html/body/div[2]/table['+str(table_id)+']/tbody/tr['+str(r)+']/td[12]'
                afg = driver.find_element_by_xpath(afg_path).text

                tov_path = '/html/body/div[2]/table['+str(table_id)+']/tbody/tr['+str(r)+']/td[13]'
                tov = driver.find_element_by_xpath(tov_path).text

                ft_path = '/html/body/div[2]/table['+str(table_id)+']/tbody/tr['+str(r)+']/td[14]'
                ft = driver.find_element_by_xpath(ft_path).text

                sf_path = '/html/body/div[2]/table['+str(table_id)+']/tbody/tr['+str(r)+']/td[15]'
                sf = driver.find_element_by_xpath(sf_path).text

                row_text = [playtype, player, percentoftime, possessions, points, ppp, fgm, fga, afg, tov, ft, sf, url]
                results.append(row_text)

                with open('synergyoverallresults_play_gleague ' + str(start_time.strftime('%Y-%m-%d %H-%M')) + '.csv', 'a', newline='') as fd:
                    writer = csv.writer(fd)
                    writer.writerow(row_text)

            except:
                pass


if __name__ == '__main__':
    # Locate the chrome webdriver

    driver = webdriver.Chrome(executable_path=r'C:\Users\hasan\Documents\python\chromedriver.exe')
    results = []

    # Login to synergy via the synergy_login function
    synergy_login(r'C:\Users\hasan\Documents\python\synergycred.txt')

    # Read in a set of URLS, which will be used later pass through the scrape(url) function
    urls = []
    with open(r'C:\Users\hasan\Documents\python\gleagueplaylinks.csv', 'r') as f:
        for line in f:
            urls.append(line)

    with open('synergyoverallresults_play_gleague ' + str(time.strftime('%Y-%m-%d %H-%M')) + '.csv', 'a', newline='') as fd:
        writer = csv.writer(fd)
        writer.writerow(['playtype', 'player', 'percentoftime', 'possessions', 'points', 'ppp', 'fgm', 'fga','afg', 'tov', 'ft', 'sf', 'url'])

    start_time = datetime.datetime.now()

    # Feed the FB urls to the scrape_url() function
    for i, u in enumerate(urls):
        scrape_url(u, 40)
        print('**** Analyzed {}% or {} out of {}, runtime so far: {} minutes, expected time left: {} minutes ****'.format(round( (i+1) / len(urls) * 100, 1),
                                                                                                                          i+1,
                                                                                                                          len(urls),
                                                                                                                          round((datetime.datetime.now() - start_time).seconds / 60 , 1),
                                                                                                                          round(round((datetime.datetime.now() - start_time).seconds / (i+1) * len(urls)/60,1) - round((datetime.datetime.now() - start_time).seconds / 60 , 1),1)
                                                                                                                          )
              )

    # Print the results list
    print("*** Entire list of {} urls scraped, total process took {} minutes".format(len(urls), round((datetime.datetime.now() - start_time).seconds / (i+1) * len(urls)/60,1)))
    driver.close()
