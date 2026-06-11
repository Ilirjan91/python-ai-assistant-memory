# Python AI Assistant with Memory

This is a simple AI assistant built with Python.
The assistant can use either a local model with Ollama or a cloud model with the Groq API.

It supports multiple languages and stores the chat history locally in a JSON file.

## Features

* Choose between a local AI model and a cloud AI model
* Supports multiple languages such as German, English, Albanian, Italian, Spanish and French
* Saves the chat history locally in `memory.json`
* Uses `.env` for API keys
* Simple chat commands
* Error handling for API requests
* System prompt for controlling the assistant behavior

## Chat Commands

```text
/help      Show available commands
/reset     Clear chat history
/history   Show recent chat history
/model     Show the current model
/exit      Exit the program
```

## Technologies

* Python
* OpenAI-compatible API
* Groq API
* Ollama
* JSON
* python-dotenv

## Installation

Clone the repository:

```bash
git clone https://github.com/dein-username/dein-repository.git
cd dein-repository
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project folder:

```env
GROQ_API_KEY=your_api_key_here
```

Important:
The `.env` file is not uploaded to GitHub because it contains private API keys.

An example file `.env.example` is included in the project.

## Start the Program

Run the program with:

```bash
python main.py
```

After starting the program, you can choose between:

```text
1. LLaMA 3.2 local with Ollama
2. LLaMA 3.3 cloud with Groq API
```

## Local Usage with Ollama

To use the local model, Ollama must be installed and running.

Start the model with:

```bash
ollama run llama3.2
```

Then choose option `1` in the program.

## Project Structure

```text
project/
│
├── main.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
└── memory.json
```

Note:
`memory.json` is created locally and is not uploaded to GitHub.

## Security

The following files are ignored by Git:

```text
.env
memory.json
__pycache__/
*.pyc
```

This keeps API keys and private chat history safe.

## What I Learned

In this project, I learned:

* how to work with AI APIs
* how to use environment variables with `.env`
* how to save data with JSON
* how to create simple chat commands
* how to handle errors in Python
* how to prepare a Python project for GitHub

## Future Improvements

Planned improvements:

* Add a memory command to save user facts
* Add a `/memory` command
* Add a `/forget` command
* Split the code into multiple Python files
* Add tests with pytest

## Status

This is a learning project and will be improved step by step.
