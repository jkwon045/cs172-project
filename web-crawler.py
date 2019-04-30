from bs4 import BeautifulSoup
import requests
import sys

def main():
	# should take seed from command line argument, but for now it is hardcoded
	#seed = sys.argv[1]
	seed = "https://www.fda.gov/drugs/information-drug-class/opioid-medications"
	listLinks = []

	listLinks.append(seed)

	for i in listLinks:
		current_page = requests.get(seed)
		html_code = BeautifulSoup(current_page.content, 'html.parser')
		for tag in html_code.findAll('p'):
			print(tag.get_text())
main()