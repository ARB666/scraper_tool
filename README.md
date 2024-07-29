# FastAPI Scraper Application

This is a FastAPI application for scraping product information. The app is containerized using Docker and can be easily built and run using Docker Compose.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Build and Run the Application

1. Clone the repository:

   git clone https://github.com/yourusername/yourrepo.git
   cd yourrepo

2. Build and run the app using :

    docker-compose up --build

3. To start scraping, use the /scrape endpoint. The endpoint requires the following parameters:

    api_token: A static API token (in our case it is "your_static_token").
    page_limit: The number of pages to scrape.
    proxy: (Optional) A proxy string.
    You can use the interactive documentation at http://localhost:8000/docs or a tool like curl to call this endpoint.


4. After scraping, you can view the json file containing the data inside /yourrepo/data. Similarly, all images scraped are inside /yourrepo/data/images.