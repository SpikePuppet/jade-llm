import bz2
import shutil
from pathlib import Path

BZ2_FILE_SUFFIX = ".bz2"

# If this one isn't here you have a problem
corpus_directory = "wikidownloads/"
unpack_directory = "wikidownloads_unpacked/"
corpus_directory_path = Path(corpus_directory)
unpack_directory_path = Path(unpack_directory)
unpack_directory_path.mkdir(parents=True, exist_ok=True)

for file in corpus_directory_path.iterdir():
    extracted_file_path = Path(unpack_directory + file.stem)
    if file.is_file() and file.suffix == BZ2_FILE_SUFFIX:
        print("extracting " + file.name)
        with bz2.open(file, "rb") as f_in:
            with open(unpack_directory + file.stem, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        print("extracted!")
