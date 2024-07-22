import scrapy
import pandas as pd

def read_excel():       
    df = pd.read_excel('linkedin_first.xlsx')
    return df['link'].values.tolist()

class IcomspiderSpider(scrapy.Spider):
    name = "icomspider"

    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.jsonl': { 'format': 'jsonlines',}}
        }
    
    def start_requests(self):
        
        for profile in read_excel():
            linkedin_people_url = profile
            yield scrapy.Request(url=linkedin_people_url, callback=self.parse_profile, meta={'profile': profile, 'linkedin_url': linkedin_people_url})

    def parse_profile(self, response):
        item = {}

        """
            SUMMARY SECTION
        """
        summary_box = response.css("section.top-card-layout")
        item['name'] = summary_box.css("h1::text").get().strip()
        data = summary_box.css("div.not-first-middot span::text").getall()
        if len(data) >= 4:
            item['location'] = data[0].strip()
            item['followers'] = data[2].strip()
            item['connections'] = data[3].strip()
        else:
            item['followers'] = data[1].strip()
            item['connections'] = data[2].strip()
        edu = response.css("span.top-card-link__description::text").getall()
        if len(edu) >= 3:
            item['education'] = edu[2].strip()
            item['job'] = edu[0].strip()

        """
            ABOUT SECTION
        """
        item['about2'] = response.css('section.summary div.core-section-container__content p::text').get()
        data = response.css('section.summary div.core-section-container__content ::text').getall()
        if len(data) >= 1:
            item['about'] = data[1].strip() + data[2].strip()
        """
            EXPERIENCE SECTION
        """
        item['experience'] = []
        experience_blocks = response.css('li.experience-item')
        experience_data = response.css("span.experience-item__subtitle::text").getall()  
        experience = {}
        tracker = 0

        for block in experience_blocks:
            ## time range
            if tracker < 3:
                experience['experience'] = experience_data[tracker].strip()
                try:
                    date_ranges = block.css('span.date-range time::text').getall()
                    if len(date_ranges) == 2:
                        experience['start_time'] = date_ranges[0]
                        experience['end_time'] = date_ranges[1]
                        experience['duration'] = block.css('span.date-range__duration::text').get()
                    elif len(date_ranges) == 1:
                        experience['start_time'] = date_ranges[0]
                        experience['end_time'] = 'present'
                        experience['duration'] = block.css('span.date-range__duration::text').get()
                except Exception as e:
                    print('experience --> time ranges', e)
                    experience['start_time'] = ''
                    experience['end_time'] = ''
                    experience['duration'] = ''
                item['experience'].append(experience)
            
            tracker += 1
        """
            EDUCATION SECTION
        """
        item['education2'] = []
        education_blocks = response.css('li.education__list-item')
        for block in education_blocks:
            education = {}

            ## course details
            try:
                education['course_details'] = ''
                for text in block.css('h4 span::text').getall():
                    education['course_details'] = education['course_details'] + text.strip() + ' '
                education['course_details'] = education['course_details'].strip()
            except Exception as e:
                print("education --> course_details", e)
                education['course_details'] = ''
         
            ## time range
            try:
                date_ranges = block.css('span.date-range time::text').getall()
                if len(date_ranges) == 2:
                    education['start_time'] = date_ranges[0]
                    education['end_time'] = date_ranges[1]
                elif len(date_ranges) == 1:
                    education['start_time'] = date_ranges[0]
                    education['end_time'] = 'present'
            except Exception as e:
                print("education --> time_ranges", e)
                education['start_time'] = ''
                education['end_time'] = ''

            item['education2'].append(education)

        yield item