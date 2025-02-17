import scrapy


class NetEmpregosItem(scrapy.Item):

    Name = scrapy.Field()
    Description = scrapy.Field()
    Organization = scrapy.Field()
    Location = scrapy.Field()
    Ref = scrapy.Field()
