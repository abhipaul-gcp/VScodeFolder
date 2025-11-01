import requests
from bs4 import BeautifulSoup
import csv

def get_recaptcha_docs_links(base_url, output_csv="Integration_links.csv"):
    """
    Extracts reCAPTCHA documentation links from the left navigation pane and saves them to a CSV file.

    Args:
        base_url: The base URL of the reCAPTCHA documentation overview.
        output_csv: The name of the CSV file to save the links to.
    """
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        nav_pane = soup.find("nav", class_="devsite-nav")

        if not nav_pane:
            print("Navigation pane not found.")
            return

        results = []
        nav_items = nav_pane.find_all("li", class_="devsite-nav-item")

        for item in nav_items:
            anchor = item.find("a", class_="devsite-nav-title")
            if anchor:
                title = anchor.text.strip()
                href = "https://cloud.google.com" + anchor.get("href")
                results.append({"Title": title, "Link": href})

                # Check for sub-items (nested lists)
                sub_items = item.find_all("li", class_="devsite-nav-item-sub")
                if sub_items:
                    for sub_item in sub_items:
                        sub_anchor = sub_item.find("a", class_="devsite-nav-title")
                        if sub_anchor:
                            sub_title = sub_anchor.text.strip()
                            sub_href = "https://cloud.google.com" + sub_anchor.get("href")
                            results.append({"Title": f"{title} - {sub_title}", "Link": sub_href})

        # Write results to CSV
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Title", "Link"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(results)

        print(f"Successfully saved reCAPTCHA links to {output_csv}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
base_url = "https://cloud.google.com/gemini/enterprise/docs"
get_recaptcha_docs_links(base_url)
