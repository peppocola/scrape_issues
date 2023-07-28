import os
import yaml
import pandas as pd
from github import Github
from tqdm import tqdm
import time

def download_issues_to_csv(github_link, output_dir, access_token, remaining_requests):
    # Parse the GitHub link to extract owner and repo names
    owner, repo = github_link.split('/')[-2:]

    # Connect to GitHub using the provided access token
    g = Github(access_token)

    # Get the repository
    repository = g.get_repo(f"{owner}/{repo}")

    # Get all issues from the repository
    issues = repository.get_issues(state="all")

    # Create a list to store issue data
    issue_data = []
    for issue in tqdm(issues, desc=f"Processing {owner}/{repo}", unit="issue"):
        labels = [label.name for label in issue.labels]
        issue_data.append({
            'Title': issue.title,
            'Body': issue.body,
            'Labels': ', '.join(labels),
            'URL': issue.html_url
        })

        # Check the GitHub API rate limit and wait if needed
        remaining_requests -= 1
        if remaining_requests == 0:
            reset_time = g.rate_limiting_resettime
            sleep_duration = reset_time - time.time() + 10  # Adding 10 seconds buffer
            print(f"Rate limit exceeded. Waiting for {sleep_duration:.2f} seconds.")
            time.sleep(sleep_duration)

    # Create a DataFrame from the issue data
    df = pd.DataFrame(issue_data)

    # Get the absolute path of the output directory
    abs_output_dir = os.path.abspath(output_dir)

    # Create the output directory if it doesn't exist
    os.makedirs(abs_output_dir, exist_ok=True)

    # Prepare the CSV file path
    csv_filename = f"{owner}#{repo}.csv"
    csv_filepath = os.path.join(abs_output_dir, csv_filename)

    # Write the DataFrame to the CSV file
    df.to_csv(csv_filepath, index=False, encoding='utf-8')

    print(f"Issues downloaded and saved to {csv_filepath}")

def main():
    # Read the YAML file containing the GitHub project links, the single output directory, and the access token
    with open('config.yaml', 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)

    # Get the relative output directory from the config
    output_dir = config['output_dir']

    # Get the access token from the config
    access_token = config['access_token']

    # Get the list of GitHub project links from the config
    github_links = config['projects']

    for link in github_links:
        # Get the remaining API requests allowed
        g = Github(access_token)
        remaining_requests = g.get_rate_limit().core.remaining
        download_issues_to_csv(link, output_dir, access_token, remaining_requests)
        print(f"Remaining requests: {remaining_requests}")

if __name__ == "__main__":
    main()
