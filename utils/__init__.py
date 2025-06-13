# Internal imports
from .dataset_curator import DatasetCurator
from .dataset_downloader import DatasetDownloader


# Download the dataset from github
# downloader = DatasetDownloader(output_dir="data")
# downloader.download_from_github(source_name="github_iqbal_demystified")

# Process the dataset into a single file
# curator = DatasetCurator(data_path="data", output_dir="data/processed_data")
# dataset = curator.process_dataset(source="github_iqbal_demystified")
# print(f"Dataset processing complete. Stats:")
# print(f"- Books: {dataset['metadata']['total_books']}")
# print(f"- Poems: {dataset['metadata']['total_poems']}")