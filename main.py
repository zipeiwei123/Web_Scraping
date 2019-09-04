from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
from time import sleep
from time import *
from random import randint
from requests_html import HTMLSession
from input import *


# global variable
TAG_RE = re.compile(r'<[^>]+>')
COUNT = 0

# Preparing the monitoring of the loop
start_time = time()

#remove </p> tags from paragraph
def remove_tags(text):
    return TAG_RE.sub('', text)


def write_page(file1, soup, count):
	contents = str(soup.find('div', id='nr_content'))
	contents = remove_tags(contents)
	chapter = "章节" + str(count)
	file1.write("\n\n" + chapter.center(100, '*') + "\n\n")
	for content in contents:
		if content == "。":
			file1.write(content+"\n\n")
		else:
			file1.write(content)

#Initial the first soup with creation of the file.txt
def initial_soup(website, title):
	# req = Request(website)
	req = Request(website, headers={'User-Agent': 'Mozilla/5.0'})
	content = urlopen(req).read()
	soup = BeautifulSoup(content, 'html.parser')
	# web scrapting content
	author = soup.find('p', {'class': 'bq'}).a.string
	
	# initial files only run one time
	file1 = open(title + "by"+ author + ".txt", "w")
	return soup, file1

#new soup for links contained in website
def new_soup(website):
	req = Request(website, headers={'User-Agent': 'Mozilla/5.0'})
	content = urlopen(req).read()
	soup = BeautifulSoup(content, 'html.parser')
	# web scrapting content
	titles = soup.title.string
	return soup

#get all inner links inside the website
def get_all_links(soup, home_page, file1):
	links = []
	current_chapters = soup.find('div', {'class': 'ml_list'})
	new_chapters = soup.find('div', {'class': 'newest'})
	string_length=30 
	#author for each chapter
	author = soup.find('p', {'class': 'bq'}).a.string
	s = soup.title.string + "by" + author
	file1.write("\n\n"+s.center(string_length)+"\n\n")
	count = 1

	file1.write("\n\n\n"+"全部章节"+"\n\n\n")
	for a in current_chapters.find_all('a', href = True):
		file1.write("\n\n"+"章节"+str(count)+a.string.center(string_length)+"\n\n")
		if str(home_page + a['href']) not in links:
			count += 1
			links.append(str(home_page + a['href']))

	
	
	return links

#wrapper class for keep reading websites
def write_files(website):
	requests = 0
	next_chapter = 'html'
	soup, file1 = initial_soup(website[0], website[1])
	links = get_all_links(soup, website[0], file1)
	#initial a counter for counting chapter
	count = 1
	for link in links:
		soup = new_soup(link)
		write_page(file1, soup, count)
		#update count
		count += 1
		sleep(randint(30,35))
		requests += 1
		elapsed_time = time() - start_time
		print(link)
		print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
	print('\n\n')
	print("File {}.txt Completed".format(website[1]))
	print('\n\n')
	file1.close() 



	
def main():
	
	websites = load_input()
	for website in reversed(websites):
		print('\n Start Downloading {}.txt\n\n'.format(website[1]))
		write_files(website)
		
	print("All Jobs Done, Goodbye")

	


if __name__ == "__main__":
	main()
