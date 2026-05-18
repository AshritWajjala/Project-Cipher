# Project Cipher - AI-powered Linux Command Interface

## Overview

Project Cipher is a Python-based application that leverages a Large Language Model (LLM) to interpret natural language user requests and translate them into executable Linux commands. This project demonstrates
proficiency in Natural Language Processing (NLP), LLM prompting, and secure system interaction.

## Features

*   **Natural Language Interface:** Allows users to interact with the Linux command line using plain English.
*   **Intent Recognition:** Employs an LLM to identify the user's intended action (e.g., list files, create directories, search for text).
*   **Entity Extraction:** Extracts relevant parameters from user input to construct accurate commands.
*   **Secure Command Execution:** Implements security measures to prevent unauthorized commands and protect the system.
*   **Modular Design:**  Designed for maintainability and extensibility.

## Technologies Used

*   Python 3.12
*   

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AshritWajjala/Project-Cipher.git
    cd ProjectCipher
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure API Keys:**
    *   Create a `.env` file in the root directory.
    *   Add your LLM API key to the `.env` file in the following format:
        ```
        LLM_API_KEY=[Your API Key]
        ```
5.  **Ensure Python is installed:**
    *   Verify that Python 3.x is installed on your system.

## Usage

1.  **Run the application:**
    ```bash
    python main.py
    ```
2.  **Interact with the command interface:**
    *   Enter natural language commands at the prompt.
    *   The application will attempt to translate your request into a Linux command and execute it.

## Security Considerations

This project includes security measures to prevent malicious command execution. However, it's crucial to understand the risks associated with executing commands based on user input. Always exercise caution and review
commands before execution, especially in a production environment.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## Contact

ashritw2000@gmail.com
