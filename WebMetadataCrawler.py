import argparse
import requests
from bs4 import BeautifulSoup
import csv
import os


class WebMetadataCrawler:
    def __init__(self, url, words):
        self.url = url
        self.title = ""
        self.meta_description = ""
        self.word_counts = {word: 0 for word in words}

    def crawl_and_parse(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:

                soup = BeautifulSoup(response.text, 'html.parser')
                self.title = soup.title.string if soup.title else "No title found"
                meta_tag = soup.find('meta', attrs={'name': 'description'})
                if meta_tag:
                    self.meta_description = meta_tag.get('content')

                page_content = soup.get_text()
                script_tags = soup.find_all('script')
                for script in script_tags:
                    script.extract()

                for word in self.word_counts.keys():
                    self.word_counts[word] = page_content.lower().count(
                        word.lower())
            else:
                print(
                    f"Failed to retrieve the page. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print("Error: Unable to connect to the website.")
        except Exception as e:
            print("An error occurred:", str(e))

    def export_to_csv(self, filename):
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Attribute", "Value"])
                writer.writerow(["Title", self.title])
                writer.writerow(["Meta Description", self.meta_description])
                for word, count in self.word_counts.items():
                    writer.writerow([f"Word Count ('{word}')", count])

            print(f"Data exported to {filename} successfully.")
        except Exception as e:
            print(f"An error occurred while exporting to CSV: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Web Metadata Crawler")
    parser.add_argument("--url", default="https://www.valuemyweb.com/")
    parser.add_argument("--words", nargs='+', default=["valuemyweb"])
    args = parser.parse_args()

    crawler = WebMetadataCrawler(args.url, args.words)
    crawler.crawl_and_parse()

    filename = input("Enter the CSV filename for export: ")
    crawler.export_to_csv(filename)


if __name__ == "__main__":
    main()
