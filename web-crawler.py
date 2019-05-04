from bs4 import BeautifulSoup
import threading
import requests
import sys
import time

def get_restrictions(url):
	robots_txt = url[:len(url)] + "robots.txt"
	robots_page = requests.get(robots_txt)
	parsed_robots_txt = BeautifulSoup(robots_page.content, 'html.parser')
	string_parsed_robots_txt = parsed_robots_txt.string
	general_user_agent_location = parsed_robots_txt.string.find('User-agent: *')
	string_parsed_robots_txt = string_parsed_robots_txt[general_user_agent_location:]
	restricted = []
	for line in string_parsed_robots_txt.split('\n'):
		if ( line.find('Disallow:') > -1 ):
			path = line[line.find('Disallow:')+len('Disallow:'):]
			if (path.find('#') > -1):
				path = path[:path.find('#')-1]
			path = path.strip()
			restricted.append(path)

	return restricted


def main():
	# should take seed from command line argument, but for now it is hardcoded
	#seed = sys.argv[1]
	#num_pages = sys.argv[2]
	#hops = sys.arv[3]
	seed = "https://www.fda.gov/"
	link = seed[:len(seed)-1]
	list_restrictions = get_restrictions("https://www.fda.gov/")
	list_links = []
	level_dictionary = { seed:1 }
	level = 0
	
	cnt = 0

	list_links.append(seed)
	for i in list_links:
		print("Current Page: ", i)
		if ( level_dictionary[i] > 5 ):
			break
		current_page = requests.get(i)
		if(current_page.status_code != 200 ):
			continue
		html_code = BeautifulSoup(current_page.content, 'html.parser')
		#for tag in html_code.findAll('p'):
		#	print(tag.get_text())
		for tag in html_code.findAll('a', href=True):
			if ( link + tag['href'] not in list_links ):
				if ( len(tag['href']) > 0 and tag['href'] not in list_restrictions and tag['href'][0] == '/'):
					if ( len(tag['href']) > 1 ):
						if ( tag['href'][1] != '['):
							list_links.append(link+tag['href'])
							level_dictionary[link+tag['href']] = level_dictionary[i]+1
						else:
							continue
					else:
						list_links.append(link+tag['href'])
						level_dictionary[link+tag['href']] = level_dictionary[i]+1
		cnt += 1
		time.sleep(30)
		
main()