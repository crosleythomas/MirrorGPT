import argparse
import os
import uuid
import urllib.request

from unstructured.partition.auto import partition

def pull_data(source_type, source):
    """Pulls the data from the given source.

    Args:
        source_type (str): Type of data source to pull from.
        source (str): Source to pull the data from, e.g. if the source type is 'url', this would be the URL to pull the data from.

    Returns:
        str: path to file containing the data.
    """
    print(f"Pulling data from {source_type} source: {source}")

    if source_type == "file":
        data_path = source
    elif source_type == "url":
        data_path = os.path.join("/tmp", str(uuid.uuid4()))
        urllib.request.urlretrieve(source, data_path)
    else:
        raise NotImplementedError(f"Pulling data from source type '{source_type}' is not implemented.")

    return data_path

def extract_text(input_path):
    """Extracts the text from the given data.

    Args:
        input_path (str): Path to the data to extract text from.

    Returns:
        str: Text extracted from the file.
    """
    print(f"Extracting text from file: {input_path}")
    return "\n".join([str(el) for el in partition(input_path)])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--source-type", type=str, choices=["file", "url"], help="Type of data source to pull from")
    parser.add_argument("-s", "--source", type=str, help=
                        "Source to pull the data from, e.g. if the source type is 'url', this would be the URL to pull the data from.")
    parser.add_argument("-o", "--output-file", type=str, help="Path to the output file")

    args = parser.parse_args()

    # Pull the requested data
    data_path = pull_data(args.source_type, args.source)

    # Extract the relevant data
    data = extract_text(data_path)

    # Write the extracted data to the output file
    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write(data)
    else:
        print("No output file specified, printing to stdout.")
        print(data)

    # Clean up any tmp files
    if os.path.exists(data_path) and data_path != args.output_file:
        os.remove(data_path)
    