"""
Firecrawl Web Content Extraction Utility

This module provides functionality to extract web content using Firecrawl API.
Supports markdown, HTML, and AI-powered structured JSON extraction.
"""

import os
from typing import Optional, Dict, Any
from django.conf import settings


def extract_web_content(url: str, extraction_prompt: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract content from a web page using Firecrawl API.
    
    Args:
        url (str): The URL of the web page to extract
        extraction_prompt (str, optional): Custom AI prompt for JSON extraction
    
    Returns:
        dict: {
            'success': bool,
            'content_markdown': str,
            'content_html': str,
            'extracted_json': dict,
            'metadata': dict,
            'error': str (if failed)
        }
    """
    try:
        from firecrawl import Firecrawl  # Changed from FirecrawlApp
    except ImportError:
        return {
            'success': False,
            'error': 'Firecrawl SDK not installed. Please install firecrawl-py package.'
        }
    
    # Get API key from settings
    api_key = getattr(settings, 'FIRECRAWL_API_KEY', None)
    if not api_key:
        api_key = os.environ.get('FIRECRAWL_API_KEY')
    
    if not api_key:
        return {
            'success': False,
            'error': 'Firecrawl API key not configured. Please set FIRECRAWL_API_KEY in settings or environment.'
        }
    
    try:
        # Initialize Firecrawl
        from firecrawl import Firecrawl
        app = Firecrawl(api_key=api_key)
        
        # Default extraction prompt if not provided
        if not extraction_prompt:
            extraction_prompt = """Extract the following from this web page:
            - main_topic: The primary topic or subject
            - key_concepts: List of key concepts mentioned
            - author: Author name if available
            - publish_date: Publication date if available
            - technologies: Technologies or tools discussed
            - summary: Brief summary of the content
            """
        
        # Prepare formats for scraping
        formats = ['markdown', 'html']
        
        # Add JSON extraction format with prompt
        json_format = {
            'type': 'json',
            'prompt': extraction_prompt
        }
        formats.append(json_format)
        
        # Scrape the URL with multiple formats
        result = app.scrape(
            url,
            formats=formats
        )
        
        # The result is a Document object, access attributes directly
        if not result:
            return {
                'success': False,
                'error': 'Failed to scrape URL. The page may be inaccessible or blocked.'
            }
        
        # Get markdown content (direct attribute access)
        content_markdown = getattr(result, 'markdown', '') or ''
        if not content_markdown:
            return {
                'success': False,
                'error': 'No markdown content extracted from the page.'
            }
        
        # Get HTML content
        content_html = getattr(result, 'html', '') or ''
        
        # Get extracted JSON data
        extracted_json = getattr(result, 'extract', {}) or {}
        
        # Get metadata
        metadata_obj = getattr(result, 'metadata', None)
        if metadata_obj:
            # Convert metadata object to dict if needed
            if hasattr(metadata_obj, '__dict__'):
                metadata = {k: v for k, v in metadata_obj.__dict__.items() if not k.startswith('_')}
            else:
                metadata = {}
        else:
            metadata = {}
        
        return {
            'success': True,
            'content_markdown': content_markdown,
            'content_html': content_html,
            'extracted_json': extracted_json,
            'metadata': metadata,
            'error': None
        }
    
    except Exception as e:
        error_msg = str(e)
        
        # Handle common errors
        if 'API key' in error_msg or 'authentication' in error_msg.lower():
            error_msg = 'Invalid Firecrawl API key. Please check your configuration.'
        elif 'rate limit' in error_msg.lower():
            error_msg = 'Firecrawl API rate limit exceeded. Please try again later.'
        elif 'timeout' in error_msg.lower():
            error_msg = 'Request timeout. The page took too long to load.'
        elif 'not found' in error_msg.lower() or '404' in error_msg:
            error_msg = 'Page not found (404). Please check the URL.'
        
        return {
            'success': False,
            'error': error_msg
        }

