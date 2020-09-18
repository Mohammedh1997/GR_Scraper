# GR_Scraper
This is a Scrapy project to scrape books from the consulting shelf of goodreads.

### Extracting other shelves
* Change the book_list_url link to your desired shelf link

### Extracted data
This project extracts five data sets including: 

* Title
* Link
* Author
* Number of time the book has been shelved to it's respective genre
* Rating score out of 5
* Quantity of ratings

### Spiders
* This project contains one spider "books"

### Spider running command
* $ scrapy crawl books

### Scraped data to csv command
* $ scrapy crawl books -o quotes.json
