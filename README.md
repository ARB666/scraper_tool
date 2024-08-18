# FastAPI Scraper Application

This is a FastAPI application for scraping product information from https://dentalstall.com/shop/. The app is containerized using Docker and can be easily built and run using Docker Compose.

## Prerequisites

1. Docker
2. Docker Compose

## Build and Run the Application

1. Clone the repository :

   - Open Command shell.
   - Run 'git clone https://github.com/ARB666/scraper_fast_api.git'.
   - Run 'cd scraper_fast_api'.

2. Build and run the app :

    - Run 'docker-compose up --build'

3. To start scraping, go to http://localhost:8000/docs and use the /scrape endpoint. The endpoint requires the following parameters:

    - api_token: A static API token (in our case it is "your_static_token").
    - page_limit: The number of pages to scrape.
    - proxy: (Optional) A proxy string.


4. After scraping, you can view the json file containing the data inside "scraper_fast_api/data" directory. Similarly, all images scraped are inside "scraper_fast_api/data/images".

5. Use the command 'docker-compose down-v' to stop and remove the containers.