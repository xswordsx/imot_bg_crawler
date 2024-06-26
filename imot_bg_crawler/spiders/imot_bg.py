import re
from urllib.parse import parse_qs, urlparse

from scrapy.utils.project import get_project_settings

from imot_bg_crawler.utils.tools import get_html_tag_text
from imot_bg_crawler.spiders.base_spiders import BaseSpider


class ImotBgSpider(BaseSpider):
    name = "imot.bg"
    allowed_domains = ["imot.bg"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = get_project_settings()
        self.start_urls = settings["INPUT_DATA"][self.allowed_domains[0]]

    def parse(self, response, **kwargs):
        items = response.css(".lnk2")
        yield from response.follow_all(items, self.parse_item)
        pages = response.css("a.pageNumbers")
        yield from response.follow_all(pages, self.parse_page)

    def parse_page(self, response):
        items = response.css(".lnk2")
        yield from response.follow_all(items, self.parse_item)

    def parse_item(self, response):
        url = response.url
        ad_id = parse_qs(urlparse(url).query).get("adv")[0]
        metadata_raw = response.css("div.adParams > *").getall()
        metadata = {}
        for item in metadata_raw:
            line = get_html_tag_text(item)
            k, v = line.split(": ")
            metadata[k] = v

        price = response.css("#cena").get()
        price = get_html_tag_text(price).strip()
        descr_base = response.css("#description_div").get()
        descr_base = get_html_tag_text(descr_base).strip()
        descr_extra = response.css("#dots_less").get()
        descr_extra = get_html_tag_text(descr_extra).strip()
        address = response.css(".location").get()
        address = get_html_tag_text(address)
        descr = descr_base + descr_extra
        descr.replace("Виж повече", "")
        descr.replace("Виж по-малко", "")
        images = response.css("a::attr(data-link)").getall()
        images = [
            f"https:{item}" for item in images if re.search(r"/big/", item) is not None
        ]

        self.fill_in_scraped_data(
            ad_id=ad_id,
            url=url,
            descr=descr,
            address=address,
            price=price,
            images=images,
            source=self.allowed_domains[0],
            metadata=metadata,
        )

        result = self.generate_result()
        return result
