import scrapy
import json
import re
from Net_Empregos.items import NetEmpregosItem

class EmpregosSpider(scrapy.Spider):
    name = "Empregos"
    domain = "https://www.net-empregos.com/pesquisa-empregos.asp?chaves=python&cidade=&categoria=0&zona=0&tipo=0"


    def start_requests(self):
        
        yield scrapy.Request(
            url=self.domain,
            method="GET",
            callback=self.parse
        )
    
    def page(self, response):
        
        get_url_page = response.xpath('//div[@class="pagination-box pb text-center"]/nav/ul/li[5]/a[@class="page-link oferta-link d-none d-lg-block"]/@href').get()
        if get_url_page != None:
            url = "https://www.net-empregos.com/" + get_url_page
            yield scrapy.Request(
                url=url,
                method="GET",                                        
                callback=self.parse
            )
        elif get_url_page == None:
            get_url_page = response.xpath('//div[@class="pagination-box pb text-center"]/nav/ul/li[6]/a[@class="page-link oferta-link d-none d-lg-block"]/@href').get()
            if get_url_page:
                url = "https://www.net-empregos.com/" + get_url_page
                yield scrapy.Request(
                    url=url,
                    method="GET",                                        
                    callback=self.parse
                )


    def parse(self, response):

        for get_link in response.xpath('//div[@class="job-item media"]/div/h2/a[@class="oferta-link"]/@href').getall():
            link = "https://www.net-empregos.com/" + get_link

            yield scrapy.Request(
                url=link,
                method="GET",
                callback=self.Jobs
            )

            yield from self.page(response) 

                                                              
    def Jobs(self, response):

        
        path_json = response.xpath('//script[@type="application/ld+json"]/text()').extract_first()
        path_json = path_json.replace("<BR>", "\\n").replace("<br>", "\\n")
        path_json = re.sub(r'\s+', ' ', path_json) 
        path = path_json.strip()
        json_info = json.loads(path)

        Ref = response.xpath('//div[@class="candidate-listing-footer"]/ul/li[3]/text()').extract_first()
        collecting_data  = {
            "Name": json_info["title"],
            "Description": json_info["description"].replace("\n \n", "").replace("\n", ""),
            "Organization": json_info["hiringOrganization"]["name"],
            "Location": json_info["jobLocation"]["address"]["addressLocality"],
            "Ref": Ref

        }   

        print(collecting_data)
        yield NetEmpregosItem(
                collecting_data
            )


