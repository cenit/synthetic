# Synthetic dataset creation with GPT-4

## Procedure for generating a dataset of 200,000 problems solved with structured text using GPT-4

### Step 1: Define Problem Categories and Subcategories

- **Objective:** Create a diverse set of problem categories (e.g., math, algorithms, data structures, string manipulation, etc.).
- **Action:** Use GPT-4 to generate a list of categories and subcategories. For example:
  - **Math Problems:** Arithmetic, Algebra, Calculus
  - **Algorithms:** Sorting, Searching, Dynamic Programming
  - **Data Structures:** Arrays, Linked Lists, Trees

### Step 2: Generate Problem Statements

- **Objective:** Generate unique problem statements for each category.
- **Action:**
  - Feed GPT-4 with the category and subcategory names and ask it to generate multiple problem statements for each.
  - For instance, ask GPT-4 to generate 500 unique problems for each subcategory, which will give you a diverse set of problems across all categories.

### Step 3: Generate Structured Solutions in Pseudocode

- **Objective:** For each problem statement, create a structured solution in pseudocode or structured text.
- **Action:**
  - Use GPT-4 to write the pseudocode for the problems generated. You can instruct it to use structured text formats, such as:

    ```markdown
    Step 1: Initialize variables
    Step 2: Loop through the array
    Step 3: Apply condition
    Step 4: Return the result
    ```

  - Iterate this process until you generate solutions for all 200,000 problems.

### Step 4: Validate and Refine Solutions

- **Objective:** Ensure the solutions are accurate and well-structured.
- **Action:**
  - Use GPT-4 to validate the pseudocode by rephrasing it into actual code snippets in a programming language (e.g., Python).
  - Run a validation script on a subset of these problems to ensure the correctness of the logic.
  - Refine any solutions that do not meet the required standards.

### Step 5: Add Variation and Complexity

- **Objective:** Introduce variation in difficulty and complexity across the dataset.
- **Action:**
  - Modify a portion of the problem statements and solutions to introduce different levels of difficulty.
  - Ask GPT-4 to add variations such as edge cases, performance optimizations, or alternative approaches.

### Step 6: Format and Structure the Dataset

- **Objective:** Format the dataset in a consistent manner suitable for training or other applications.
- **Action:**
  - Create a CSV or JSON structure where each entry contains the problem statement, category, subcategory, and structured solution.
  - Ensure that each problem has metadata like difficulty level, problem type, and any tags for specific concepts.

### Step 7: Review and Quality Assurance

- **Objective:** Ensure the final dataset meets your quality standards.
- **Action:**
  - Perform a quality check on random samples across all categories.
  - Use GPT-4 to cross-check and improve consistency in structured text formatting.

### Step 8: Scale and Automate

- **Objective:** Scale the process to generate the full 200,000 dataset.
- **Action:**
  - Automate the generation, validation, and formatting processes using scripts that call GPT-4 for different stages.
  - Parallelize the task across multiple instances of GPT-4 to expedite the generation process.

### Step 9: Post-Processing and Final Checks

- **Objective:** Finalize the dataset and prepare it for use.
- **Action:**
  - Perform any necessary final cleaning, deduplication, and formatting.
  - Export the dataset into the desired format and ensure it's well-documented.

### Step 10: Dataset Documentation

- **Objective:** Create comprehensive documentation for the dataset.
- **Action:**
  - Document the process, dataset structure, and any specific details about problem categories, complexity levels, and structured text formats.
  - Include guidelines on how to use the dataset effectively.
