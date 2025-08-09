# SnippetGuard

**SnippetGuard** is a CLI tool for Linux that combines AI and cybersecurity to detect vulnerabilities in Python code snippets. It uses a fine-tuned CodeBERT model to analyze code and help understand AI-driven security analysis.

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

SnippetGuard is a personal project created as a simple but effective tool to combine my interests in AI and cybersecurity. It is intended as a learning exercise to train and use an AI model for code vulnerability detection.

Do not rely on this tool for critical or production projects. The model is trained on a relatively small and simple dataset and may produce incorrect results.

---

## Dataset and Model

- The training dataset consists of about 1600 Python code snippets, partly AI-generated and partly adapted from a modified version of the lemon42-ai/Code_Vulnerability_Labeled_Dataset available on Hugging Face.
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
    git clone [<repository_url>](https://github.com/Ale-Deto04/SnippetGuard/edit/main/README.md)
    cd SnippetGuard
    ```

2. Make sure the paths to the model and labels in `bin/config.py` are correct.

3. Run the tool and check if it works:

      ```bash
      python bin/snippetguard --help
      ```

---

## Features

The tool supports the following command-line options:

- `-f <file>`: Specify a single input python script to analyze.  
- `-d <directory>`: Specify a directory to analyze all contained python scripts.
- `-o <output_file>`: Specify the output file where results will be saved.
- `-s <label>`: Search for the specified vulnerability  
- `-a`: Print detailed metrics for each vulnerability category after evaluation.  
- `-g`: Show how the snippet is divided into chunks during parsing.  

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
      # Use GPU if available
      device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
      model.to(device)

      # Default: use CPU
      # device = torch.device("cpu")
      # model.to(device)
      ```
If you don’t have a GPU or drivers, just leave it commented to run on CPU.

---

If you have any questions or want to contribute, feel free to open an issue or submit a pull request!
