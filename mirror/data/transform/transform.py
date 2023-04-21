import argparse

from langchain import PromptTemplate
from langchain.llms import OpenAI

def statements(data):
    """
        Transforms the data into a series of single-sentence facts about the data.

        Args:
            data (str): Data to be transformed.

        Returns:
            str: Transformed data.
    """
    print("Transforming data into a series of single-sentence facts about the data.")
    # Use LLM to turn the resume into a series of single-sentence facts about the resume
    template = """
    The purpose of this model is to take a string describing something about a person, for example their resume, as Input
    and turn it into as many single-sentence facts about that person as possible.

    Output Examples:
    Studied Computer Science at the University of Washington.
    Started his PhD at the University of Texas at Austin, but dropped out after one year.
    Did two undergrad internships at Amazon Lab 126.

    Input: {data}
    Output:
    """
    prompt = PromptTemplate(
        input_variables=["data"],
        template=template,
    )
    formatted_prompt = prompt.format(data=data)

    llm = OpenAI()
    llm_facts = llm(formatted_prompt)
    print(f"Transformed into Facts: {llm_facts}")
    return llm_facts

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', type=str)
    parser.add_argument('-o', '--output-file', type=str)
    parser.add_argument('-t', '--transformation', choices=['statements'], default="statements", help='Transformation type to apply to input data')
    args = parser.parse_args()

    # Load text file
    with open(args.input_file, 'r') as f:
        data = f.read()

    transformation_map = {
        "statements": statements,
    }

    transformed_data = transformation_map[args.transformation](data)

    if args.output_file:
        print(f"Writing transformed data to file: {args.output_file}")
        with open(args.output_file, 'w') as f:
            f.write(transformed_data)
