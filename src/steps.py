import openai
import json
import random
import csv
from tqdm import tqdm
import os

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

# Configuration parameters
categories = {
    "Math": ["Arithmetic", "Algebra", "Calculus"],
    "Algorithms": ["Sorting", "Searching", "Dynamic Programming"],
    "Data Structures": ["Arrays", "Linked Lists", "Trees"],
    "String Manipulation": ["Pattern Matching", "Parsing", "Encoding"]
}

# Number of problems per subcategory
num_problems_per_subcategory = 1000

# Function to generate problem statements
def generate_problem_statements(category, subcategory, num_problems):
    problem_statements = []
    for _ in range(num_problems):
        prompt = f"Generate a unique problem statement for {subcategory} in the {category} category."
        response = openai.Completion.create(
            engine=openai_model,
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7,
        )
        problem_statement = response.choices[0].text.strip()
        problem_statements.append(problem_statement)
    return problem_statements

# Function to generate structured pseudocode
def generate_pseudocode(problem_statement):
    prompt = f"Write a structured solution in pseudocode for the following problem: {problem_statement}"
    response = openai.Completion.create(
        engine=openai_model,
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )
    pseudocode = response.choices[0].text.strip()
    return pseudocode

# Function to validate and refine solutions
def validate_solution(pseudocode):
    prompt = f"Convert the following pseudocode into a Python code and check its correctness: {pseudocode}"
    response = openai.Completion.create(
        engine=openai_model,
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    python_code = response.choices[0].text.strip()
    return python_code

# Function to generate the dataset
def generate_dataset(categories, num_problems_per_subcategory):
    dataset = []
    for category, subcategories in categories.items():
        for subcategory in subcategories:
            print(f"Generating problems for {subcategory} in {category}...")
            problem_statements = generate_problem_statements(category, subcategory, num_problems_per_subcategory)
            for problem_statement in tqdm(problem_statements):
                pseudocode = generate_pseudocode(problem_statement)
                python_code = validate_solution(pseudocode)
                dataset.append({
                    "category": category,
                    "subcategory": subcategory,
                    "problem_statement": problem_statement,
                    "pseudocode": pseudocode,
                    "python_code": python_code
                })
    return dataset

# Function to save the dataset to a JSON file
def save_dataset_to_json(dataset, filename):
    with open(filename, 'w') as f:
        json.dump(dataset, f, indent=4)

# Function to save the dataset to a CSV file
def save_dataset_to_csv(dataset, filename):
    keys = dataset[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(dataset)

# Main execution
if __name__ == "__main__":
    dataset = generate_dataset(categories, num_problems_per_subcategory)
    save_dataset_to_json(dataset, "synthetic_dataset.json")
    save_dataset_to_csv(dataset, "synthetic_dataset.csv")
    print("Dataset generation complete!")
