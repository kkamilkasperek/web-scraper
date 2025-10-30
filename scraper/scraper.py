from requests import RequestException
from requests_html import HTMLSession
from fake_useragent import UserAgent
import logging, dateparser

logger = logging.getLogger('scraper')

def create_session():
    user_agent = UserAgent().random
    return HTMLSession(browser_args=[
        '--no-sandbox',
        f'--user-agent={user_agent}'
    ])

def fetch(session, url, timeout=10):
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    logger.info(f'Request successful: {url}')
    return response

def render_page(response, sleep=2, timeout=20):
    response.html.render(sleep=sleep, timeout=timeout, keep_page=True)
    logger.info(f'Page rendered: {response.url}')
    return response.html

def scrape_article(html, title_h1=False):
    parsed_article = {
        'title': None,
        'html_content': None,
        'plain_text': None,
        'date': None,
    }
    # find html content
    article_match = html.find('article', first=True)
    if article_match:
        parsed_article['html_content'] = article_match.html
        parsed_article['plain_text'] = article_match.text
    else:
        return parsed_article # return empty dict if no article found
    # find title
    selectors = ['h1', 'title'] if title_h1 else ['title', 'h1']
    for selector in selectors:
        title_match = html.find(selector, first=True)
        if title_match:
            if title_h1 and selector == 'title':
                logger.warning('h1 tag not found, using title tag instead')
            elif not title_h1 and selector == 'h1':
                logger.warning('title tag not found, using h1 tag instead')
            parsed_article['title'] = title_match.text
            break
    # find date
    date_match = html.find('time', first=True)
    if not date_match:
        possible_dates = html.find('p')
        for possible_date in possible_dates:
            date = dateparser.parse(possible_date.text)
            if date:
                # assume first date is most likely date of publication
                date_match = possible_date
                break
    date = dateparser.parse(date_match.text) if date_match else None
    parsed_article['date'] = date if date else None
    return parsed_article





