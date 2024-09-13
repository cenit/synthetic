import comtypes.client
import hashlib
import logging
import argparse
import random
import os
import time
import sys
import clr

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

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Generate synthetic ST code dataset")
    parser.add_argument('--log', action='store_true',
                        help='Enable logging to disk')
    args = parser.parse_args()

    # Set up logging
    if args.log:
        logging.basicConfig(
            filename='st_code_generation.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    else:
        # Suppress logging if not enabled
        logging.basicConfig(level=logging.CRITICAL)


    # Define categories and subcategories
    categories = {
        "Motion Control": [
            "Linear Motion Control",
            "Rotary Motion Control",
            "Positioning Systems",
            "Speed Regulation",
            "Acceleration and Deceleration Profiles",
            "Synchronized Multi-Axis Motion",
            "Cam Profile Generation",
            "Electronic Gearing and Coupling",
            "Interpolation Methods (Linear, Circular)",
            "Homing and Reference Procedures",
            "Torque Control Applications",
            "Path Planning Algorithms",
            "Motion Queuing and Buffering",
            "Jogging Functions",
            "Limit Switch Handling",
            "Emergency Stop in Motion Systems",
            "Vibration and Resonance Control",
            "Load Compensation Techniques",
            "Motion Error Detection and Correction",
            "Motion Diagnostics and Monitoring"
        ],
        "Process Control": [
            "PID Control Loops",
            "Temperature Regulation",
            "Pressure Control Systems",
            "Flow Rate Control",
            "Level Measurement and Control",
            "Cascade Control Strategies",
            "Ratio Control Systems",
            "Feedforward Control Methods",
            "pH Balancing Control",
            "Humidity Control Systems",
            "Density Measurement Control",
            "Batch Processing Automation",
            "Multi-Loop Control Systems",
            "Adaptive Control Algorithms",
            "Model Predictive Control",
            "Valve Actuation and Control",
            "Sensor Calibration Routines",
            "Alarm Handling in Processes",
            "Safety Interlocks in Process Control",
            "Process Optimization Techniques"
        ],
        "Safety Systems": [
            "Emergency Stop Implementation",
            "Safety Interlock Systems",
            "Guard Monitoring Mechanisms",
            "Safety PLC Programming",
            "Safe Torque Off (STO) Functions",
            "Safety Relay Logic",
            "Light Curtain Integration",
            "Safety Mat Detection",
            "Two-Hand Control Systems",
            "Safety Zone Management",
            "Safety Diagnostics and Testing",
            "Redundancy in Safety Systems",
            "Fail-Safe Communication Protocols",
            "Safe Speed Monitoring",
            "Safety Validation Procedures",
            "Safety Function Blocks Usage",
            "Safety over Fieldbus Protocols",
            "Safety Data Logging and Analysis",
            "Lockout/Tagout Procedures",
            "Compliance with Safety Standards"
        ],
        "Communication Protocols": [
            "Modbus RTU/TCP Communication",
            "Profibus Integration",
            "Profinet Communication",
            "Ethernet/IP Protocols",
            "DeviceNet Communication",
            "CANopen Networking",
            "OPC UA Client/Server Setup",
            "MQTT Publish/Subscribe Models",
            "Serial Communication (RS232/RS485)",
            "EtherCAT Protocol Implementation",
            "AS-Interface Networking",
            "BACnet for Building Automation",
            "Interbus Communication",
            "IO-Link Device Integration",
            "DNP3 Protocol for Utilities",
            "HART Protocol Communication",
            "CC-Link Integration",
            "Foundation Fieldbus Communication",
            "Sercos Interface for Motion Control",
            "Wireless Communication (Wi-Fi, Bluetooth)"
        ],
        "Human-Machine Interface (HMI)": [
            "Dynamic Display Updates",
            "User Input Handling and Validation",
            "Alarm Display and Acknowledgment",
            "Trend Graph Implementation",
            "Recipe Management Systems",
            "Multi-Language Support",
            "Security and Login Mechanisms",
            "Screen Navigation Logic",
            "Touchscreen Gesture Recognition",
            "Data Entry and Editing",
            "Dynamic Graphics and Animations",
            "Event Logging and History",
            "Remote HMI Access Setup",
            "Operator Guidance Messages",
            "Notifications and Alert Systems",
            "Custom Widget Development",
            "HMI Scripting and Macros",
            "Animation Control Techniques",
            "HMI Configuration via PLC Code",
            "HMI-PLC Communication Protocols"
        ],
        "Data Handling and Management": [
            "Data Logging and Archiving",
            "Recipe Data Storage",
            "Data Conversion Techniques",
            "Data Serialization and Deserialization",
            "File Operations (Read/Write/Delete)",
            "Database Connectivity (SQL Integration)",
            "Buffer Management Systems",
            "Data Compression Algorithms",
            "Historical Data Retrieval Methods",
            "Data Integrity and Checksums",
            "Time-Stamping Data Entries",
            "Data Encryption and Security",
            "Data Synchronization Across Devices",
            "Cloud Data Storage Solutions",
            "Real-Time Data Analysis",
            "Data Filtering and Sorting",
            "Data Aggregation Techniques",
            "Backup and Recovery Procedures",
            "Data Import/Export Utilities",
            "Data Validation and Verification"
        ],
        "Diagnostics and Maintenance": [
            "Error Handling Mechanisms",
            "Alarm Management Systems",
            "Self-Test and Diagnostic Routines",
            "Predictive Maintenance Algorithms",
            "Fault Detection and Isolation",
            "System Health Monitoring",
            "Logging and Traceability",
            "Watchdog Timer Implementation",
            "Remote Diagnostics Tools",
            "Diagnostic LED Control",
            "System Reset and Recovery Procedures",
            "Calibration and Adjustment Routines",
            "Maintenance Scheduling and Alerts",
            "Firmware Update Processes",
            "Diagnostic Communication Protocols",
            "Memory Usage Monitoring",
            "Network Diagnostics and Testing",
            "Performance Benchmarking Tools",
            "Diagnostic Dashboards and Visualization",
            "Event-Triggered Diagnostic Actions"
        ],
        "Power Management": [
            "Load Shedding Strategies",
            "Battery Backup Management",
            "Power Factor Correction Techniques",
            "Energy Consumption Monitoring",
            "Uninterruptible Power Supply (UPS) Control",
            "Voltage Regulation Systems",
            "Generator Control and Synchronization",
            "Renewable Energy Integration",
            "Power Quality Monitoring",
            "Overcurrent and Overvoltage Protection",
            "Soft Starter Control for Motors",
            "Inverter Control Systems",
            "Power Failure Detection and Recovery",
            "Demand Response Programs",
            "Harmonic Filtering Methods",
            "Motor Management Systems",
            "Scheduled Power Operations",
            "Transformer Monitoring and Control",
            "Smart Grid Interaction and Control",
            "Power Supply Redundancy and Switching"
        ],
        "Timing and Scheduling": [
            "Delay Functions and Timers",
            "On-Delay and Off-Delay Timers",
            "Scheduled Task Execution",
            "Real-Time Clock Utilization",
            "Time Synchronization Across Devices",
            "Event Scheduling and Timing",
            "Cycle Time Optimization Techniques",
            "Time-Based Control Loops",
            "Timeout Handling and Recovery",
            "Seasonal Adjustment Implementations",
            "Watchdog Timer Management",
            "Time-Stamped Data Logging",
            "Timer Interrupt Handling",
            "Calendar Function Integration",
            "Time Zone and Daylight Saving Adjustments",
            "Stopwatch Functionality",
            "Delayed Start and Stop Operations",
            "Periodic Maintenance Scheduling",
            "Time-Based Sequencing and Control",
            "Time-of-Day Dependent Logic"
        ],
        "Sequencing and State Machines": [
            "Batch Process Sequencing",
            "Sequential Function Chart (SFC) Implementation",
            "Event Handling Mechanisms",
            "Mode Management (Auto/Manual/Service)",
            "Recipe Execution Sequences",
            "Transition Condition Programming",
            "Nested State Machines",
            "Interrupt Handling in Sequences",
            "Production Line Sequencing Logic",
            "Fault Recovery Sequences",
            "Startup and Shutdown Procedures",
            "Mode Switching and Transitions",
            "Sequence Step Timing and Delays",
            "Conditional Sequencing Paths",
            "Step Skipping and Repetition",
            "Multi-Product Sequencing Strategies",
            "Safety Interlocks within Sequences",
            "Reversible Sequencing Operations",
            "Parallel Sequencing and Synchronization",
            "Sequence Monitoring and Visualization"
        ]
    }

    total_examples = 10000
    pairs = get_category_subcategory_pairs(categories)
    examples_per_pair = total_examples // len(pairs)
    remainder = total_examples % len(pairs)
    example_index = 1
    total_generated = 0
    generated_codes = set()

    # Main generation loop
    for idx, (category, subcategory) in enumerate(pairs):
        num_examples = examples_per_pair + (1 if idx < remainder else 0)
        for _ in range(num_examples):
            logging.info(
                f"Generating code example {example_index} for {category} - {subcategory}...")
            prompt = create_prompt(category, subcategory)
            code = generate_st_code(prompt)
            if code:
                compilation_successful = False
                attempts = 0
                max_attempts = 3  # Limit the number of fix attempts
                while not compilation_successful and attempts < max_attempts:
                    code = generate_st_code(prompt)
                    if code:
                        code_saved = save_code(
                            code, example_index, category, subcategory, generated_codes)
                        if code_saved:
                            compilation_successful, error_message = compile_code_with_twincat(
                                get_code_file_path(
                                    example_index, category, subcategory)
                            )
                            if compilation_successful:
                                logging.info(
                                    f"Code example {example_index} compiled successfully.")
                                example_index += 1
                                total_generated += 1
                            else:
                                logging.warning(
                                    f"Compilation failed for example {example_index}. Attempting to fix...")
                                # Send error back to GPT-4 to fix the code
                                fix_prompt = create_fix_prompt(code, error_message)
                                code = generate_st_code(fix_prompt)
                                attempts += 1
                        else:
                            logging.warning(
                                f"Duplicate code for example {example_index}. Generating a new one...")
                            code = generate_st_code(prompt)
                    else:
                        logging.error(
                            f"Failed to generate code example {example_index}. Retrying...")
                        time.sleep(5)  # Wait before retrying
                        continue
                    time.sleep(1)  # Respect rate limits
        logging.info(f"Total code examples generated: {total_generated}")


def get_category_subcategory_pairs(categories):
    pairs = []
    for category, subcategories in categories.items():
        for subcategory in subcategories:
            pairs.append((category, subcategory))
    return pairs


def create_prompt(category, subcategory):
    extra_instructions = [
        # ... (Your extra instructions here)
    ]
    instruction = random.choice(extra_instructions)
    prompt = f"""
You are an expert PLC programmer proficient in Structured Text (ST) according to the IEC 61131-3 standard.

- Generate a high-quality ST code example for **{category} - {subcategory}** that represents typical automation patterns used in PLC programming.
- {instruction}
- Use case structures (state machines) with as many states as necessary, including transitional and persistent states.
- Include detailed comments at the beginning of each function and state.
- Provide variable descriptions with doxygen-like formatting for documentation extraction.
- Ensure the code is well-structured for future machine requirements and expansion.

Please provide only the code, without additional explanations.
"""
    return prompt


def create_fix_prompt(code, error_message):
    fix_prompt = f"""
You are an expert PLC programmer proficient in Structured Text (ST) according to the IEC 61131-3 standard.

The following ST code has compilation errors:

```StructuredText
{code}
```

The compiler returned the following error messages:

```
{error_message}
```

Please fix the code so that it compiles successfully, while adhering to the original requirements, including:

- Use case structures (state machines) with as many states as necessary, including transitional and persistent states.
- Include detailed comments at the beginning of each function and state.
- Provide variable descriptions with doxygen-like formatting for documentation extraction.
- Ensure the code is well-structured for future machine requirements and expansion.

Please provide only the corrected code, without additional explanations.
"""
    return fix_prompt


def generate_st_code(prompt, max_retries=5, initial_delay=60):
    retries = 0
    delay = initial_delay
    while retries < max_retries:
        try:
            response = client.chat.completions.create(
                model=openai_model,
                messages=[
                    {"role": "system",
                        "content": "You are a helpful assistant that generates code."},
                    {"role": "user", "content": prompt}
                ],
                # Vary the temperature for diversity
                temperature=random.uniform(0.6, 0.9),
                max_tokens=1024,
                n=1,
                stop=None
            )
            code = response.choices[0].message.content
            return code
        except RateLimitError as e:
            if retries < max_retries:
                logging.warning(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
                retries += 1
                delay *= 2  # Exponential backoff
            else:
                logging.error(f"Maximum retries reached.")
                raise e


def save_code(code, index, category, subcategory, generated_codes):
    code_hash = hashlib.sha256(code.encode('utf-8')).hexdigest()
    if code_hash in generated_codes:
        logging.warning("Duplicate code detected.")
        return False  # Indicate that the code was not saved
    else:
        generated_codes.add(code_hash)
        directory = os.path.join("st_code_examples", category.replace(
            " ", "_"), subcategory.replace(" ", "_"))
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = os.path.join(directory, f"st_code_example_{index}.st")
        try:
            with open(filename, 'w') as file:
                file.write(code)
            return True
        except Exception as e:
            logging.error(f"Failed to save code example {index}: {e}")
            return False


def get_code_file_path(index, category, subcategory):
    directory = os.path.join("st_code_examples", category.replace(" ", "_"), subcategory.replace(" ", "_"))
    filename = os.path.join(directory, f"st_code_example_{index}.st")
    return filename


def compile_code_with_twincat(code_file_path):
    try:
        # Add references to TwinCAT XAE assemblies
        sys.path.append(r"C:\TwinCAT\3.1\Components\Base\TcXaeShell")
        clr.AddReference("EnvDTE")
        clr.AddReference("EnvDTE80")
        clr.AddReference("EnvDTE90")
        clr.AddReference("EnvDTE100")
        clr.AddReference("System")
        clr.AddReference("System.IO")
        clr.AddReference("System.Collections")
        clr.AddReference("System.Linq")

        # Start the TwinCAT XAE shell
        dte = comtypes.client.CreateObject(
            "TcXaeShell.DTE.15.0")  # Adjust version if necessary
        dte.UserControl = False

        # Open the TwinCAT project
        # Replace with your project path
        solution_path = r".\TemplateProject.sln"
        dte.Solution.Open(solution_path)

        # Wait for the solution to fully load
        while not dte.Solution.IsOpen:
            time.sleep(1)

        # Get the PLC project
        plc_project = None
        for project in dte.Solution.Projects:
            if project.Name == "PLC_Template":  # Replace with your PLC project name
                plc_project = project
                break

        if plc_project is None:
            logging.error("PLC project not found in the solution.")
            dte.Quit()
            return False, "PLC project not found."

        # Load the code from the file
        with open(code_file_path, 'r') as code_file:
            code_content = code_file.read()

        # Access the PLC project items
        plc_item = plc_project.ProjectItems.Item("POUs")  # Adjust if necessary

        # Add or replace the POU with the generated code
        pou_name = f"GeneratedPOU_{os.path.basename(code_file_path).split('.')[0]}"

        # Check if the POU already exists
        existing_pou = None
        for item in plc_item.ProjectItems:
            if item.Name == f"{pou_name}.TcPOU":
                existing_pou = item
                break

        if existing_pou:
            # Delete the existing POU
            existing_pou.Delete()

        # Add new POU
        pou_file_path = os.path.join(os.path.dirname(solution_path), f"PLC_Template\\POUs\\{pou_name}.TcPOU")
        with open(pou_file_path, 'w') as pou_file:
            pou_file.write(code_content)

        plc_item.ProjectItems.AddFromFile(pou_file_path)

        # Build the PLC project
        build_started = plc_project.DTE.Solution.SolutionBuild.BuildProject("Release", plc_project.UniqueName, True)

        # Wait for the build to complete
        while dte.Solution.SolutionBuild.BuildState == EnvDTE.vsBuildState.vsBuildStateInProgress:
            time.sleep(1)

        build_successful = dte.Solution.SolutionBuild.LastBuildInfo == 0

        if build_successful:
            # Compilation successful
            dte.Quit()
            return True, None
        else:
            # Compilation failed
            error_messages = ""
            for error_item in dte.ToolWindows.ErrorList.ErrorItems:
                error_messages += f"{error_item.Description}\n"
            dte.Quit()
            return False, error_messages.strip()

    except Exception as e:
        logging.error(f"An error occurred during compilation: {e}")
        return False, str(e)



if __name__ == "__main__":
    main()
