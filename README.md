# GitHub Project Scraper

This is a Python script (scrape.py) that allows you to download and save issues from multiple GitHub projects to CSV files. The script uses the GitHub API to fetch issues from the specified projects and saves them in separate CSV files containing the issue title, body, labels, and URL.

## Requirements

- Python 3.x
- Install the required libraries using pip:

```bash
pip install -r requirements.txt
```

Make sure to have a valid GitHub access token for authentication. Please do not share your access token publicly.

## Configuration

1. Create a YAML configuration file named `config.yaml` in the root directory of the project.
2. Add the following details to the `config.yaml` file:

```yaml
output_dir: /path/to/output/directory
access_token: YOUR_GITHUB_ACCESS_TOKEN
projects:
  - https://github.com/owner1/repo1
  - https://github.com/owner2/repo2
  # Add more GitHub project links as needed
```

Replace `/path/to/output/directory` with the directory where you want to save the CSV files. Also, replace `YOUR_GITHUB_ACCESS_TOKEN` with your GitHub access token. Make sure to avoid sharing this token publicly.

## Usage

1. Ensure you have set up the `config.yaml` file correctly with the required project URLs and access token.
2. Run the Python script `scrape.py`:

```bash
python scrape.py
```

The script will start fetching issues from the specified GitHub projects and save them in separate CSV files.

## Note

- This script uses the GitHub API, and it's subject to rate limits. The script will pause execution and wait if the rate limit is exceeded.
- The CSV files will be saved in the specified `output_dir` directory.

## Contributing

Contributions are welcome! If you find any issues or want to add enhancements, feel free to submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
