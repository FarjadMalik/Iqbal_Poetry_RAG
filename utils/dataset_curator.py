# Standard library imports
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

# Third-party imports
import yaml
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("dataset_curation.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("DatasetCurator")


class DatasetCurator:
    """
    A robust dataset curator for processing Allama Iqbal's poetry collection
    with nested YAML structures into a flattened JSON format optimized for RAG.
    
    Features:
    - Hierarchical data flattening
    - Multilingual support (with English focus)
    - Nested structure resolution
    - Metadata preservation
    - Data validation and error handling
    """
    
    def __init__(self, data_path: str, output_dir: str):
        """
        Initialize the curator with validated paths
        
        Args:
            data_root (str): Root directory containing 'lists' and 'poems' folders
            output_dir (str): Directory for saving processed datasets
        """
        self.data_root = Path(data_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.dataset = {
            "metadata": {
                "total_books": 0,
                "total_poems": 0
            },
            "books": [],
            "poems": []
        }


    def process_dataset(self, source: str = 'github_iqbal_demystified'):
        """
        Process the dataset based on the source.
        """
        if source == 'github_iqbal_demystified':
            self.data_root = self.data_root / source
            self.dataset = self.process_github_iqbal_demystified()
            logger.info(f"Dataset processed successfully")
            # logger.debug(f"Dataset: {self.dataset}")
        else:
            raise ValueError(f"Unsupported source: {self.source}")
        
        # Save the dataset to various formats
        self._save_dataset()
        
        return self.dataset
    
    
    def process_github_iqbal_demystified(self):
        """
        Main processing pipeline with error handling and progress tracking
        """
        try:
            book_files = sorted((self.data_root / "lists").glob("List_*.yaml"))
            logger.info(f"Found {len(book_files)} book files to process")
            
            for book_file in tqdm(book_files, desc="Processing books"):
                book_data = self._load_yaml(book_file)
                book_id = book_file.stem.split("_")[-1]
                processed_book = self._process_book(book_id, book_data)
                self.dataset["books"].append(processed_book)
                
                poems = self._process_poems(book_id, processed_book)
                self.dataset["poems"].extend(poems)          
                self.dataset["metadata"]["total_poems"] += len(poems)
            self.dataset["metadata"]["total_books"] = len(self.dataset["books"])  
            
            return self.dataset
            
        except Exception as e:
            logger.error(f"Processing failed: {str(e)}")
            return None

    def _process_book(self, book_id: str, raw_data: Dict) -> Dict:
        """
        Process book metadata with nested section structure
        
        Args:
            book_id (str): Unique identifier for the book
            raw_data (Dict): Raw YAML data from list file
            
        Returns:
            Dict: Processed book structure with flattened metadata
        """
        book_structure = {
            "id": book_id,
            "titles": {},
            "sections": [],
            "metadata": {"total_sections": 0, "total_poems": 0}
        }
        
        # Process multilingual titles
        for title_entry in raw_data.get("name", []):
            lang = title_entry.get("lang", "unknown")
            book_structure["titles"][lang] = title_entry.get("text", "")
            if lang == 'en':
                book_structure['primary_title'] = title_entry.get("text", "Unknown")
        
        # Process sections
        current_section = None
        for section_data in raw_data.get("sections", []):
            if "sectionName" in section_data:
                if current_section:
                    book_structure["sections"].append(current_section)
                    book_structure["metadata"]["total_sections"] += 1
                
                current_section = {
                    "id": len(book_structure["sections"]) + 1,
                    "titles": {},
                    "poems": [],
                    "poem_ids": [],
                    "metadata": {"total_poems": 0}
                }
                
                for name_entry in section_data["sectionName"]:
                    lang = name_entry.get("lang", "unknown")
                    current_section["titles"][lang] = name_entry.get("text", "")
            
            if "poems" in section_data and current_section:
                poems = self._process_poem_metadata(section_data["poems"])
                poem_ids = [poem['id'] for poem in poems]
                current_section["poems"].extend(poems)
                current_section["poem_ids"].extend(poem_ids)
                current_section["metadata"]["total_poems"] += len(poems)
        
        if current_section:
            book_structure["sections"].append(current_section)
            book_structure["metadata"]["total_sections"] += 1
        
        book_structure["metadata"]["total_poems"] = sum(
            len(s["poems"]) for s in book_structure["sections"]
        )
        return book_structure
    

    def _process_poem_metadata(self, poems: List[Dict]) -> List[Dict]:
        """
        Flatten poem metadata from nested structure
        
        Args:
            poems (List[Dict]): Raw poem metadata entries
            
        Returns:
            List[Dict]: Processed poem metadata
        """
        processed = []
        for poem in poems:
            processed_poem = {
                "id": poem.get("id", ""),
                "titles": {},
                "metadata": {"languages": []}  # Changed from set to list
            }
            
            for title_entry in poem.get("poemName", []):
                lang = title_entry.get("lang", "unknown")
                processed_poem["titles"][lang] = title_entry.get("text", "")
                if lang not in processed_poem["metadata"]["languages"]:
                    processed_poem["metadata"]["languages"].append(lang)
            
            processed.append(processed_poem)
        return processed
    

    def _process_poems(self, book_id: str, book_data: Dict) -> List[Dict]:
        """
        Process poem content files with validation and error handling
        
        Args:
            book_id (str): Parent book identifier
            book_data (Dict): Processed book structure
            
        Returns:
            List[Dict]: Processed poems with flattened content
        """
        poems = []
        book_name = book_data.get("primary_title", f"book_{book_id}")
        sections = book_data.get("sections", [])
        poem_dir = self.data_root / "poems" / book_id
        
        if not poem_dir.exists():
            logger.warning(f"Missing poem directory for book: {book_id}:{book_name}")
            return []
            
        for poem_file in poem_dir.glob("*.yaml"):
            try:
                poem_id = poem_file.stem
                raw_data = self._load_yaml(poem_file)
                
                # Create the generator expression, broken for readability
                sectioninfo_generator = (
                    (section_info.get('id'), section_info.get('titles', {}).get('en'))
                    for section_info in sections
                    if poem_id in section_info.get('poem_ids', [])
                )
                # Use next() with the generator and a default tuple
                section_id, section_name = next(sectioninfo_generator, (None, None))
                # Create poem structure
                poem = {
                    "id": poem_id,
                    "book_id": book_id,
                    "book_title": book_name,
                    "section_id": section_id,
                    "section_title": section_name,
                    "metadata": {"languages": []},
                    "content": {"descriptions": {}, "verses": []}
                }
                
                # Process descriptions
                for desc_entry in raw_data.get("description", []):
                    lang = desc_entry.get("lang", "unknown")
                    poem["content"]["descriptions"][lang] = desc_entry.get("text", "")
                    if lang not in poem["metadata"]["languages"]:
                        poem["metadata"]["languages"].append(lang)
                
                # Process verses with language detection
                for verse in raw_data.get("sher", []):
                    processed_verse = self._process_verse(verse)
                    poem["content"]["verses"].append(processed_verse)
                    # Detect verse languages
                    for content in verse.get("sherContent", []):
                        lang = content.get("lang", "unknown")
                        if lang not in poem["metadata"]["languages"]:
                            poem["metadata"]["languages"].append(lang)
                
                # Flatten structure with complete English detection
                rag_poem = self._flatten_for_rag(poem)
                if rag_poem:  # Only add if English content exists
                    poems.append(rag_poem)
            except Exception as e:
                logger.error(f"Failed processing poem {poem_id}: {str(e)}")
        
        return poems

    def _process_verse(self, verse: Dict) -> Dict:
        """
        Process individual verse with multilingual content
        
        Args:
            verse (Dict): Raw verse data from YAML
            
        Returns:
            Dict: Processed verse structure
        """
        processed = {
            "id": verse.get("id", ""),
            "content": {},
            "notes": []
        }
        
        for content_entry in verse.get("sherContent", []):
            lang = content_entry.get("lang", "unknown")
            processed["content"][lang] = {
                "text": content_entry.get("text", ""),
                "notes": [self._process_note(n) for n in content_entry.get("notes", [])]
            }
        
        return processed
    

    def _process_note(self, note: Dict) -> Dict:
        """
        Standardize phrase/note structure
        
        Args:
            note (Dict): Raw note data
            
        Returns:
            Dict: Processed note structure
        """
        return {
            "phrase": note.get("phrase", ""),
            "meaning": note.get("meaning", ""),
            "occurrences": note.get("occurrence", 1)
        }
    

    def _flatten_for_rag(self, poem: Dict) -> Dict:
        """
        Transform poem structure into RAG-optimized format
        
        Args:
            poem (Dict): Original poem structure
            
        Returns:
            Dict: Flattened structure with combined text fields
        """
        rag_poem = {
            "poem_id": poem["id"],
            "book_id": poem["book_id"],
            "book_title": poem["book_title"],
            "section_id": poem["section_id"],
            "section_title": poem["section_title"],
            "text_blocks": [],
            "full_text": ""
        }

        # Extract English content from all sources
        en_content = {
            "descriptions": poem["content"]["descriptions"].get("en", ""),
            "verses": [],
            "phrases": []
        }

        # Process verses
        for verse in poem["content"]["verses"]:
            if "en" in verse["content"]:
                en_content["verses"].append(verse["content"]["en"]["text"])
                en_content["phrases"].extend(
                    f"{note['phrase']}: {note['meaning']}"
                    for note in verse["content"]["en"].get("notes", [])
                )

        # Build full text if English content exists
        if en_content["verses"]:
            rag_poem["full_text"] = "\n\n".join([
                en_content["descriptions"],
                "\n".join(en_content["verses"])
            ])
            rag_poem["text_blocks"] = en_content["verses"]
            rag_poem["phrases"] = en_content["phrases"]
            return rag_poem
        
        logger.warning(f"No English content found for poem {poem['id']}")
        return None
    

    def _save_dataset(self):
        """Save datasets with proper serialization checks"""
        base_path = self.output_dir / "iqbal_poems"
        
        # Save full dataset
        with open(f"{base_path}_full.json", "w", encoding="utf-8") as f:
            json.dump(self.dataset, f, ensure_ascii=True, indent=2)
        
        # Save RAG-optimized poems (only those with English content)
        rag_data = [p for p in self.dataset["poems"] if p is not None]
        
        with open(f"{base_path}_rag.json", "w", encoding="utf-8") as f:
            json.dump(rag_data, f, ensure_ascii=True, indent=2)
        
        logger.info(f"Saved {len(rag_data)} RAG-ready poems")

    def _load_yaml(self, path: Path) -> Dict:
        """
        Safe YAML loader with validation
        
        Args:
            path (Path): Path to YAML file
            
        Returns:
            Dict: Parsed YAML content
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed loading YAML from {path}: {str(e)}")
            raise
