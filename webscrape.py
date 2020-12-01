from __future__ import unicode_literals
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import discord_notify as dn
from time import sleep
import csv
import shutil
import smtplib
import os
import threading

def update():
    num_discs = 20   # Number of products scraped
    my_url = 'https://otbdiscs.com/'    # URL of site to scrap
    notifier = dn.Notifier("https://discordapp.com/api/webhooks/782356542179508254/_VVJxmscOPkztfubKdO3198msha8cjfAEsvntyR76ed7ps3kSucdZlIt20v-TAKy3UsQ")
    message = ""

    # Find directory
    BASE_DIR = os.getcwd()

    while True:
        #notifier.send("Loop!", print_message=False)

        # Grab the html from website
        uClient = urlopen(my_url)
        page_html = uClient.read()
        uClient.close()

        # Open old csv file of discs
        old_discs_csv = open('old_disc_list.csv')
        csv_reader = csv.reader(old_discs_csv, delimiter=',')

        # Open new csv file of discs
        new_discs_csv = open('new_disc_list.csv', "w+")
        csv_writer = csv.writer(new_discs_csv, delimiter=',')

        # Parse html
        page_soup = soup(page_html, "html.parser")

        # Find all products
        discs = page_soup.findAll("li",{"class":"wc-block-grid__product"})

        # Make list
        old_discs = []

        for row in csv_reader:
            old_discs.append(row[0])

        count = 0
        didItChange = False
        for old_disc in old_discs:
            # Grab the name
            name_div = discs[count].findAll("div",{"class":"wc-block-grid__product-title"})
            disc_name = name_div[0].text

            csv_writer.writerow([disc_name])

            if(old_disc != disc_name):
                didItChange = True
                if not(disc_name in old_discs):
                    message+="NEW ITEM! " + disc_name + "\n"
                    print("NEW DISC!")
                    print(disc_name)

            # Increment the row count
            count+=1

        if(didItChange):
            notifier.send(message, print_message=False)
        shutil.move(BASE_DIR + "/new_disc_list.csv", BASE_DIR + "/old_disc_list.csv")

        base_sleep = 1
        sleep(base_sleep)

update()
