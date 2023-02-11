import xml.etree.ElementTree as ET
import requests
import csv
import os
import datetime
import threading
from queue import Queue
from tqdm import tqdm

sitemap_folder = "sitemaps"
csv_folder = "csv"
sitemap_files = [f for f in os.listdir(sitemap_folder) if f.endswith(".xml")]
now = datetime.datetime.now()
datetime_str = now.strftime("%Y-%m-%d_%H-%M-%S")
filename = "404response_{}.csv".format(datetime_str)

if not os.path.exists(csv_folder):
    os.makedirs(csv_folder)

with open(os.path.join(csv_folder, filename), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Sitemap Path", "URL", "Status Code"])

    with tqdm(total=len(sitemap_files), desc="Processing Sitemaps") as sitemap_pbar:
        for sitemap_file in sitemap_files:
            tree = ET.parse(os.path.join(sitemap_folder, sitemap_file))
            root = tree.getroot()
            url_count = len(root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"))

            with tqdm(total=url_count, desc=sitemap_file) as url_pbar:
                q = Queue()
                def check_response():
                    while True:
                        url = q.get()
                        response = requests.get(url)
                        if response.status_code == 404:
                            writer.writerow([sitemap_file, url, response.status_code])
                            f.flush()
                        url_pbar.update(1)
                        q.task_done()
                for _ in range(min(32, url_count)):
                    t = threading.Thread(target=check_response)
                    t.daemon = True
                    t.start()
                for loc in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
                    q.put(loc.text)
                q.join()
            sitemap_pbar.update(1)

