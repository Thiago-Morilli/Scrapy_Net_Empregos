import scrapy


class NetEmpregosItem(scrapy.Item):

    Name = scrapy.field()
    Description = scrapy.field()
    Organization = scrapy.field()
    Location = scrapy.field()
    Ref = scrapy.field()
    