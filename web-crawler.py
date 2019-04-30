from bs4 import BeautifulSoup
import threading
import requests
import sys

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
	seed = "https://www.fda.gov/drugs/information-drug-class/opioid-medications"
	list_restrictions = get_restrictions("https://www.fda.gov")
	list_links = []

	list_links.append(seed)
	cnt = 0
	for i in list_links:
		print(i)
		#print(i)
		if ( cnt == 1000 ):
			break;
		current_page = requests.get(i)
		html_code = BeautifulSoup(current_page.content, 'html.parser')
		#for tag in html_code.findAll('p'):
		#	print(tag.get_text())
		for tag in html_code.findAll('a', href=True):
			if ( tag['href'] not in list_restrictions and tag['href'][0] == '/'):
				list_links.append(i+tag['href'])
		cnt+=1
main()