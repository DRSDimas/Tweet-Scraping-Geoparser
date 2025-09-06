# X (Twitter) Event Heatmap Scraper

This repository provides two Python scripts (`scraper.py` and `geoparser.py`) to map the online discussion surrounding a real-world event.

There are many ways to get data from X (Twitter), including powerful paid APIs and services that are faster, more efficient, and obviously scrape much more data. However, most of these require paid subscriptions or pre-purchased fleets of "safe" accounts for scraping. This project, however, was built to provide a **completely free, zero-budget solution**. It's designed for anyone using a budget computer who wants to perform this kind of analysis without any financial cost.

## Important Disclaimer
  * It is critical to understand that this toolkit performs a **confirmatory analysis, not an exploratory one**. The `geoparser.py` script is not an advanced AI that can automatically detect and discover new, unknown locations from tweet text. It can only find locations that you have pre-defined in its (`DEFINITIVE_LOCATIONS`) dictionary. This means that thorough preliminary research is the most important step of any project using this tool. You must first identify all potential hotspots and relevant locations from news articles, reports, and other sources before you begin.
 * The purpose of this tool is to map the volume and intensity of online discussion surrounding these **known locations, not to discover new ones**. This approach was chosen for its reliability and accuracy, as it avoids the errors and false positives that more advanced methods can sometimes produce.
  * **Use a Burner Account**, because this kind of automated activity is against X's (Twitter's) terms of service. **DO NOT use your personal X account for this.** The account you use is at high risk of being temporarily or permanently banned. Create a new, disposable "burner" account specifically for this project.
  * This tool scrapes public data. Be responsible and ethical with how you use, analyze, and present the information you collect.
  * This project is intended for educational and research purposes to understand the dynamics of social media data and geospatial analysis.

## Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites

  * Python 3.8+
  * pip (Python package installer)

### Installation & Setup

1.  **Clone the repository** to your local machine:
    ```sh
    git clone [Your-GitHub-Repo-URL]
    cd [your-repo-name]
    ```
2.  **Create a Python virtual environment.** This is highly recommended to keep dependencies isolated.
    ```sh
    python -m venv venv
    ```
3.  **Activate the virtual environment.**
      * On Windows (PowerShell): `.\venv\Scripts\Activate`
      * On macOS/Linux: `source venv/bin/activate`
4.  **Install the required libraries.**
    ```sh
    pip install pandas playwright
    playwright install
    ```

### Configuration: Getting Your Cookie

To bypass the login wall, the script needs to use an authentication cookie from your **burner account**.

1.  Using Google Chrome, log in to X.com with your **burner account**.
2.  Press **F12** to open the Chrome Developer Tools.
3.  Go to the **"Application"** tab.
4.  On the left, expand the **"Cookies"** section and click on `https://x.com`.
5.  Find the cookie named **`auth_token`**.
6.  Copy the entire long string from the **"Cookie Value"** field.
7.  In your project folder, create a new file named **`cookies.json`**.
8.  Paste the following text into the file, replacing `"PASTE_YOUR_TOKEN_HERE"` with the value you just copied:
    ```json
    [
      {
        "name": "auth_token",
        "value": "PASTE_YOUR_TOKEN_HERE",
        "domain": ".x.com"
      }
    ]
    ```
## Usage

This project uses a two-stage process to ensure the final data is both comprehensive and geographically relevant.

### Step 1: Broad Thematic Scraping

First, we scrape X (Twitter) for a large number of tweets that are thematically related to the event, without initially filtering for location.

1.  Open `scraper_thematic.py` in your code editor.
2.  Modify the `PROTEST_KEYWORDS` list and the `START_DATE`/`END_DATE` to match your event.
3.  Run the script from your activated terminal:
    ```sh
    python scraper_thematic.py
    ```
    This will produce a CSV file (e.g., `thematic_tweets.csv`) containing thousands of tweets that are generally about the protest but may or may not mention a specific location.

### Step 2: Geographic Parsing and Filtering

Next, we process the large, "noisy" file from Step 1. This script will read every tweet and act as a filter, keeping only the ones that contain a specific, known location from your research.

1.  Open `geoparser_simple.py`.
2.  Update the `DEFINITIVE_LOCATIONS` dictionary with the precise names, keywords, and coordinates for your specific project.
3.  Make sure the `input_filename` in the script matches the output file from the scraper (e.g., `"thematic_tweets.csv"`).
4.  Run the script:
    ```sh
    python geoparser_simple.py
    ```
    This will produce your final, clean dataset (e.g., `simple_map_data.csv`), which is now ready for visualization in ArcGIS Pro, QGIS, or other mapping software.

-----

## Limitations and Best Practices

  * X is very good at detecting automated activity. The script uses a batching method to break up searches and includes cool-down periods to seem more human (yes, it is what it is), but it can still be blocked.
  * The script is designed to search for a small number of keywords at a time (`CHUNK_SIZE`). Do not set this number too high (5-8 is a good range). Searching for 30+ keywords at once will likely fail, since X would rate-limit your account during midscraping.
  * If the script suddenly stops working and fails on every batch, X has likely rate-limited or "poisoned" your account's session. The best solution is to **log out and log back in** to your burner account, get a **new `auth_token`**, and update your `cookies.json` file. Sometimes, you may need to create a completely new burner account.
  * This method scrapes the "Top" search results for a given query and date range. It does not capture an exhaustive archive of every single tweet ever posted. The results are what X's algorithm considers most relevant.
