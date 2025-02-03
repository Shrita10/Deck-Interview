# Deck Interview Project

This document outlines the steps to set up and run the Deck Interview project.

## Project Structure

The project directory structure should resemble the following:

├── README.md
├── requirements.txt
├── src/
│   ├── init.py
│   ├── config.py
│   ├── scraper.py
│   └── tests/
│       ├── init.py
│       └── test_scraper.py
└── .gitignore

## Setup Instructions

1. **Navigate to the project directory:**
`cd deck_interview`

2. **Create a virtual environment (Python 3 required):**
`python3 -m venv venv`

3. **Activate the virtual environment:**
* **macOS/Linux:**
`source venv/bin/activate`
* **Windows:**
`venv\Scripts\activate`

4. **Install project dependencies:**
Download the `requirements.txt` file (attached separately) and install the required packages:
`pip install -r requirements.txt`

5. **Install Playwright browsers:**
`playwright install`

6. **Run the tests:**
`python3 src/tests/test_scraper.py`

7. If running the tests more than once, please clear the following:

* `__pycache__` directories 
* The `downloads` folder 
* The `extracted_json` file 

