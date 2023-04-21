import argparse
import os

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

def load_chromalocal(data, persist_directory="data/local/loaded"):
    """Loads the data into the Chroma local data store.

    Args:
        data (str): Data to be loaded.

    Returns:
        Chroma: Chroma data store.
    """
    print(f"Loading data into Chroma local data store: {persist_directory}")
    embedding = OpenAIEmbeddings()
    return Chroma.from_texts(texts=data, embedding=embedding, persist_directory=persist_directory)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", type=str, help="Path to the input file")
    parser.add_argument('-d', '--data-store', choices=['chromalocal'], help='Name of the data store to use as the destination')
    parser.add_argument('-p', '--path', type=str, help='Path to the location in the data store')
    args = parser.parse_args()

    # Load input file
    print(f"Loading input file: {args.input_file}")
    with open(args.input_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        print(f"Loaded {len(lines)} lines")
        print(f"First line: {lines[0]}")

    # Check output path
    if args.path:
        data_dir = args.path
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '..', 'local', 'loaded')

    # Load into target data store
    data_store_map = {
        "chromalocal": load_chromalocal,
    }

    data_store_map[args.data_store](lines, data_dir)
