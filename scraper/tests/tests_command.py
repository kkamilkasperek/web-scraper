from io import StringIO
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class ScrapeArticlesCommandTest(TestCase):
    """Tests for scrape_articles management command"""

    def test_command_requires_urls_argument(self):
        """Test that command raises error when --urls argument is missing"""
        out = StringIO()
        with self.assertRaises(CommandError):
            call_command('scrape_articles', stdout=out)

    def test_command_with_nonexistent_file(self):
        """Test that command raises error when --urls argument is not a file"""
        out = StringIO()
        with self.assertRaises(CommandError):
            call_command('scrape_articles', '--urls', 'nonexistent.txt', stdout=out)
