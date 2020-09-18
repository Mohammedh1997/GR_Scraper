import scrapy
from scrapy.http import FormRequest
from ..items import GrBooksItem
import re


class BooksSpider(scrapy.Spider):
    name = 'books'
    page_num = 2
    start_urls = ['https://www.goodreads.com/user/sign_in']

    def parse(self, response):
        token = response.xpath("//form//input[@name='authenticity_token']/@value").get()
        n = response.xpath("//form//input[@name='n']/@value").get()
        return FormRequest.from_response(response, formdata={
            'utf8': '✓',
            'authenticity_token': token,
            'user[email]': 'INPUT YOUR OWN',
            'user[password]': 'INPUT YOUR OWN',
            'next': 'Sign in',
            'n': n
        }, callback=self.after_login)

    def after_login(self, response):
        # You may choose whatever url you're interested in
        book_list_url = 'https://www.goodreads.com/shelf/show/consulting?page=1'
        yield scrapy.Request(url=book_list_url, callback=self.start_scraping)

    def start_scraping(self, response):
        items = GrBooksItem()
        books = response.xpath("//div[@class='left']")

        for book in books:
            title = book.xpath(".//a[@class='bookTitle']/text()").get()
            link = book.xpath(".//a[@class='bookTitle']/@href").get()
            author = book.xpath(".//span[2]/div/a[@class='authorName']/span/text()").get()
            shelf_count = book.xpath(".//a[@class = 'smallText']/text()[1]").get()
            shelf_count = int(re.search(r'\d+', shelf_count).group())
            rating_line = book.xpath(".//span[@class='greyText smallText']/text()").get()
            rating_line = (" ".join(rating_line.split())).split(" — ")
            if ',' in rating_line[1]:
                rating_line[1] = rating_line[1].replace(",", "")
            rate_score = float(re.search("\d+\.\d+", rating_line[0]).group())
            rate_quant = int(re.search('\d+', rating_line[1]).group())

            items['title'] = title
            items['link'] = link
            items['author'] = author
            items['shelf_count'] = shelf_count
            items['rate_score'] = rate_score
            items['rate_quant'] = rate_quant

            yield items

        next_page = response.xpath("//a[@class='next_page']/@href").get()

        if next_page:
            yield response.follow(next_page, callback=self.start_scraping)
