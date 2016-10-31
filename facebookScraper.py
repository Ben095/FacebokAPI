import requests, dryscrape
from bs4 import BeautifulSoup
from time import sleep
import json
from datetime import datetime, timedelta



def TryDate():
	from datetime import datetime, timedelta

	N = 1

	date_N_days_ago = datetime.now() - timedelta(weeks=N)
	day =  str(date_N_days_ago).split(' ')[0].split('-')[-1]
	print str(date_N_days_ago.strftime("%B")) + ' ' + day 
#TryDate()

def FacebookScraper():
	N = 1

	date_N_days_ago = datetime.now() - timedelta(weeks=N)
	day =  str(date_N_days_ago).split(' ')[0].split('-')[-1]
	FilterDate =  str(date_N_days_ago.strftime("%B")) + ' ' + day 

	username = 'raisethehell_biplov@yahoo.com'
	password = '5102217320vb'
	sess = dryscrape.Session(base_url='https://www.facebook.com')
	sess.visit('/')
	emailField = sess.at_xpath('//*[@name="email"]')
	emailField.set(username)
	passwordField = sess.at_xpath('//*[@name="pass"]')
	passwordField.set(password)
	sess.render('setpass.png')
	LoginButton = sess.at_xpath('//*[@type="submit"]')
	LoginButton.click()
	sleep(2)
	print "Logged In!"
	sess.visit('https://www.facebook.com/search/latest/?q=%23Fitness')
	sleep(7)
	print "processing data...."
	#html = sess.body()
	sess.render('whatpage.png')
	sess.exec_script("window.scrollTo(0, document.body.scrollHeight);")
	sleep(10)
	sess.render('scrolled.png')
	html = sess.body()
	soup = BeautifulSoup(html)
	getUserPosts = soup.findAll('div',attrs={'class':"userContentWrapper _5pcr"})
	arr = []
	for timeDate in getUserPosts:
		#sess.exec_script("scroll(0, 250);")
		dictionary = {}
		try:
			dictionary['post'] = timeDate.find('div',attrs={'class':'_5pbx userContent'}).text
		except AttributeError:
			dictionary['post'] = "None"
		try:
			dictionary['time'] = timeDate.find('span',attrs={'class':'timestampContent'}).text
		except AttributeError:
			dictionary['time'] = "None"
		try:
			dictionary['share'] = timeDate.find('div',attrs={'class':'_36_q'}).text
		except AttributeError:
			dictionary['share'] = "None"
		try:
			dictionary['likes'] = timeDate.find('span',attrs={'class':'_4arz'}).text
		except AttributeError:
			dictionary['likes'] = "None"
		try:
			dictionary['userURL'] = timeDate.find('span',attrs={'class':'fwb'}).find('a')['href']
		except AttributeError:
			dictionary['userURL'] = "None"
		try:
			dictionary['imgURL'] = timeDate.find('div',attrs={'class':'_3-_h'}).find('img')['style'].replace('background-image: url(','').replace(');','')
		except AttributeError:
			dictionary['imgURL'] = "None"
		arr.append(dictionary)

	with open('data.json','wb') as outfile:
		json.dump(arr,outfile,indent=4)
	print arr
	print len(arr)
FacebookScraper()
