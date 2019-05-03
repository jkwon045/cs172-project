from bs4 import BeautifulSoup
import threading
import requests
import sys
import time


def get_restrictions(url):
	robots_txt = url[:len(url)] + "/robots.txt"
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
#	seed = open("test.txt", "r")
#	if seed.mode != "r":
#		exit(-99)
	#seed = "https://www.fda.gov/"
	with open("test.txt", "r") as file:
		list_links = file.read().splitlines()

	seed_list = list_links[:]
	level_dictionary = {}
	#list_restrictions = get_restrictions(links[1])
	level = 0

	cnt = 0

#	for x in seed:
#		print("Current page: " , x)
#		list_links.append(x)
	for current_seed in seed_list:
		level_dictionary.clear()
		level_dictionary = {current_seed: 1}
		list_restrictions = get_restrictions(current_seed)  # get restrictions for every page we scan
		list_links.clear()
		list_links.append(current_seed)

		for i in list_links:
			link = i[:len(i)-1]

			print("Current page: ", repr(i))
			#if ( level_dictionary[i] > 5 ):
				#  break
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
			time.sleep(2) #speed this up for testing
			#time.sleep(30)
		
main()