#!/bin/sh

cd \cs172-project\cs172_web_scraper\cs172_web_scraper\spiders
scrapy crawl govspider -a seed_file="$*" -a num_hops="$*"
