import datetime
import json

from scrapy.exceptions import DropItem

from .sendmail import send_email, format_body, format_subject
from .settings import (
    SKIP_EXISTING,
    SEND_EMAIL,
    EMAIL_RECIPIENTS,
)

CRAWLED_IDS_FILE = "crawled_ids.json"

class ImotBgCrawlerPipeline:
    results_file = None
    start_time = None
    results = []
    existing_items = []

    def open_spider(self, spider):
        self.results_file = open("crawl_stats.json", "w", encoding="utf-8")
        self.start_time = datetime.datetime.now()
        try:
            with open(CRAWLED_IDS_FILE, "r") as file:
                self.existing_items = json.load(file)
                spider.logger.debug(f"Loaded {len(self.existing_items)} items")
        except FileNotFoundError:
            pass  # Probably first pass of the crawler
        except json.JSONDecodeError:
            spider.logger.warn(
                f"The file {self.file_path} does not contain valid JSON."
            )
        except Exception as e:
            raise e

    def process_item(self, item, __spider__):
        item_id = list(item)[0]

        if SKIP_EXISTING and item_id in self.existing_items:
            raise DropItem(f"Item id: {item_id} already scrapped, skipping...")

        self.results.append(item)
        self.existing_items.append(item_id)

        return item

    def close_spider(self, spider):
        end_time = datetime.datetime.now()
        crawled_data = {
            "total_found": len(self.results),
            "stated": self.start_time.isoformat(),
            "ended": end_time.isoformat(),
            "tookSeconds": (end_time - self.start_time).seconds,
        }

        if SEND_EMAIL:
            for item in self.results:
                spider.logger.info(
                    f"Sending email to {len(EMAIL_RECIPIENTS)} recipients"
                )
                data = item[list(item)[0]]
                send_email(subject=format_subject(data), body=format_body(data))

        self.results.append(crawled_data)
        self.results_file.write(
            json.dumps(self.results, ensure_ascii=False).encode("utf8").decode()
        )
        self.results_file.close()
        with open(CRAWLED_IDS_FILE, "w") as file:
            json.dump(self.existing_items, file)
            spider.logger.debug("Updated existing list")
