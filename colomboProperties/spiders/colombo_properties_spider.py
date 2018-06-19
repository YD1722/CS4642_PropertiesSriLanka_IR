import scrapy


class ResidenceSpider(scrapy.Spider):
    name = "colombo_properties"
    start_urls = [
        'https://www.booking.com/searchresults.en-gb.html?aid=357026&label=gog235jc-country-en-lk-lk-unspec-lk-com-L%3Aen-O%3AwindowsS10-B%3Achrome-N%3AXX-S%3Abo-U%3Ac-H%3As&sid=f8914ecb3ef566d21549063f729f68e7&city=-2214877&track_hp_back_button=1#hotel_1115841-back',

    ]
    seen = set()

    def parse(self, response):
        for hotel in response.css("div.sr_item"):
            main_page_url = hotel.css(
                    'a.hotel_name_link::attr(href)').extract_first().replace('\n', '')
            if(main_page_url in self.seen):
                self.log('already seen------------------------------------  %s' % hotel)
            else:
                self.seen.add(main_page_url)
                main_page_url = hotel.css(
                    'a.hotel_name_link::attr(href)').extract_first().replace('\n', '')
                yield scrapy.Request(response.urljoin(main_page_url), callback=self.parseMain)
        next_page = response.css('a.paging-next::attr(href)').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def parseMain(self, response):
        yield{
            'name': response.css('h2.hp__hotel-name::text').extract_first().replace('\n', ''),
            'stars': response.css('i.star_track::attr(title)').extract_first(),
            'address': response.css('span.hp_address_subtitle::text').extract_first().replace('\n', ''),
            'review_score': response.css('span.review-score-badge::text').extract_first().replace('\n', ''),
            'des': response.css('div.hp_desc_main_content p::text').extract_first().replace('\n', ''),
            # 'important_fascilities':response.css('div.important_facility::text').extract()

        }
