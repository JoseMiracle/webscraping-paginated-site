import scrapy


class HockeyTeamInfoScraperSpider(scrapy.Spider):
    name = "hockey_team_info_scraper"
    allowed_domains = ["www.scrapethissite.com"]
    start_urls = ["https://www.scrapethissite.com/pages/forms/"]
    base_url = 'https://www.scrapethissite.com'

    def parse(self, response):
        tables = response.css('table.table')
        rows = tables.css('tr')

        for each_row in rows[1:]:
            yield {
                'team_name': ' '.join(each_row.css('td.name::text').get().split()),
                'team_year': ''.join(each_row.css('td.year::text').get().split()),
                'wins': ''.join(each_row.css('td.wins::text').get().split()),
                'losses': ''.join(each_row.css('td.losses::text').get().split()),
                'ot-losses': ''.join(each_row.css('td.ot-losses::text').get().split()),
                'pct.text-success':  ''.join(each_row.css('td.ot-losses::text').get().split()) if each_row.css('td.ot-losses::text').get() is not None else None,
                'gf': ''.join(each_row.css('td.gf::text').get().split()),
                'ga': ''.join(each_row.css('td.ga::text').get().split()),
                'diff.text-success': ''.join(each_row.css('td.diff.text-success::text').get().split()) if each_row.css('td.diff.text-success::text').get() is not None else None

            }

        next_page_links = response.css('a[href*="pages/forms/?"]::attr(href)').getall()
        number_of_links = len(next_page_links)
        for link in next_page_links[2:number_of_links-2]:
            if link :
                next_page_url = self.base_url + link
                yield response.follow(next_page_url, callback=self.parse)
        

                
