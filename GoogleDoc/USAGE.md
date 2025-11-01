# Documentation Processing Pipeline

This document outlines the step-by-step process for generating a compressed PDF of the Google Cloud Gemini documentation using the provided Python scripts.

## Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3**: Make sure Python 3 is installed on your system.
2.  **Required Python Libraries**: Install the necessary libraries using pip:
    ```bash
    pip install requests beautifulsoup4 pandas selenium pypdf
    ```
3.  **ChromeDriver**: The `web_to_pdf_merger.py` script uses Selenium with Chrome. You must have ChromeDriver installed and available in your system's PATH. You can download ChromeDriver from the official website.

## Step-by-Step Instructions

### Step 1: Fetch Documentation Links

This step uses `getlinks_csv.py` to scrape the documentation URLs from the Google Cloud Gemini documentation website and saves them into a CSV file.

**To execute:**

Run the following command in your terminal:

```bash
python getlinks_csv.py
```

**Output:**

This will create a file named `Integration_links.csv` in the same directory. This file contains the titles and URLs of the documentation pages.

### Step 2: Convert and Merge Webpages to PDF

This step uses `web_to_pdf_merger.py` to read the `Integration_links.csv` file, convert each URL into a PDF, and then merge all the individual PDFs into a single file.

**To execute:**

Run the following command in your terminal:

```bash
python web_to_pdf_merger.py
```

**Output:**

This will create a file named `Merged_Documentation_Output.pdf`. This file is a combination of all the documentation pages.

### Step 3: Compress the Merged PDF

The merged PDF file can be quite large. This final step uses `pdf_compressor.py` to reduce the file size of the `Merged_Documentation_Output.pdf`.

**Default Usage (No Arguments):**

If you run the script without any arguments, it will automatically:
*   Use `Merged_Documentation_Output.pdf` as the input file.
*   Save the compressed file as `compressed_Merged_Doc.pdf`.
*   Use the default compression level (9).

To execute with default settings:
```bash
python pdf_compressor.py
```

**Custom Usage:**

You can still specify the input file, output file, and compression level as command-line arguments.

To execute with custom settings:
```bash
python pdf_compressor.py [input_filename.pdf] [output_filename.pdf] -c [compression_level]
```

**Example:**

To compress the PDF with a high compression level (e.g., 5) and save it as `compressed_documentation.pdf`, use the following command:

```bash
python pdf_compressor.py Merged_Documentation_Output.pdf compressed_documentation.pdf -c 5
```

**Output:**

This will create a new, smaller PDF file with the specified name. The script will print the original size, the new size, and the percentage reduction.
