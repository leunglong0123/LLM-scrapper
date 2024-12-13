from playwright.sync_api import sync_playwright
from typing import Callable, Optional
from abc import ABC
from proto import Message


class BaseLLMScraperService(ABC):
    def __init__(self, llm_model: Callable, base_prompt: Optional[str] = None):
        """
        Initialize the scraper service.

        :param llm_model: Callable that invokes the LLM for processing.
        :param base_prompt: Default prompt for the LLM.
        """
        self.llm_model = llm_model
        self.base_prompt = base_prompt

    def set_scrap_prompt(self, prompt: str):
        """
        Configure the prompt to be used for LLM processing.

        :param prompt: The base prompt for the LLM.
        """
        self.base_prompt = prompt

    def scrape_page(
        self, url: str, html_processor: Optional[Callable[[str], str]] = None
    ) -> Message:
        """
        Generic function to scrape and process a webpage.

        :param url: The URL of the webpage to scrape.
        :param html_processor: A callable that processes HTML and extracts relevant content.
        :return: A dictionary containing structured data parsed by the LLM.
        """
        html_content = self._fetch_page_content(url)

        processed_html = html_processor(
            html_content) if html_processor else html_content

        if not self.base_prompt:
            raise ValueError(
                "Base prompt is not configured. Use `set_scrap_prompt`.")
        prompt = f"{self.base_prompt}\n\n{processed_html}"

        return self.llm_model(prompt)

    def _fetch_page_content(self, url: str) -> str:
        """
        Fetches the page content using Playwright.

        :param url: The URL to scrape.
        :return: The HTML content of the page.
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            page.goto(url, timeout=60000)
            page.wait_for_timeout(5000)  # Adjust as needed for page loading
            html_content = page.content()

            browser.close()

        return html_content
