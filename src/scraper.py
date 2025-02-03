#Importing files
from playwright.sync_api import sync_playwright
import json
import os 

class WebScraper:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def login(self):
        try:
            #Playwright starts
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=False)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            self.page.goto('https://deck-dev-eastus2-academy.yellowrock-2749f805.eastus2.azurecontainerapps.io/mfa-login')
            credentials_text = self.page.query_selector('div.text-sm.text-gray-500.mb-2').inner_text()
            username = credentials_text.split('Username: ')[1].split('\n')[0].strip()
            password = credentials_text.split('Password: ')[1].strip()


            self.page.evaluate('''() => {
                const forms = document.querySelectorAll('form');
                forms.forEach(form => {
                    const inputs = form.querySelectorAll('input, button');
                    inputs.forEach(input => {
                        input.disabled = false;
                    });
                });
            }''')

            #Scraper goes through login
            self.page.fill('#username', username)
            self.page.fill('#password', password)
            self.page.click('button:has-text("Continue to MFA")')

            #Scraper goes through 2FA and selects email
            # Please replace value = "email" with sms for sms and authenticator for authenticator app
            self.page.wait_for_selector('button[name="mfa_method"][value="email"]', timeout=50000)
            self.page.click('button[name="mfa_method"][value="email"]')

            #Scraper goes to the page which expects verification code
            self.page.wait_for_selector('div.text-sm.text-gray-500.mb-2', timeout=5000)
            verification_code_text = self.page.query_selector('div.text-sm.text-gray-500.mb-2').inner_text()
            verification_code = verification_code_text.split('Demo Verification Code:')[1].strip()
            self.page.fill('#mfa_code', verification_code)
            self.page.click('button:has-text("Verify")')

            #Scraper reaches dashboard
            self.page.wait_for_selector('h2.text-3xl.font-bold.text-blue-800', timeout=50000)
            print("Dashboard loaded, starting data extraction")
            return self.page
        
        #Exception Handling
        except Exception as e:
            print(f"Login failed: {e}")
            return None

    def extract_data(self):
        try:
            print("Running extract_data function")
            data = []

            account_cards = self.page.query_selector_all('div.bg-white.rounded-lg.shadow-md.p-6')
            if not account_cards:
                return None

            for card in account_cards:
                account_data = {}
                address_element = card.query_selector('h3.font-semibold.text-gray-800.text-xl')
                account_number_element = card.query_selector('p.text-gray-600:has-text("Account #:")')
                if address_element and account_number_element:
                    account_data['address'] = address_element.inner_text() if address_element else None
                    account_number_element = card.query_selector('p.text-gray-600:has-text("Account #:")')
                    account_data['account_number'] = account_number_element.inner_text().split(": ")[1] if account_number_element else None
                    due_date_element = card.query_selector('div.space-y-3 div:has-text("Due Date:") span:nth-child(2)')
                    account_data['due_date'] = due_date_element.inner_text() if due_date_element else None
                    last_month_usage_element = card.query_selector('div.space-y-3 div:has-text("Last Month Usage:") span:nth-child(2)')
                    account_data['last_month_usage'] = last_month_usage_element.inner_text() if last_month_usage_element else None
                    data.append(account_data)
            return data

        except Exception as e:
            print(f'Error extracting data: {e}')
            return None 
        
    def download_bills(self, page):
        try:
            download_links = page.query_selector_all('a[download], button:has-text("Download"), a:has-text("Download Bill")')
            
            download_dir = "./downloads" 
            os.makedirs(download_dir, exist_ok=True) 

            for link in download_links:
                link.click()
                with page.expect_download() as download_info:
                    pass
                download = download_info.value
                original_filename = download.suggested_filename
                base_name, ext = os.path.splitext(original_filename)
                counter = 1
                while True:  
                    new_filename = f"{base_name}_{counter}{ext}"
                    download_path = os.path.join(download_dir, new_filename)

                    if not os.path.exists(download_path):  
                        break  
                    counter += 1  

                download.save_as(download_path)
                print(f"Download path: {download_path}")

        except Exception as e:
            print(f"Error downloading bills: {e}")

    def save_data(self, data):
        try:
            with open('extracted_data.json', 'w') as f:
                json.dump(data, f, indent=4)
       
        except Exception as e:
            print(f'Error saving data IN SAVE: {e}')
    #Playwright ends, I noticed not adding these gave me a lot of issues like "loop ending incorrectly"
    #It was really important to close everything correctly
    def close(self):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()