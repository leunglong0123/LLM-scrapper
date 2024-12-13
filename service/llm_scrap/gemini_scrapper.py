import os
import traceback
from typing import Optional
from model.Error.ErrorModel import ErrorModel, ErrorCode
from service.logger_service import LoggerService
from service.llm_scrap.base import BaseLLMScraperService
from typing import Callable
import google.generativeai as genai

GEMINI_API_KEY = os.environ["GOOGLE_API_KEY"]
GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
LOCATION = os.environ["LOCATION"]


class GeminiScraperService(BaseLLMScraperService):
    """
    A specialized scraper service leveraging Google Gemini to extract structured data.
    """

    def __init__(self, base_prompt: Optional[str] = None):
        """
        Initialize the Gemini scraper service.

        Args:
            model_name (str): The Gemini model to use.
            base_prompt (Optional[str]): Default base prompt for the LLM.
        """
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash-002")
        self.logger = LoggerService()
        super().__init__(llm_model=self.model, base_prompt=base_prompt)

    def scrape_page(self, prompt: str, url: str, html_processor: Optional[Callable[[str], str]] = None, response_schema=list[Callable], trace_id=None) -> dict:
        """
        Scrape an Instagram page and extract structured post data.

        Args:
            url (str): URL of the Instagram page to scrape.
            html_processor (Optional[Callable[[str], str]]): Processor to preprocess HTML content.

        Returns:
            List[PostModel]: List of structured Instagram posts.
        """
        try:
            self.logger.set_trace_id(trace_id)
            html_content = self._fetch_page_content(url)

            processed_html = html_processor(
                html_content) if html_processor else html_content

            prompt = prompt.format(
                html_content=processed_html)

            structured_data = self.model.generate_content(
                contents=prompt + f'fetched from {url}'
            )

            return structured_data
        except Exception as e:
            self.logger.error(ErrorModel(
                self.__class__, ErrorCode.FLASK_ERR_CREATE, traceback.format_exc()))
            print(traceback.format_exc())
            raise ValueError(
                f"Failed to parse Gemini response: {e.__traceback__}") from e
