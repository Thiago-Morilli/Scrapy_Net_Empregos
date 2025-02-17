import scrapy
import json
import re
from Net_Empregos.items import NetEmpregosItem

class EmpregosSpider(scrapy.Spider):
    name = "Empregos"
    allowed_domains = ["www.net-empregos.com"]
    start_urls = ["https://www.net-empregos.com/pesquisa-empregos.asp?chaves=python&cidade=&categoria=0&zona=0&tipo=0"]

    def parse(self, response):

        get_link = response.xpath('//div[@class="job-item media"]/div/h2/a[@class="oferta-link"]/@href').extract_first()
        link = "https://www.net-empregos.com/" + get_link

        yield scrapy.Request(
            url=link,
            method="GET",
            callback=self.Jobs
        )
                                                                         
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

        yield NetEmpregosItem(
            collecting_data
        )
            