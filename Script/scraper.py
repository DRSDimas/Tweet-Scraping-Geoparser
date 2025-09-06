import json
import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError
import time
import random
import os

PROTEST_KEYWORDS = [
  "affan kurniawan", "ojol", "brimob", "polri", "parcok", "demo", "protes", 
  "unjuk rasa", "mahasiswa", "konvoi", "long march", "standoff", "bentrok",  "ricuh", 
  "rusuh", "anarkis", "bakar", "terluka", "dipukul", "vandalisme", "dirusak", "looting", 
  "jarah", "gas air mata", "tear gas", "tembakan", "1312"
]

START_DATE = "2025-08-28"
END_DATE = "2025-08-31"

SCROLL_ATTEMPTS = 100 # The more general your keywords are, the more scroll is usually needed.

def parse_tweets_simple(raw_json_data):
    cleaned_tweets = []
    for instruction in raw_json_data.get('data', {}).get('search_by_raw_query', {}).get('search_timeline', {}).get('timeline', {}).get('instructions', []):
        if instruction.get('type') == 'TimelineAddEntries':
            for entry in instruction.get('entries', []):
                content = entry.get('content', {})
                if content.get('entryType') == 'TimelineTimelineItem':
                    item_content = content.get('itemContent', {})
                    if item_content.get('itemType') == 'TimelineTweet':
                        tweet_results = item_content.get('tweet_results', {})
                        result = tweet_results.get('result', {})
                        legacy = result.get('legacy', {})
                        cleaned_tweets.append({
                            'created_at': legacy.get('created_at'),
                            'username': result.get('core', {}).get('user_results', {}).get('result', {}).get('legacy', {}).get('screen_name'),
                            'full_text': legacy.get('full_text'),
                            'place_full_name': legacy.get('place', {}).get('full_name') if legacy.get('place') else None
                        })
    return cleaned_tweets

def main():
    if not os.path.exists("cookies.json"): print("[ERROR] 'cookies.json' file not found."); return
    with open("cookies.json", 'r') as f: cookies = json.load(f)

    all_parsed_tweets = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        context.add_cookies(cookies)
        page = context.new_page()
        
        intercepted_data = []
        def handle_response(response):
            if "SearchTimeline" in response.url:
                try: intercepted_data.append(response.json())
                except Exception: pass
        page.on("response", handle_response)

        print(f"\n[INFO] Starting broad thematic search...")
        
        try:
            keyword_query = " OR ".join(PROTEST_KEYWORDS)
            date_query = f"since:{START_DATE} until:{END_DATE}"
            full_query = f"({keyword_query}) {date_query}"
            target_url = f"https://x.com/search?q={full_query.replace(' ', '%20')}&src=typed_query"

            print(f"  [*] Searching for general protest keywords...")
            page.goto(target_url, wait_until="domcontentloaded", timeout=90000)
            page.wait_for_selector('article[data-testid="tweet"]', timeout=30000)
            
            print(f"  [+] Page loaded, scrolling {SCROLL_ATTEMPTS} times...")
            for j in range(SCROLL_ATTEMPTS):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(random.uniform(1.5, 2.5)) # This is the cooldown time between scroll
            
            for raw_json in intercepted_data:
                parsed_tweets = parse_tweets_simple(raw_json)
                if parsed_tweets: all_parsed_tweets.extend(parsed_tweets)

        except TimeoutError:
            print(f"  [!] No results found for the thematic search.")
        except Exception as e:
            print(f"  [!] An unexpected error occurred: {e}.")
        
        browser.close()

    if not all_parsed_tweets: print("\n[RESULT] The entire search found 0 tweets."); return

    df = pd.DataFrame(all_parsed_tweets)
    df.drop_duplicates(subset='full_text', inplace=True)
    output_filename = "tweets.csv"
    df.to_csv(output_filename, index=False)
    
    print(f"\n[SUCCESS] Saved {len(df)} unique thematic tweets to '{output_filename}'")

if __name__ == "__main__":
    main()
