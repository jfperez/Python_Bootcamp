#!/usr/bin/env python27
# TennisBot.py
# Python Script to automatically sign onto www.holdmycourt.com and make a reservation


import os
import mechanize
import smtplib
import pyttsx
import datetime
import time


class User(object):
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class Reservation(object):
    def __init__(self, date, time, court, email, password):
        self.date = date
        self.time = time
        self.court = court
        self.email = email
        self.password = password

    def get_res(self):
        return self.date, self. time, self.court, self.password


def get_user():
    # Get username
    while True:
        name = raw_input("Enter Firstname: ")
        # name = str(name)
        if len(name) == 0:
            exit()
        if not name.isalpha():
            print('Alpha characters only')
        else:
            break
    # Check to see if data already on file
    if os.path.isfile(name + '.txt'):
        fh = open(name + '.txt', 'r')
        data = fh.read()
        data = data.split('|')
        fh.close()
        user = User(data[0], data[1], data[2])
        return user
    else:
        # If UserName not on file then gather info for logon
        str = ''+name
        while True:
            email = raw_input("Enter Website Email: (XXXXXX@XXXX.com) ")
            if len(email) == 0 or email.find('@') == -1:
                talk('Enter email in correct format')
                continue
            else:
                str = str + '|' + email
                break
        while True:
            password = raw_input('Enter Website Password: ')
            if len(password) == 0:
                talk('Enter password')
                continue
            else:
                str = str + '|' + password
                break
    # Create user file and class instance
    user = User(name, email, password)
    fh = open(name + '.txt', 'w')
    fh.write(str)
    fh.close()
    return user


def get_res(user):
    # Get reservation data from user
    while True:
        res_date = raw_input('Enter (1) for Today or (2) for tomorrow: ')
        if res_date != '1' and res_date != '2':
            talk("Enter 1 for Today or 2 for tomorrow")
            continue
        if res_date == '2':
            if int(time.strftime('%H')) < 15:
                talk('Cant do it until after 3 pm')
                exit()
        break
    # Massage reservation date into useful format for link search
    if res_date == '2':
        res_date = datetime.date.today() + datetime.timedelta(days=1)
    else:
        res_date = datetime.date.today()
    res_date = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][res_date.weekday()] \
               + ' ' + res_date.strftime('%B')[0:3] + ' ' + res_date.strftime('%d')
    # Get the rest of the reservation data
    print "Scheduled Time Slots\n7:00am\n8:30am\n10:00am\n11:30am\n1:00p\n2:30pm\n4:00pm\n5:30pm\n7:00pm"
    while True:
        res_time = raw_input('Enter time from list displayed: ')
        if not res_time in '7:00am,8:30am,10:00am,11:30am,1:00p,2:30pm,4:00pm,5:30pm,7:00pm':
            talk('Enter time from list please')
            continue
        else:
            break
    while True:
        res_court = raw_input('Enter (1) for Ballmachine Court or (2) for Backboard Court: ')
        if res_court != '1' and res_court != '2':
            talk('Enter 1 for Ballmachine Court or 2 for Backboard Court')
            continue
        else:
            break
    res_email = raw_input('Enter notifications email: ')
    if not len(res_email):
        res_email = user.email
    res_password = raw_input('Enter password for email notification or just Enter to use previous: ')
    if not len(res_password):
        res_password = user.password
    res_data = Reservation(res_date, res_time, res_court, res_email, res_password)
    return res_data


def make_res(user, res):
    # Open the website
    browser = mechanize.Browser()
    browser.open('https://holdmycourt.com/reserve2/diamondarec')
    # Sign On
    response = browser.follow_link(text='Sign In or Register', nr=0)
    browser.select_form(nr=0)
    browser.form['email'] = user.email
    browser.form['password'] = user.password
    browser.submit()
    # Now you are on the reservations page
    # Pick the date
    success = False
    for link in browser.links():
        if link.text == res.date:
            response = browser.follow_link(link)
            success = True
            break
    if not success:
        send_mail('Could not find the date selected', res.email, res.password)
        exit()
    # Pick the court
    if res.court == 'Ball Machine':
        num = '1'
    else:
        num = '2'
    # Find the right time to click and make a reservation
    success = False
    for link in browser.links():
        if link.text == res.time and link.url.find("count=" + num):
            response = browser.follow_link(link)
            success = True
            break
    if not success:  # Time already booked
        send_mail('Houston we have a problem - could not book the time', res.email, res.password)
        exit()
    # Now we click again to submit reservation
    browser.select_form(nr=0)
    browser.submit()
    # Sign off
    browser.back()
    response = browser.follow_link(text='Sign Out', nr=0)
    send_mail('TennisBot Reservation Made', res.email, res.password)


def talk(text):
    # Talk to the user
    engine = pyttsx.init()
    engine.setProperty('rate', 100)
    engine.setProperty('volume', 100)
    engine.say(text)
    engine.runAndWait()


def send_mail(text, email, password):
    # Send email to user
    sender, receiver = email, email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, text)
        print 'email sent'
    except smtplib.SMTPException:
        print 'Error: unable to send email'

# Execute the logic
talk('welcome to the tennis bot program')
talk('please enter your first name')
user = get_user()
res = get_res(user)
make_res(user, res)
exit()