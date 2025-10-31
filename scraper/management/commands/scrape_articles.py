from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
from scraper import scraper
from scraper.models import Article

class Command(BaseCommand):
    help = 'Scrapes articles from a urls specified in provided .txt file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--urls',
            type=str,
            required=True,
            help='Path to .txt file containing new line separated urls to scrape'
        )

        parser.add_argument(
            '--title-h1',
            action='store_true',
            help='If provided, scrapes title from h1 tag otherwise uses title from <title> tag'
        )

        parser.add_argument(
            '--title-strict',
            action='store_true',
            help='If provided, does not save article if title is missing'
        )

    def handle(self, *args, **options):
        urls_path = options['urls']
        title_h1 = options['title_h1']

        path = Path(urls_path)
        if not path.exists():
            raise CommandError(f'File {urls_path} does not exist')
        if not path.is_file():
            raise CommandError(f'{urls_path} is not a file')

        with open(urls_path, 'r') as file:
            urls = [url.strip() for url in file.read().splitlines()]

        session = scraper.create_session()
        for i, url in enumerate(urls):
            if Article.objects.filter(url=url).exists():
                self.stdout.write(self.style.WARNING(f'Article {url} already saved in database, skipping'))
                continue
            self.stdout.write(self.style.SUCCESS(f'Scraping article {i+1} of {len(urls)}'))
            try:
                response = scraper.fetch(session, url)
            except scraper.RequestException as e:
                self.stderr.write(self.style.HTTP_BAD_REQUEST(f"Error fetching {url}: {e}"))
                continue
            try:
                html = scraper.render_page(response)
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error rendering {url}: {e}"))
                continue

            scraped_article = scraper.scrape_article(html, title_h1)
            if not scraped_article['html_content']:
                self.stderr.write(self.style.ERROR(f"No article content found at {url}"))
                continue
            if not scraped_article['date']:
                self.stderr.write(self.style.ERROR(f"No publish date found at {url}"))
                continue
            if not scraped_article['title']:
                if options['title_strict']:
                    self.stderr.write(self.style.ERROR(f"No title found at {url}"))
                    continue
                else:
                    self.stderr.write(self.style.WARNING(f"No title found at {url}"))


            article = Article(
                url=url,
                title=scraped_article['title'],
                html_content=scraped_article['html_content'],
                text=scraped_article['plain_text'],
                date=scraped_article['date']
            )
            article.save()
            self.stdout.write(self.style.SUCCESS(f"Saved article {article.url}"))

