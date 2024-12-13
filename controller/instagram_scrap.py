from datetime import datetime
import traceback
from model.Post import PostModel
from model.Error.ErrorModel import ErrorModel, ErrorCode
from service.llm_scrap.gemini_scrapper import GeminiScraperService
from service.logger_service import LoggerService
from service.bigquery_service import BigQueryService
from constants.prompt.instagram import InstagramTarget, INSTAGRAM_PROMPT
import json
import re
import typing


class Post(typing.TypedDict):
    shortcode: typing.Optional[str]
    post_type: str
    likes: int
    comments: int
    caption: str
    hashtags: typing.Optional[str]
    url: typing.Optional[str]
    owner_username: str
    timestamp: typing.Optional[datetime]
    is_video: bool


class InstagramHTMLparser:
    @staticmethod
    def process(html_content: str) -> dict:
        """
        Processes the Instagram HTML content to extract relevant metadata and raw text.

        Args:
            html_content (str): The raw HTML content of the Instagram page.

        Returns:
            dict: A dictionary containing the extracted data including caption, image URL, title, and raw text.
        """
        from bs4 import BeautifulSoup

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract metadata
        caption = soup.find("meta", {"property": "og:description"})[
            "content"] if soup.find("meta", {"property": "og:description"}) else None
        image_url = soup.find("meta", {"property": "og:image"})[
            "content"] if soup.find("meta", {"property": "og:image"}) else None
        title = soup.find("meta", {"property": "og:title"})["content"] if soup.find(
            "meta", {"property": "og:title"}) else None

        # Remove unnecessary tags
        for data in soup(['style', 'script']):
            data.decompose()

        # Retrieve raw text content
        raw_text = ' '.join(soup.stripped_strings)

        return json.dumps({
            "caption": caption,
            "image_url": image_url,
            "title": title,
            "raw_text": raw_text
        }, indent=4)


class InstagramScraperController:
    def __init__(self):
        self.scrap_service = GeminiScraperService()
        self.bq_service = BigQueryService()
        self.logger = LoggerService()

    def find_short_code(self, post_url) -> str:
        pattern = r"\/p\/([a-zA-Z0-9_-]+)"
        match = re.search(pattern, post_url)

        if match:
            shortcode = match.group(1)
            print(f"Shortcode: {shortcode}")
            return shortcode
        else:
            print("No shortcode found.")

    def scrape_instagram_post(self, post_url: str, trace_id: str) -> PostModel:
        """
        Scrapes an Instagram post and returns it as a PostModel.

        Args:
            post_url (str): URL of the Instagram post to scrape.

        Returns:
            PostModel: Structured data of the Instagram post.
        """

        try:
            self.logger.set_trace_id(trace_id)
            result = self.scrap_service.scrape_page(
                prompt=INSTAGRAM_PROMPT[InstagramTarget.SINGLE_POST],
                url=post_url,
                response_schema=Post,
                html_processor=InstagramHTMLparser.process,
                trace_id=trace_id
            )
            clean_text = result.text.replace(
                'json\n', '').replace('```', '').replace('\n', '')
            data = json.loads(clean_text)
            post_model = PostModel(
                id=self.find_short_code(post_url),
                post_type=data.get("type", 'GraphImage'),
                likes=int(data.get("likes", 0)),
                comments=int(data.get("comments", 0)),
                is_video=True if data.get("type") == "video" else False,
                owner_username=data.get("owner_username"),
                batch_id=trace_id,
                caption_hashtags=', '.join(re.findall(
                    r"#(\w+)", data.get("caption", ""))),
                caption=data.get("caption"),
                url=post_url,
                shortcode=self.find_short_code(post_url),
                fetched_by="LLMScraperService",
                uploaded_at=datetime.now(),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                label_annotations=None,
                context=None,
                label_list=None
            )

            self.bq_service.set_one(
                post_model, trace_id=trace_id
            )

            return post_model
        except Exception as e:
            self.logger.error(ErrorModel(
                'create_post', ErrorCode.FLASK_ERR_CREATE, traceback.format_exc()))
            print(traceback.format_exc())
            raise ValueError(
                f"Failed to parse Gemini response: {e.__traceback__}") from e
