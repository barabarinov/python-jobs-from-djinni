import random
import time

import scrapy
from scrapy.http import Response


class PythonVacanciesSpider(scrapy.Spider):
    name = "python_vacancies"
    allowed_domains = ["djinni.co"]
    start_urls = ["https://djinni.co/jobs/?primary_keyword=Python"]

    @staticmethod
    def get_vacancy_title(response: Response) -> str | None:
        vacancy_title = response.css("h1::text").get()
        if vacancy_title:
            return vacancy_title.strip()
        return None

    @staticmethod
    def get_company_name(response: Response) -> str | None:
        company_title = response.css(".job-details--title::text").get()
        if company_title:
            return company_title.strip()
        return None

    @staticmethod
    def get_technologies(response: Response) -> str | None:
        span_tag = response.xpath('//span[contains(@class, "bi-tags")]')
        return span_tag.xpath('./parent::div/following-sibling::div[@class="col pl-2"]/text()').get()

    def parse(self, response: Response, **kwargs) -> None:
        job_urls = response.css(".job-list-item__link::attr(href)").getall()

        for job_url in job_urls:
            time.sleep(random.randint(1, 3))
            yield response.follow(job_url, callback=self.parse_job_vacancy)

        next_page = response.css(".page-link:has(span.bi-chevron-right)::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_job_vacancy(self, response: Response) -> dict[str, str | None]:
        yield {
            "vacancy_title": self.get_vacancy_title(response),
            "company_name": self.get_company_name(response),
            "required_technologies": self.get_technologies(response),
        }
