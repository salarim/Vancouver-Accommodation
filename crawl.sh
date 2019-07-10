#!/bin/sh
rm craigslist.csv; scrapy crawl craigslist --nolog -o craigslist.csv -t csv;
rm kijiji.csv; scrapy crawl kijiji --nolog -o kijiji.csv -t csv;