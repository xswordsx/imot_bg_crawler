import logging
import scrapy
import scrapy.logformatter
import os


class LessVerboseLogger(scrapy.logformatter.LogFormatter):
    def dropped(self, item, exception, response, spider):
        return {
            "level": logging.DEBUG,  # lowering the level from logging.WARNING
            "msg": "Dropped: %(exception)s",
            "args": {
                "exception": exception,
            },
        }

    # def crawled(self, request, response, spider):
    #     """Logs a message when the crawler finds a webpage."""

    # def scraped(self, item, spider):
    #     """Logs a message when an item is scraped by a spider."""

    # def download_error(failure: Failure, request: Request, spider: Spider, errmsg: Optional[str] = None):
    #     """Logs a download error message from a spider (typically coming from the engine)."""

    # def item_error(item: Any, exception: BaseException, response: Response, spider: Spider):
    #     """Logs a message when an item causes an error while it is passing through the item pipeline."""

    # def scraped(item: Any, response: Union[Response, Failure], spider: Spider):
    #     """Logs a message when an item is scraped by a spider."""

    # def spider_error(failure: Failure, request: Request, response: Union[Response, Failure], spider: Spider):
    #     """Logs an error message from a spider."""
