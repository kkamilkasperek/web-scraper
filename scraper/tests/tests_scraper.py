import datetime

from scraper import scraper
from requests_html import HTML
from pathlib import Path
import unittest


class ScraperTest(unittest.TestCase):
    """Tests for scraper module"""

    def load_html_file(self, filename):
        """Helper method to load HTML test files"""
        test_dir = Path(__file__).parent
        file_path = test_dir / filename
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HTML(html=content)

    def test_scrape_article_with_complete_article(self):
        """Test scraping article with all elements present"""
        html = self.load_html_file('test_with_article_tag.html')
        result = scraper.scrape_article(html, title_h1=False)

        self.assertIsNotNone(result['title'])
        self.assertEqual(result['title'], 'Test Article Title')
        self.assertIsNotNone(result['html_content'])
        self.assertIn('<h1>Article Heading</h1>', result['html_content'])
        self.assertIsNotNone(result['plain_text'])
        self.assertIn('Article Heading', result['plain_text'])
        self.assertIn('first paragraph', result['plain_text'])
        self.assertIsNotNone(result['date'])
        self.assertIn('2025-01-15', result['date'].isoformat())

    def test_scrape_article_with_title_h1_flag_true(self):
        """Test scraping with title_h1=True prefers h1 over title tag"""
        html = self.load_html_file('test_with_article_tag.html')
        result = scraper.scrape_article(html, title_h1=True)

        self.assertEqual(result['title'], 'Article Heading')

    def test_scrape_article_with_title_h1_flag_false(self):
        """Test scraping with title_h1=False prefers title over h1 tag"""
        html = self.load_html_file('test_with_article_tag.html')
        result = scraper.scrape_article(html, title_h1=False)

        self.assertEqual(result['title'], 'Test Article Title')

    def test_scrape_article_without_article_tag_returns_empty(self):
        """Test that scraping without article tag returns None values"""
        html = self.load_html_file('test_without_article_tag.html')
        result = scraper.scrape_article(html)

        self.assertIsNone(result['title'])
        self.assertIsNone(result['html_content'])
        self.assertIsNone(result['plain_text'])
        self.assertIsNone(result['date'])

    def test_scrape_article_without_title_tag_uses_h1(self):
        """Test that h1 is used when title tag is missing"""
        html = self.load_html_file('test_without_title_tag.html')
        result = scraper.scrape_article(html, title_h1=False)

        # Should fallback to h1 when title is not found
        self.assertEqual(result['title'], 'Page Heading Without Title Tag')

    def test_scrape_article_extracts_date_from_time_tag(self):
        """Test date extraction from time tag with datetime attribute"""
        html = self.load_html_file('test_with_article_tag.html')
        result = scraper.scrape_article(html)
        date = result['date'].isoformat()

        self.assertIsNotNone(result['date'])
        self.assertIn('2025-01-15', date)

    def test_scrape_article_extracts_date_from_paragraph(self):
        """Test date extraction from paragraph when time tag is missing"""
        html = self.load_html_file('test_without_time_tag.html')
        result = scraper.scrape_article(html)
        date = result['date'].isoformat()
        self.assertIsNotNone(result['date'])
        # dateparser should parse "14 Październik 2024"
        self.assertIn('2024-10-14', date)

    def test_scrape_article_empty_dict_when_no_article(self):
        """Test that all dict values are None when no article tag exists"""
        html = self.load_html_file('test_without_article_tag.html')
        result = scraper.scrape_article(html)

        expected = {
            'title': None,
            'html_content': None,
            'plain_text': None,
            'date': None
        }

        self.assertDictEqual(result, expected)

    def test_scrape_article_plain_text_content(self):
        """Test plain text extracts text without HTML tags"""
        html = self.load_html_file('test_with_article_tag.html')
        result = scraper.scrape_article(html)

        # Verify plain text content
        self.assertIn('Article Heading', result['plain_text'])
        self.assertIn('January 15, 2025', result['plain_text'])
        self.assertIn('first paragraph', result['plain_text'])
        self.assertIn('second paragraph', result['plain_text'])

        # Verify no HTML tags
        self.assertNotIn('<', result['plain_text'])
        self.assertNotIn('>', result['plain_text'])

    def test_scrape_article_date_datetime_instance(self):
        """Test that date is returned as datetime.datetime instance"""
        html = self.load_html_file('test_with_article_tag.html')
        result = scraper.scrape_article(html)

        self.assertIsNotNone(result['date'])
        self.assertIsInstance(result['date'], datetime.datetime)

    def test_scrape_article_with_polish_date(self):
        """Test date extraction with Polish date format"""
        html = self.load_html_file('test_without_time_tag.html')
        result = scraper.scrape_article(html)

        # Polish date "14 Październik 2024" should be parsed
        self.assertIsNotNone(result['date'])
        self.assertTrue(result['date'].isoformat().startswith('2024-10-14'))

    def test_scrape_article_title_priority_with_both_tags(self):
        """Test title selection priority when both title and h1 exist"""
        html = self.load_html_file('test_with_article_tag.html')

        # With title_h1=False, should prefer <title> tag
        result_title_first = scraper.scrape_article(html, title_h1=False)
        self.assertEqual(result_title_first['title'], 'Test Article Title')

        # With title_h1=True, should prefer <h1> tag
        result_h1_first = scraper.scrape_article(html, title_h1=True)
        self.assertEqual(result_h1_first['title'], 'Article Heading')


