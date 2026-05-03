from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def download_wikipedia_corpus(url: str) -> None:
    response = requests.get(url)
    # print(wiki_download_page.content)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    print(soup.prettify())
    # The links that come back here are relative, so we need to append them to the URL
    links = extract_download_links(soup)
    print(links)
    download_corpus_archives(url, links)


def extract_download_links(page: BeautifulSoup) -> list[str]:
    # Note: What's the difference between find_all and findAll?
    download_links = []
    for link in page.find_all("a"):
        download_links.append(link.get("href"))
    return download_links


def download_corpus_archives(url: str, filenames: list[str]) -> None:
    download_status = {}
    # First check if we have our download directoy, and create if not
    download_directory = "wikidownloads/"
    Path(download_directory).mkdir(parents=True, exist_ok=True)

    # Next start going through each file and download it
    for file in filenames:
        download_url = url + file
        downloaded_file_name = download_directory + file
        try:
            # Use streaming so we're not loading the whole thing into memory
            with requests.get(download_url, stream=True) as response:
                response.raise_for_status()
                with (
                    open(downloaded_file_name, "wb") as f,
                    tqdm(
                        desc=downloaded_file_name,
                        total=int(response.headers.get("content-length", 0)),
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                    ) as progress,
                ):
                    # Iterate over content chunks
                    for chunk in response.iter_content(
                        chunk_size=8192
                    ):  # This was a recommended thing from Gemini, can change up size
                        if chunk:
                            f.write(chunk)
                            progress.update(len(chunk))

                    download_status[file] = "SUCCESS"
        except Exception as e:
            print(f"There was an issue downloading {file}, Exception: {e}")
            download_status[file] = "FAILED"


# This was the most recent one when we started it
corpus_month = "2026-05-01"
with open("last_month_ran.rec") as f:
    last_month = int(f.read())
    current_month = datetime.now().month
    if last_month != current_month:
        corpus_month = datetime.now().strftime("%Y-%m-01")
        f.write(str(current_month))

url = f"https://dumps.wikimedia.org/other/mediawiki_content_current/enwiki/{corpus_month}/xml/bzip2/"
download_wikipedia_corpus(url)
