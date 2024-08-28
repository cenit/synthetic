import os
import json
import time
import sys
from tqdm import tqdm

use_azure = True

if use_azure:
    from openai import AzureOpenAI, RateLimitError
    openai_model = os.getenv("AZURE_OPENAI_DEPLOYMENT_MODEL")
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01"
    )
else:
    from openai import OpenAI, RateLimitError
    openai_model = "gpt-4o"
    client = OpenAI()

def read_questions(file_path):
    """Read questions from a file and return them as a list."""
    with open(file_path, 'r') as file:
        questions = file.readlines()
    return [q.strip() for q in questions]


def process_question(question, max_retries=5, initial_delay=60):
    retries = 0
    delay = initial_delay
    while retries < max_retries:
        try:
            response = client.chat.completions.create(
                model=openai_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant, writing programs in structured text (ST, standard IEC 61131-3). You are given requests to write programs in structured text that solve the question. Structured text (ST) is used in PLC programming and so the algorithms should represent typical patterns used in automation and not what is more usual in computer science. For example, you really have to focus on using case structures (state machines) with as many states as necessary, considering of course also transitional states and not just those persisting (for example, from stop to run, you have to considering a state in which the machine is entering the running status for transient operations). Do these states also when they do not look as necessary, because they are necessary to better structure the code for future machine requirements. The request is to have top-level quality code, with a lot of comments at the beginning of each function, of each state and anticipating variable description and with a doxygen-like formatting so that we can parse the code and extract documentation. Do not write explanations, introductions or any description of your actions. Just give the code. Your output will be passed directly to a compiler so avoid anything that might break building. Be also realistic and make the code look authentic and not too much synthetic. The first line of your output shall be a comment with the expected file name, the second line should be another comment with the question given to you. In case you need to do multiple file, terminate the file with a new line with (* ========== *) and then start the new file again with a comment line with the expected file name. Do not encapsulate output into a markdown code block, just wrote the pure code directly as the compiler expects it."},
                    {"role": "user", "content": question}
                ]
            )
            return response.choices[0].message.content

        except RateLimitError as e:
            if retries < max_retries:
                print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
                retries += 1
                delay *= 2  # Exponential backoff
            else:
                print("Maximum retries reached. Exiting.")
                raise e


def process_questions(question_file_path, output_folder):
    questions = read_questions(question_file_path)
    with tqdm(total=len(questions), desc="Creating dataset") as pbar:
        for index, question in enumerate(questions, start=1):
            answer = process_question(question)
            answer_and_question = {
                "question": question,
                "answer": answer
            }
            output_path_json = os.path.join(output_folder, f"answer_{index}.json")
            json.dump(answer_and_question, open(output_path_json, "w"), indent=4)
            output_path_st = os.path.join(output_folder, f"answer_{index}.st")
            with open(output_path_st, 'w') as file:
                file.write(answer)
            pbar.update(1)


questions_file_path = sys.argv[1]
output_file_folder = sys.argv[2]
if not os.path.exists(output_file_folder):
    os.makedirs(output_file_folder)
process_questions(questions_file_path, output_file_folder)
