import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper import WebScraper

def main():
    scraper = WebScraper()
    try:
        page = scraper.login()
        if not page:
            print("Login failed!")
            return

        data = scraper.extract_data()
        if data:
            print("Data extraction is done!")
            scraper.save_data(data)
        else:
            print("Data extraction failed!")
            return
        if page:  
            scraper.download_bills(page)
        else:
            print("Download bills failed!")

    finally:
        scraper.close()

if __name__ == "__main__":
    main()