import base64
import os
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pypdf import PdfWriter

# --- CONFIGURATION ---
# IMPORTANT: Ensure your CSV file is in the same directory as this script.
CSV_FILE_NAME = "Integration_links.csv" 
URL_COLUMN_NAME = "Link"            
TITLE_COLUMN_NAME = "Title"         

FINAL_OUTPUT_FILENAME = "Merged_Documentation_Output.pdf"
TEMP_DIRECTORY = "./temp_pdfs"
# ---------------------

def get_urls_and_titles_from_csv(file_name, url_column, title_column):
    """
    Reads a CSV file and extracts lists of URLs and corresponding titles.
    
    The order of the URLs returned is the EXACT order they appear in the CSV.
    """
    data = []
    try:
        # --- ADJUST THIS LINE IF CSV READING FAILS ---
        # If the script fails, try different encoding (e.g., encoding='latin-1') 
        # or delimiter (e.g., sep=';').
        df = pd.read_csv(file_name, encoding='utf-8') 
        # ---------------------------------------------

        if url_column not in df.columns or title_column not in df.columns:
            print(f"ERROR: Missing one or both required columns ('{url_column}' or '{title_column}').")
            print(f"Available columns are: {', '.join(df.columns)}")
            return []
        
        # Iterate over the DataFrame rows, preserving the original order
        for index, row in df.iterrows():
            url = str(row[url_column]).strip()
            title = str(row[title_column]).strip()
            
            # Simple check for valid URL data
            if url.startswith('http'):
                data.append({'url': url, 'title': title})
        
        return data

    except FileNotFoundError:
        print(f"ERROR: The file '{file_name}' was not found. Please ensure it's in the same folder as the script.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while reading the CSV: {e}")
        return []


def save_and_merge_webpages_to_pdf(url_data, final_output_filename, temp_directory):
    """
    Converts each URL to a temporary PDF, named by the 'Title' column,
    and merges all individual PDFs into one final document.
    """
    if not url_data:
        print("No URLs to process. Exiting.")
        return
        
    print(f"Setting up headless Chrome to process {len(url_data)} URLs...")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    if not os.path.exists(temp_directory):
        os.makedirs(temp_directory)

    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"ERROR: Failed to initialize Chrome WebDriver. Ensure ChromeDriver is installed and in your PATH. Error: {e}")
        return

    # Print options (no headers/footers/background)
    print_params = {
        'printBackground': False,
        'displayHeaderFooter': False,
        'preferCSSPageSize': True,
        'scale': 1.0,
    }
    
    temp_pdf_paths = []

    try:
        # 1. Convert URLs to Individual PDFs (in CSV order)
        for i, item in enumerate(url_data):
            url = item['url']
            title = item['title']
            
            # Clean the title for a safe filename
            safe_title = re.sub(r'[\\/:*?"<>|]+', '_', title).strip()
            if not safe_title:
                 safe_title = f"page_{i+1}"
                 
            print(f"Processing {i+1}/{len(url_data)}: '{title}'")
            driver.get(url)
            
            result = driver.execute_cdp_cmd("Page.printToPDF", print_params)
            pdf_data = base64.b64decode(result['data'])
            
            temp_file_name = f"{safe_title}.pdf"
            output_path = os.path.join(temp_directory, temp_file_name)

            with open(output_path, "wb") as file:
                file.write(pdf_data)
                
            temp_pdf_paths.append(output_path)
            print(f"-> Saved temporary file: {temp_file_name}")

        driver.quit() 

        # 2. Merge Individual PDFs
        print("\nStarting PDF merge process...")
        merger = PdfWriter()
        
        # Files are appended in the same order they were processed (CSV order)
        for pdf_path in temp_pdf_paths:
            merger.append(pdf_path)
        
        with open(final_output_filename, "wb") as f_out:
            merger.write(f_out)
        merger.close()
        
        print(f"\n✅ **Successfully merged {len(temp_pdf_paths)} documents into:** {final_output_filename}")

    except Exception as e:
        print(f"A runtime error occurred during conversion or merging: {e}")

    finally:
        # 3. Cleanup
        print("\nCleaning up temporary files...")
        for pdf_path in temp_pdf_paths:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        if os.path.exists(temp_directory):
             os.rmdir(temp_directory)
        print("Cleanup complete.")
        
# --- Main Execution ---
if __name__ == "__main__":
    # 1. Get the URL and Title data from the CSV file
    url_data_list = get_urls_and_titles_from_csv(CSV_FILE_NAME, URL_COLUMN_NAME, TITLE_COLUMN_NAME)
    
    # 2. Pass the data to the conversion and merging function
    save_and_merge_webpages_to_pdf(url_data_list, FINAL_OUTPUT_FILENAME, TEMP_DIRECTORY)