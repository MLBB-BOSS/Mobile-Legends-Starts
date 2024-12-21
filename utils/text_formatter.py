# utils/text_formatter.py

import logging

logger = logging.getLogger(__name__)

def format_profile_text(template: str, profile_info: dict) -> str:
    """
    Formats the profile text using the provided template and profile information.
    """
    try:
        formatted_text = template.format(**profile_info)
        logger.info("Formatted profile text successfully")
        return formatted_text
    except KeyError as e:
        logger.error(f"Missing key in profile_info: {e}")
        raise ValueError(f"Missing key in profile_info: {e}")
