# TickleMyFilings

TickleMyFilings is a Python tool designed to automate the fetching and analysis of SEC filings from the EDGAR database. It simplifies the process of retrieving financial data, parsing complex XML documents, and filtering for specific information like hedge accounting or derivative instruments.

## Features

- Automated fetching of SEC filings based on CIK and form type.
- Parsing of XML filings into structured Python data types.
- Filtering of filing content based on user-defined keywords.
- Modular design for easy customization and extension.

## Getting Started

### Prerequisites

- Python 3.6+
- `pip` for installing dependencies

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/TickleMyFilings.git
cd TickleMyFilings
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Configuration

Before using TickleMyFilings, update the `HEADER` information in `data_fetching.py` to include your email or website. This is necessary to comply with the SEC's request to identify who is making the request.

```python
class TickleMyFilings:
    HEADER = {'User-Agent': 'Your Name <youremail@example.com>'}
```

Replace `'Your Name <youremail@example.com>'` with your actual name and email address or website. This is crucial for responsible use of the SEC's EDGAR system.

## Usage

The `main.py` file serves as the entry point for the TickleMyFilings tool. Here's how to run it:

```bash
python main.py
```

For custom usage, you can import and use the TickleMyFilings class in your Python scripts:

```python
from src.data_fetching import TickleMyFilings

# Initialize scraper
scraper = TickleMyFilings()

# Fetch filings
cik = '0000051143'  # Example CIK
submission_df = scraper.get_submission_df(cik, '10-K')
print(submission_df)
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests, report issues, or suggest new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This `README.md` provides an overview of your project, installation instructions, usage examples, and a reminder for users to update their personal information in the scraper's header. It's a good starting point for your GitHub repository that you can expand and customize as your project evolves.
