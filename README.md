# Web Scraper - Django Article Scraping Application

A Django-based web scraping application that extracts articles from websites, stores them in a PostgreSQL database, and provides a REST API for accessing the scraped content.


## Prerequisites

- **Docker** (version 20.0 or higher)
- **Docker Compose** (version 1.29 or higher)

**OR** for running locally without Docker:

- **Python** 3.12 or higher
- **PostgreSQL** 16 or higher
- **pip** 



## Installation & Setup

### Option 1: Using Docker

#### 1. Clone the repository

```bash
git clone https://github.com/kkamilkasperek/web-scraper.git
cd web-scraper
```



**Configure settings.py:**
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0'] # Add your domain for release
DEBUG = False

```
Start containers:
```bash
docker-compose up --build
```

The application will be available at: **http://localhost:8000**

#### 5. Create a Superuser (Optional)

```bash
docker-compose exec web python manage.py createsuperuser
```


### Option 2: Local Development (Without Docker)

#### 1. Clone and Install Dependencies

```bash
git clone https://github.com/kkamilkasperek/web-scraper.git
cd web-scraper
python -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
```

#### 2. Install PostgreSQL

Follow the instructions for your operating system to install PostgreSQL 16 or higher. Make sure the PostgreSQL server is running.

#### 3. Configure PostgreSQL

Create a PostgreSQL database:

```bash
psql -U postgres
CREATE DATABASE scraper_db;
CREATE USER scraper_user WITH PASSWORD 'scraper_password';
GRANT ALL PRIVILEGES ON DATABASE scraper_db TO scraper_user;
\q
```

#### 3. Configure Environment Variables

Set the following environment variables or modify `settings.py`:

```bash
export POSTGRES_DB='your_db_name'
export POSTGRES_USER='your_username'
export POSTGRES_PASSWORD='your_password'
export POSTGRES_HOST='localhost'
export POSTGRES_PORT='5432'
```

#### 4. Run Migrations

```bash
python manage.py migrate
```

#### 5. Start the Development Server

```bash
python manage.py runserver
```

Or with Gunicorn:

```bash
gunicorn web_scraper.wsgi:application --bind 0.0.0.0:8000
```

## Usage

### Scraping Articles

The application provides a custom management command to scrape articles from a list of URLs.

#### 1. Create a text file with URLs

Create a file (e.g., `urls.txt`) with one URL per line:

```
https://example.com/article1
https://example.com/article2
https://example.com/article3
```

#### 2. Run the scraping command

**With Docker:**

```bash
docker-compose exec web python manage.py scrape_articles --urls=urls.txt
```

**Locally:**

```bash
python manage.py scrape_articles --urls=urls.txt
```

#### Optional Flags

- `--title-h1`: Look for title in `<h1>` tag firstly
- `--title-strict`: If title won't be found skip article, by default save without title


### API Endpoints

The application provides the following REST API endpoints:

#### List All Articles

```bash
GET http://localhost:8000/articles/
```

**Optional Query Parameters:**

- `?source=domain.com` - Filter articles by domain/URL substring


#### Get Single Article

```bash
GET http://localhost:8000/articles/{id}/
```



#### API Root

```bash
GET http://localhost:8000/
```

Returns available endpoints.

### Response Format

```json
{
  "id": 1,
  "url": "https://example.com/article",
  "title": "Article Title",
  "date": "30.10.2025 14:30:00",
  "html_content": "<article>...</article>",
  "text": "Plain text content..."
}
```


