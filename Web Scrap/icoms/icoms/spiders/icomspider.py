import scrapy
import pandas as pd

base_url = 'https://icomarks.com/ico/{}'

def read_excel():
    df = pd.read_excel('data_sheet.xlsx')
    return df['Tags'].values.tolist()

class IcomspiderSpider(scrapy.Spider):
    name = "icomspider"
    
    def start_requests(self):
        for tag in read_excel():
            yield scrapy.Request(base_url.format(tag))

    def parse(self, response):
        teams = response.css("div.company-team__item")
        tracker = 0
        for team in teams:
            data = team.xpath("//h1/text()").getall()
            data2 = team.css("div.company-team__post::text").getall()
            advisor = data[1]
            number = len(teams) - int(advisor[10])
            if tracker >= number:
                role = "advsisor"
            else:
                role = "normal"

            url = team.css("div.company-team__links a").attrib['href']
            if "twitter" in url:
                link = "twitter"
            elif "linkedin" in url:
                link = "linkedin"
            else:
                link = "website"

            if len(data2) > 1:
                desc = data2[1]
            else:
                desc = "No description"

            yield{
                'ico_name' : data[0],
                'member_order' : tracker + 1,
                'member_name' : team.css("div.company-team__title::text").get(),
                'position' : data2[0],
                'description' : desc,
                'linktype' : link,
                'link' : url,
                'member_type' : role
            }
            tracker += 1
        pass
