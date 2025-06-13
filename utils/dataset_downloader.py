# External imports
import os
import requests
import yaml
import time
import logging

from bs4 import BeautifulSoup
from pathlib import Path
from tqdm import tqdm


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("dataset_downloader.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("DatasetDownloader")


# Constants at module level
SOURCES = {
    "github_iqbal_demystified": "https://raw.githubusercontent.com/AzeemGhumman/iqbal-demystified-dataset/master/data",
    "iqbal_cyberlibrary": "https://iqbalcyberlibrary.net",
    "allama_iqbal_poetry": "https://blogs.library.mcgill.ca/islamicstudieslibrary/allama-iqbal-poetry-%DA%A9%D9%84%D8%A7%D9%85-%D8%B9%D9%84%D8%A7%D9%85%DB%81-%D9%85%D8%AD%D9%85%D8%AF-%D8%A7%D9%82%D8%A8%D8%A7%D9%84/",
    "iqbal_review": "https://www.allamaiqbal.com/publications/journals/review/",
    "rekhta": "https://www.rekhta.org/poets/allama-iqbal/ghazals"
}


class DatasetDownloader:
    """
    A class to download dataset from various sources.
    """
    
    def __init__(self, output_dir: str = "data", number_of_books: int = 11, max_workers: int = 5) -> None:
        """Initialize the dataset downloader with configuration parameters.
        
        Args:
            output_dir (str): Directory to store the downloaded files. Defaults to "data".
            max_workers (int): Maximum number of concurrent workers. Defaults to 5.
        """
        if max_workers < 1:
            raise ValueError("max_workers must be at least 1")
    
        self.output_dir = Path(output_dir)
        self.max_workers = max_workers
        self.number_of_books = number_of_books
        # Constant variables
        self.sources = SOURCES


    def download_from_github(self, source_name: str = "github_iqbal_demystified"):
        """Download dataset from GitHub."""
        logger.info("Downloading dataset from GitHub")

        # Check if the source name is valid
        if source_name not in self.sources:
            raise ValueError(f"Source name {source_name} not found in sources")
        
        # Get the source name and base url
        base_url = self.sources[source_name]
        folders = ["lists", "poems"]
        
        # Create the folders for the source
        for folder in folders:
            output_path = self.output_dir / source_name / folder
            os.makedirs(output_path, exist_ok=True)

        # Fetch the list metadata from the GitHub repository
        book_ids = self._download_github_lists(source_name, base_url, folder="lists")
        # Fetch the poems from the GitHub repository
        poem_ids = self._download_github_poems(source_name, base_url, folder="poems", book_ids=book_ids)

        logger.info(f"Completed fetching data from Iqbal Demystified GitHub repository. Total poems fetched: {len(poem_ids)}")

    
    def _download_github_lists(self, source_name: str, base_url: str, folder: str) -> list:
        """Fetch the list metadata from the GitHub repository."""

        logger.info(f"Fetching book metadata from {folder} folder")
        
        book_ids = []
        # Fetch the metadata for each book along with the poems
        for index in tqdm(range(self.number_of_books), desc="Fetching book metadata"):
            book_id = f"{index+1:03}"
            # Create the output path for the book
            output_path = self.output_dir / source_name / folder / f"List_{book_id}.yaml"
            # Fetch the metadata for the book using requests
            metadata_url = f"{base_url}/lists/List_{book_id}.yaml"
            # Skip if already downloaded
            if output_path.exists():
                logger.debug(f"List_{book_id}.yaml already exists, skipping download")
                book_ids.append(book_id)
                continue

            try:
                response = requests.get(metadata_url)
                response.raise_for_status()
                if response.status_code == 200:
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(response.text)
                
                    book_ids.append(book_id)
                    logger.info(f"Successfully fetched List_{book_id}.yaml")
            except Exception as e:
                logger.error(f"Error fetching metadata for {book_id}: {e}")
            
            # Respect rate limits
            time.sleep(0.5)

        logger.info(f"Fetched {len(book_ids)} book lists")
        return book_ids
    
    
    def _download_github_poems(self, source_name: str, base_url: str, folder: str, book_ids: list) -> list:
        """Fetch the poems from the GitHub repository."""
        # List to store the fetched poems
        fetched_poems = []
        # Fetch the poems for each book by first reading the list metadata and then fetching the poems
        for id in tqdm(book_ids, desc=f"Fetching books metadata, poems and shers"):
            metadata_path = self.output_dir / source_name / "lists" / f"List_{id}.yaml"
            if not metadata_path.exists():
                logger.error(f"Metadata file for book {id} does not exist")
                continue

            # Create directory for this book's poems
            poems_path = self.output_dir / source_name / folder / id
            os.makedirs(poems_path, exist_ok=True)

            # Load and parse the list file
            try:
                with open(metadata_path, "r", encoding="utf-8") as f:
                    book_metadata = yaml.safe_load(f)
            except Exception as e:
                logger.error(f"Error parsing list file for book {id}: {str(e)}")
                continue
 
            # Extract all poem IDs from the list
            poem_ids = []
            for section in book_metadata.get('sections', []):
                if 'poems' in section:
                    for poem in section['poems']:
                        if 'id' in poem:
                            poem_ids.append(poem['id'])
            
            # Fetch each poem
            fetched_poems = []
            for poem_id in tqdm(poem_ids, desc=f"Fetching poems for book {id}"):
                poem_url = f"{base_url}/poems/{id}/{poem_id}.yaml"
                output_path = poems_path / f"{poem_id}.yaml"
                
                # Skip if already downloaded
                if output_path.exists():
                    logger.debug(f"Poem {poem_id} already exists, skipping download")
                    fetched_poems.append(poem_id)
                    continue
                
                try:
                    response = requests.get(poem_url, timeout=10)
                    
                    if response.status_code == 200:
                        with open(output_path, "w", encoding="utf-8") as f:
                            f.write(response.text)
                        
                        fetched_poems.append(poem_id)
                        print(f"Successfully fetched poem {poem_id}")
                    else:
                        print(f"Failed to fetch poem {poem_id}: {response.status_code}")
                    
                    # Respect rate limits
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"Error fetching poem {poem_id}: {str(e)}")

            logger.info(f"Fetched {len(fetched_poems)} poems for book {id}")
        return fetched_poems

