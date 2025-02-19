# ScrapeyDocs

## The problem

- You want an LLM to write code for you, because you're too busy, lazy, or code illiterate to do that yourself. Me too, friend.
- But copy-pasting chunks (or entire pages) of documentation from your favorite open source project into an LLM's winking context hole isn't clever or fun. This bit depends on that bit, and before you know it, you are drowning in worthless error messages and apologies.

## The solution

- Run a script on your Windows, Mac, or Linux box
- Feed it a URL of a documentation site
- Sit back and enjoy a beverage
- Get a single lightweight text or md file dropped in your lap
- Feed that file to your large context window LLM or pop it in your RAGhole
- Now your LLM knows all the things. Kind of.

## What this is

Take it away, ChatGPT:

> A simple Python-based web scraper for downloading and compiling documentation from any website into Markdown and plain text formats. This tool is ideal for scraping documentation sites and consolidating the content into a single file with a Table of Contents, which you can then feed to a large context window LLM directly or via a more involved RAG setup.

## Features

This thing:

- Scrapes multiple pages from a documentation site.
- Automatically generates a combined Markdown file with a Table of Contents.
- Outputs both a `.md` and a `.txt` file. AT NO EXTRA COST!
- Uses a Python virtual environment to manage dependencies for easy setup on Windows, Linux, or MacOS.

## Installation and usage

### Prerequisites

- Python 3.6 or higher
- `pip` package manager

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/michaelpick/ScrapeyDocs
   cd documentation-scraper

2. **Install option 1: run the setup script:**

**Linux/Mac:** Make the shell script executable and run it

```bash
chmod +x run_documentation-scraper.sh
./run_documentation-scraper.sh
```

**Windows:** Double-click run_documentation-scraper.bat or run the following command in a command prompt:

```batch
run_documentation-scraper.bat
```

The script will:

- Set up a Python virtual environment.
- Install all required dependencies.
- Prompt you for a URL to scrape.
- Scrape the site and generate output files in the Outputs directory.

**Install option 2: Installing requiremnents manually**

Don't want to run a batch or shell script? All good. Just install the requirements manually.

1. Create and activate a virtual environment (optional but recommended):

**On Linux/Mac**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows**

```batch
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies using requirements.txt:

```bash
pip install -r requirements.txt
```

### Running the script manually

Want to run it manually, too? Have at it:

1. Activate the virtual environment:

Linux/MacOS:

```bash
source venv/bin/activate
```

Windows:

```batch
venv\Scripts\activate
```

2. Run the scraper script:

```bash
python documentation-scraper.py
```

3. Deactivate the virtual environment when done:

Linux/MacOS/Windows:

```batch
deactivate
```

### Output

The output files will be located in the Outputs directory, under a subdirectory named after the domain of the URL you scraped. The generated files will include:

`<domain>_documentation.md`: The combined Markdown file with a Table of Contents.
`<domain>_documentation.txt`: A plain text version of the documentation.

#### Example

For a website with the domain `example.com`, the output directory structure will look like this:

```
Outputs/
└── example_com/
    ├── example_com_documentation.md
    └── example_com_documentation.txt
```

## Credits

- All the hard work: ChatGPT 4o.
- Unreasonable demands, testing, and fist shaking by me, an illiterate code idiot who just needed a script.

## Need help?

ChatGPT is entirely to blame for anything that goes wrong and therefore best equipped to answer your troubleshooting questions.
