# Event Data Scraper

Note: some of the informations in the given objectives weren't extracted, this is because the website didn't contain the information regarding those attributes.

This Python script scrapes event data from Eventbrite URLs and saves it to a CSV file.

## Overview

This script utilizes Python along with `requests`, `BeautifulSoup`, and `pandas` libraries to scrape event information from Eventbrite event pages. It extracts event names, dates, locations, descriptions, and pricing information based on specified CSS classes from HTML elements.

## Features

- Scrapes event data from multiple Eventbrite URLs.
- Handles dynamic pricing elements and nested HTML structures for robust data extraction.
- Saves scraped data into a CSV file for further analysis or integration with other systems.

## Installation

1. Clone the repository

2. Install the required libraries: `requests`, `beautifulsoup4`, and `pandas`


## Usage

1. Modify the `urls`, `name_classes`, `date_classes`, `location_classes`, `description_classes`, `pricing_classes`, and `referers` lists in the `scrape_data.py` file to match your Eventbrite event pages.

2. Run the script

   This will execute the data scraping process. It will fetch event details from the specified URLs, process the data, and save it to a CSV file named `event_data.csv` in the same directory.

## Configuration

- `urls`: List of Eventbrite event URLs to scrape.
- `name_classes`: List of CSS classes for event names.
- `date_classes`: List of CSS classes for event dates.
- `location_classes`: List of CSS classes for event locations.
- `description_classes`: List of CSS classes for event descriptions.
- `pricing_classes`: List of CSS classes for event pricing.
- `referers`: List of referer URLs corresponding to each Eventbrite URL.

Ensure the CSS classes provided match the structure of the event pages you are scraping. Adjust the lists based on your specific requirements and the HTML structure of the event pages.

## Contributing

Contributions are welcome! Fork the repository, make your changes, and submit a pull request.
