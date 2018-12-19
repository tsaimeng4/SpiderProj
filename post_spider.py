import scrapy

# In command window, go to the project's top level directory and run:
# 'scrapy crawl post -o bc_post.json'
# to start the spider and store the scraped data

class CommentSpider(scrapy.Spider):
    name = "post"
    #disc_url='https://www.dailystrength.org/group/diabetes-type-2/discussions/ajax?page={}&limit=15'
    #disc_url='https://www.dailystrength.org/group/diabetes-type-2?page={}#discussion-3670319'
    #disc_url='https://www.dailystrength.org/group/breast-cancer?page={}#discussion-3650431'
    #disc_url = 'https://www.dailystrength.org/group/depression?page={}#discussion-3693153'
    disc_url = 'https://www.dailystrength.org/group/depression?page={}#discussion-3660150'

    start_urls = [
        disc_url.format(102)
        #'https://www.dailystrength.org/group/breast-cancer?page=9#discussion-3650431',
    ]

    def parse(self, response):

        #data=json.loads(response.text)

        # follow links to comment pages
        for href in response.css('h3.newsfeed__title a::attr(href)'):

            if href is not None:
                
               yield response.follow(href, callback=self.pat_comment)


    def pat_comment(self, response):

        #for post in response.css('div.newsfeed__title-block'):
        post=response.css('div.newsfeed__title-block')

        yield {
            'title': response.css('title::text').extract(),
            'author': post.css('span.newsfeed__byline a::text').extract(),
            'a_id': post.css('span.newsfeed__byline a::attr(href)').extract(),
            'time': post.css('time.newsfeed__item-time ::attr(datetime)')[0].extract(),
            'date': post.css('time.newsfeed__item-time::text')[0].extract(),
            'mood': response.css('div.avatar-mood i')[0].extract(),
            'reply_ct': response.css('div.newsfeed__icon-count::text')[0].extract(),
            'comment': post.css("div.posts__content p::text").extract(),
            'comments': post.css("div.posts__content p span::text").extract()
        }

       #for comment in response.css('div.comments__comment'):
        #   yield {
        #        'title': response.css('title::text').extract(),
        #        'reply-to': post.css('span.newsfeed__byline a::text').extract(),
         #       'author':comment.css('span.comments__name a::text').extract_first(),
         #       'time':comment.css('time.newsfeed__itemtime::text').extract_first(),
         #       'comment':comment.css("::text")[7:].extract()
         #   }
