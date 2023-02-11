## 404 Response Checker for XML Sitemaps

The following script checks the responses for all URLs in a set of XML sitemap files and writes the 404 responses to a CSV file.

## Requirements

*   `xml.etree.ElementTree` module to parse XML files
*   `requests` module to check the URL responses
*   `csv` module to write the 404 responses to a CSV file
*   `os` module to list the files in a folder and create the csv folder if it does not exist
*   `datetime` module to get the current date and time
*   `threading` module to check the URL responses in parallel
*   `queue` module to store the URLs for processing by the worker threads
*   `tqdm` module to display progress bars for processing the sitemap files and checking the URL responses

## Inputs

*   The folder containing the XML sitemap files.
*   The folder to save the CSV file with the 404 responses.

## Outputs

*   A CSV file with the 404 responses, including the following columns:
    *   Sitemap Path: The path of the sitemap file containing the URL.
    *   URL: The URL that returned a 404 response.
    *   Status Code: The HTTP status code returned by the URL.

## Usage

1.  Install the required modules.
2.  Replace `sitemap_folder` and `csv_folder` with the desired folders.
3.  Run the script.
