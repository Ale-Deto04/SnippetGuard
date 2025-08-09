# SnippetGuard

**SnippetGuard** is a CLI tool for Linux that combines AI and cybersecurity to detect vulnerabilities in Python code snippets. It uses a fine-tuned CodeBERT model to analyze code and perform an AI-driven security analysis.

---

## Overview

SnippetGuard accepts a file or a directory as input, identifies Python scripts, splits each file into smaller chunks (snippets), and feeds them into a CodeBERT-based model for vulnerability evaluation. The model returns a prediction for each snippet.

The model is trained to recognize the following vulnerabilities:

- SQL Injection (SQLi)
- Arbitrary Code Execution
- Path Traversal
- Command Injection
- Insecure Deserialization
- Buffer Overflow

The entire tool works offline and runs locally without any external dependencies.

---

## The Project

SnippetGuard is a personal project born from my interest for AI and cybersecurity. Designed as both an academic endeavor and a hands-on learning experience, it aims to train and utilize an AI model to effectively detect vulnerabilities in code. Simple yet powerful, SnippetGuard bridges cutting-edge technology with practical security challenges.

_**[Disclaimer]**: Do not rely on this tool for critical or production projects. This project is purely academic and intended for learning purposes only. It is not designed for serious or production-level code development. The model is trained on a limited dataset and may produce inaccurate results. Use it with caution._

---

## Dataset and Model

- The training dataset consists of about 1600 Python code snippets, partly AI-generated and partly adapted from a modified version of the `lemon42-ai/Code_Vulnerability_Labeled_Dataset` available on Hugging Face.
- The CodeBERT model has been fine-tuned with this dataset; training parameters and a final training report are included in the repository.
- Repository structure:
  - `bin/`: Python modules to run the tool
  - `model/`: pretrained model files and `labels.json`
  - `data/`: dataset used for training, training parameters (epochs, batch size, test size), and training report

---

## Requirements

- Python 3.8 or higher
- Dependencies listed in `requirements.txt`, installable via:

  ```bash
  pip install -r requirements.txt
  ```
---

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/Ale-Deto04/SnippetGuard
    cd SnippetGuard
    ```

2. Make sure the paths to the model and labels in `bin/config.py` are correct.

3. Make `bin/snippetguard` executable:

     ```bash
     chmod +x bin/snippetguard
     ```

4. Run the tool and check if it works:

      ```bash
      ./bin/snippetguard --help
      ```
      
5. _(Optional)_ Add ./bin/snippetguard to your `$PATH` environment variable to run the tool from anywhere:

     ```bash
     export PATH="$PATH:$(pwd)/bin"
     ```

---

## Features

The tool supports the following command-line options:

- `snippetguard -f <file>`: Specify a single input python script to analyze.  
- `snippetguard -d <directory>`: Specify a directory to analyze all contained python scripts.
- `snippetguard -o <output_file>`: Specify the output file where results will be saved.
- `snippetguard -s <label>`: Search for the specified vulnerability  
- `snippetguard -a`: Print detailed metrics for each vulnerability category after evaluation.  
- `snippetguard -g`: Show how the snippet is divided into chunks during parsing.  

---

## Technlogies Used
- Python
- CodeBERT (fine-tuned)
- Typer (for CLI)
- Rich (for enhance command-line interface)

---

## GPU support

The code can use GPU if available, but you need a compatible NVIDIA GPU and CUDA drivers installed. Otherwise, it will run on CPU.
To enable GPU:

1. Go on `bin/model.py` source code

2. Uncomment lines 15-16 and comment lines 19-20

      ```python
      14 # Use GPU if available
      15 device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
      16 model.to(device)

      18 # Default: use CPU
      19 # device = torch.device("cpu")
      20 # model.to(device)
      ```
If you don’t have a GPU or drivers, just leave it commented to run on CPU.

---

## Future Developments

Potential future improvements for SnippetGuard include optimizing the parsing and segmentation of code chunks to enhance accuracy and efficiency. Another important direction is to expand the model’s knowledge base, enabling it to analyze vulnerabilities in additional programming languages beyond Python.
A possible future development could be the integration of generative AI to suggest safe fixes for vulnerable code snippets; however, this would make the program slower and heavier, moving away from the original lightweight design of the project.

---

If you have any questions or want to contribute, feel free to open an issue or submit a pull request!
