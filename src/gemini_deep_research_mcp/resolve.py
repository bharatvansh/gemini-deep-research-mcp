"""Resolve Gemini grounding redirect URLs to actual source URLs."""
from __future__ import annotations

import logging
import re
from functools import lru_cache
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

# Pattern to match Gemini grounding redirect URLs
REDIRECT_URL_PATTERN = re.compile(
    r'https://vertexaisearch\.cloud\.google\.com/grounding-api-redirect/[A-Za-z0-9_-]+'
)

# HTTP timeout for resolving redirects (seconds)
RESOLVE_TIMEOUT = 10.0


@lru_cache(maxsize=256)
def resolve_redirect_url(url: str) -> Optional[str]:
    """Follow a redirect URL and return the final destination.
    
    Args:
        url: A Gemini grounding redirect URL
        
    Returns:
        The resolved destination URL, or None if resolution fails
    """
    if not url or 'grounding-api-redirect' not in url:
        return None
    
    try:
        # Use HEAD request to follow redirects without downloading content
        # follow_redirects=False so we can capture the Location header
        with httpx.Client(timeout=RESOLVE_TIMEOUT, follow_redirects=False) as client:
            response = client.head(url)
            
            # The redirect URL returns a 302/301 with Location header
            if response.status_code in (301, 302, 303, 307, 308):
                location = response.headers.get('location')
                if location:
                    logger.debug(f"Resolved {url[:60]}... -> {location}")
                    return location
            
            # If no redirect, try GET as fallback (some servers don't respond to HEAD)
            response = client.get(url, follow_redirects=True)
            final_url = str(response.url)
            
            # Only return if we actually got redirected somewhere different
            if final_url != url and 'grounding-api-redirect' not in final_url:
                logger.debug(f"Resolved {url[:60]}... -> {final_url}")
                return final_url
                
    except httpx.TimeoutException:
        logger.warning(f"Timeout resolving URL: {url[:80]}...")
    except httpx.HTTPError as e:
        logger.warning(f"HTTP error resolving URL: {e}")
    except Exception as e:
        logger.warning(f"Unexpected error resolving URL: {e}")
    
    return None


def resolve_sources_in_text(text: str) -> str:
    """Find and resolve all grounding redirect URLs in text.
    
    Scans the text for Gemini grounding redirect URLs and replaces them
    with resolved destination URLs where possible.
    
    Args:
        text: The text containing potential redirect URLs
        
    Returns:
        Text with redirect URLs replaced by resolved URLs where possible
    """
    if not text or 'grounding-api-redirect' not in text:
        return text
    
    def replace_url(match: re.Match) -> str:
        original_url = match.group(0)
        resolved = resolve_redirect_url(original_url)
        if resolved:
            return resolved
        # Keep original if resolution failed
        return original_url
    
    return REDIRECT_URL_PATTERN.sub(replace_url, text)
