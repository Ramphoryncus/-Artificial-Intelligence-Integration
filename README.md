# Artificial Intelligence Integration Mini-Project

## Overview

This project demonstrates a locally deployed generative AI system for game development.

A Python script communicates with a local Ollama model and generates a short game encounter from a location entered by the user. Each generated encounter contains:

- an enemy;
- a hazard;
- a reward;
- a short encounter description.

The program also records telemetry including the model name, response time, model loading time, prompt token count, generated token count, generation speed, platform information, and the generated response.

All generation runs locally on the user's computer. No cloud AI service or API key is required.

## Technologies Used

- Python 3
- Ollama
- `llama3.2:1b`
- Ollama local HTTP API
- Python `requests` package
- JSON telemetry files
- Git and GitHub

## Project Structure

```text
-Artificial-Intelligence-Integration/
├── encounter_generator.py
├── README.md
├── COMMENTARY.md
├── telemetry/
└── Media/
```

The `telemetry` folder is created automatically when the program successfully generates its first encounter.

## Requirements

Before running the program, install:

1. Python 3
2. Ollama
3. The Python `requests` package
4. The `llama3.2:1b` Ollama model

## Installation

### 1. Clone the repository

Open PowerShell, Git Bash, or another terminal and run:

```bash
git clone <REPOSITORY-URL>
```

Move into the cloned repository:

```bash
cd -Artificial-Intelligence-Integration
```

Replace `<REPOSITORY-URL>` with the URL of this GitHub repository.

### 2. Check Python

Run:

```powershell
py --version
```

A Python version number should be displayed.

### 3. Install the Python dependency

Install `requests` using:

```powershell
py -m pip install requests
```

The script uses this package to send HTTP requests to the local Ollama API.

### 4. Check Ollama

Run:

```powershell
ollama --version
```

If Ollama is installed correctly, its version number will be displayed.

### 5. Download the local model

Run:

```powershell
ollama pull llama3.2:1b
```

This downloads the local language model used by the project.

The model only needs to be downloaded once.

### 6. Test the model

The model can be tested directly with:

```powershell
ollama run llama3.2:1b
```

Enter a simple prompt to confirm that the model responds.

To leave Ollama's interactive mode, enter:

```text
/bye
```

The `/bye` command only works while inside Ollama's interactive mode. It is not a PowerShell command.

## Running the Encounter Generator

From the repository folder, run:

```powershell
py encounter_generator.py
```

The program will ask for a game location:

```text
LOCAL AI GAME ENCOUNTER GENERATOR
---------------------------------
Enter a game location:
```

Example input:

```text
Antarctic Science Station in Winter studying sentient radioactive penguins
```

The model then generates an encounter containing the required headings:

```text
ENEMY:

HAZARD:

REWARD:

ENCOUNTER:
```

After the generated encounter, the program displays telemetry such as:

```text
Model:             llama3.2:1b
Platform:          Windows-11
Response time:     3.424 seconds
Model load time:   0.282 seconds
Prompt tokens:     152
Generated tokens:  246
Generation speed:  238.42 tokens/second
```

## Telemetry Output

Each successful generation is saved as a JSON file inside:

```text
telemetry/
```

Example filename:

```text
telemetry/encounter_20260724_152210.json
```

Each file contains:

- timestamp;
- model name;
- operating-system platform;
- original location input;
- generated encounter;
- measured response time;
- Ollama total duration;
- model loading duration;
- prompt token count;
- generated token count;
- generation duration;
- calculated tokens per second.

A new file is created for every completed generation, allowing several tests to be compared.

## Output Formatting

The model is instructed to use four exact headings:

```text
ENEMY:
HAZARD:
REWARD:
ENCOUNTER:
```

A Python formatting function also normalises the heading capitalisation and spacing. This is necessary because a generative model may occasionally return headings such as `Reward:` instead of `REWARD:`.

The formatting function improves presentation but does not alter the creative content of the response.

## Suggested Test Locations

Examples that can be used to test the system include:

```text
An Antarctic science station during perpetual winter darkness
```

```text
A flooded engine room aboard a sinking spaceship
```

```text
An abandoned underground railway station occupied by sound-sensitive creatures
```

```text
A medieval observatory built above an active volcano
```

## Limitations

The model can generate plausible-sounding but factually incorrect information.

For example, an early test placed polar bears in Antarctica even though polar bears naturally live in the Arctic. This demonstrates that generative AI output should be reviewed by a human before being used in a finished game.

The `llama3.2:1b` model is relatively small and fast, but its instruction following and factual accuracy are more limited than those of larger models.

Response times can also vary. The first request is usually slower because Ollama must load the model into memory. Later requests are normally faster while the model remains loaded.

## Declared Assets

The following externally produced or assisted assets were used in this project:

- `encounter_generator.py` – Python implementation developed with assistance from ChatGPT, including the Ollama API request, telemetry collection, JSON export, error handling, and output-formatting functions.
- `llama3.2:1b` – local language model provided through Ollama and used to generate encounter content.
- `requests` – third-party Python package used to communicate with the local Ollama HTTP API.

All prompts, testing, project setup, generated evidence, evaluation, and final documentation were completed by the author.

