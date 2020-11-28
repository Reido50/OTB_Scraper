from __future__ import unicode_literals
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import csv
import shutil
import smtplib
import os
import threading

def update():
    # Timer for every 10 seconds
    #threading.Timer(10.0, update).start()

    num_discs = 24   # Number of products scraped
    my_url = 'https://otbdiscs.com/'
    sender_email = "reidsender@gmail.com"
    rec_email = "reidoharry50@gmail.com"
    password = "8zM7sBGi9jvK"
    message = """\
    Subject: New Discs!

    Here's the current list:"""

    # Find directory
    BASE_DIR = os.getcwd()

    # Link with gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)

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
    didItChange = False;
    for old_disc in old_discs:
        # Grab the name
        name_div = discs[count].findAll("div",{"class":"wc-block-grid__product-title"})
        disc_name = name_div[0].text

        csv_writer.writerow([disc_name])

        if(old_disc != disc_name):
            didItChange = True
            if not(disc_name in old_discs):
                print("NEW DISC!")
                print(disc_name)
                message += "\n\t" + disc_name

        # Increment the row count
        count+=1

    if(didItChange):
        server.sendmail(sender_email, rec_email, message.encode("utf-8"))
        print("Sent")

    shutil.move(BASE_DIR + "/new_disc_list.csv", BASE_DIR + "/old_disc_list.csv")

update()
