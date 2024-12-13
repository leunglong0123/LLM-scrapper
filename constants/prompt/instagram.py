from enum import Enum


class InstagramTarget(Enum):
    SINGLE_POST = "SINGLE_POST"
    PROFILE = "PROFILE"
    FEED = "FEED"
    STORY = "STORY"
    REELS = "REELS"
    LIVE = "LIVE"


INSTAGRAM_PROMPT = {
    InstagramTarget.SINGLE_POST: """
        Extract Instagram posts data from the provided input HTML and return as Json Object.

        The information you need to extract includes:
        - Post ID (shortcode) get it from url /p/shortcode
        - Post type (image or video)
        - Number of likes
        - Number of comments
        - Caption text
        - Hashtags in the caption
        - URL of the post
        - Username of the post's owner
        - Timestamp of the post (if available)
        - Is the post a video? (boolean)

        Return the extracted information in JSON format, with the following structure:
        {{
            "shortcode": "string",
            "post_type": "string",
            "likes": int,
            "comments": int,
            "caption": "string",
            "hashtags": "string",
            "url": "string",
            "owner_username": "string",
            "timestamp": "datetime",
            "is_video": bool
        }}

        HTML input:
        {html_content}

        parse the provided HTML content and return the structured data in the required JSON format.
        """
}
