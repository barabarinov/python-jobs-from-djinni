import time

import scrapy
from scrapy.http import Response


class PythonVacanciesSpider(scrapy.Spider):
    name = "python_vacancies"
    allowed_domains = ["djinni.co"]
    start_urls = ["https://djinni.co/jobs/?primary_keyword=Python"]

    @staticmethod
    def get_vacancy_title(response: Response) -> str:
        return response.css("h1::text").get().strip()

    @staticmethod
    def get_company_name(response: Response) -> str:
        company_title = response.css(".job-details--title::text").get()
        if company_title:
            return company_title.strip()
        return company_title

    @staticmethod
    def get_technologies(response: Response) -> str:
        span_tag = response.xpath('//span[contains(@class, "bi-tags")]')
        return span_tag.xpath('./parent::div/following-sibling::div[@class="col pl-2"]/text()').get()

    def parse(self, response: Response, **kwargs) -> None:
        job_urls = response.css('.job-list-item__link::attr(href)').getall()
        for job_url in job_urls:
            time.sleep(3)
            yield response.follow(job_url, callback=self.parse_job_vacancy)

        next_page = response.css('.page-link:has(span.bi-chevron-right)::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_job_vacancy(self, response: Response) -> dict[str, str]:
        yield {
            "vacancy_title": self.get_vacancy_title(response),
            "company name": self.get_company_name(response),
            "required technologies": self.get_technologies(response),
        }
