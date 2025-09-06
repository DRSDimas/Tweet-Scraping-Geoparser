import pandas as pd
import os
import re

DEFINITIVE_LOCATIONS = {
    # State Institutions & Police HQs
    "Parliamentary Complex": {"lat": -6.2098, "lon": 106.8002, "keywords": ["dpr", "mpr", "parliamentary complex"]},
    "Mako Brimob Kwitang": {"lat": -6.181, "lon": 106.838, "keywords": ["mako brimob", "kwitang"]},
    "Polda Metro Jaya": {"lat": -6.2214, "lon": 106.8098, "keywords": ["polda metro jaya", "polda"]},
    "Mabes Polri": {"lat": -6.2398, "lon": 106.8015, "keywords": ["mabes polri"]},
    "Polres Metro Jaktim": {"lat": -6.221, "lon": 106.871, "keywords": ["polres metro jakarta timur", "polres jaktim"]},
    "Bekas Gedung Mapolres Jakpus": {"lat": -6.1838, "lon": 106.8457, "keywords": ["mapolres jakpus"]},
    "Kejaksaan Agung": {"lat": -6.2401, "lon": 106.7983, "keywords": ["kejaksaan agung"]},
    
    # Police Sub-precincts (Polsek) & Posts
    "Polsek Duren Sawit": {"lat": -6.237, "lon": 106.908, "keywords": ["polsek duren sawit"]},
    "Polsek Jatinegara": {"lat": -6.222, "lon": 106.87, "keywords": ["polsek jatinegara"]},
    "Polsek Matraman": {"lat": -6.205, "lon": 106.86, "keywords": ["polsek matraman"]},
    "Polsek Makasar": {"lat": -6.257, "lon": 106.877, "keywords": ["polsek makasar"]},
    "Polsek Ciracas": {"lat": -6.301, "lon": 106.879, "keywords": ["polsek ciracas"]},
    "Polsek Cipayung": {"lat": -6.311, "lon": 106.897, "keywords": ["polsek cipayung"]},
    "Pos Polisi Slipi": {"lat": -6.196, "lon": 106.8, "keywords": ["pos polisi slipi"]},
    "Pos Polisi GBK/Kemenpora": {"lat": -6.218, "lon": 106.803, "keywords": ["pos polisi gbk", "pos polisi kemenpora"]},
    "Pos Polisi Senayan": {"lat": -6.226, "lon": 106.7991, "keywords": ["pos polisi senayan"]},

    # Major Roads & Intersections
    "Jalan Gatot Subroto": {"lat": -6.2251, "lon": 106.8174, "keywords": ["gatot subroto", "gatsu"]},
    "Jalan Sudirman": {"lat": -6.2214, "lon": 106.8098, "keywords": ["sudirman"]},
    "Jalan Asia Afrika": {"lat": -6.226, "lon": 106.7991, "keywords": ["asia afrika"]},
    "Jalan Kramat Raya": {"lat": -6.1838, "lon": 106.8457, "keywords": ["kramat raya"]},
    "Jalan Otista": {"lat": -6.2282, "lon": 106.8743, "keywords": ["otista"]},
    "Jalan Casablanca": {"lat": -6.226, "lon": 106.838, "keywords": ["casablanca"]},
    "Tugu Tani": {"lat": -6.1827, "lon": 106.8347, "keywords": ["tugu tani"]},

    # Toll Gates
    "Tol Pejompongan": {"lat": -6.2015, "lon": 106.8077, "keywords": ["tol pejompongan"]},
    "Tol Slipi": {"lat": -6.196, "lon": 106.8, "keywords": ["tol slipi"]},
    "Tol Senayan": {"lat": -6.218, "lon": 106.804, "keywords": ["tol senayan"]},
    "Tol Semanggi": {"lat": -6.224, "lon": 106.815, "keywords": ["tol semanggi"]},
    "Tol Kuningan": {"lat": -6.2246, "lon": 106.8296, "keywords": ["tol kuningan"]},
    "Gerbang Pemuda": {"lat":-6.2125, "lon": 106.8036, "keywords": ["gerbang pemuda"]},

    # TransJakarta Shelters (Halte)
    "Halte Polda": {"lat": -6.2214, "lon": 106.8098, "keywords": ["halte polda"]},
    "Halte Senen Toyota Rangga": {"lat": -6.178, "lon": 106.843, "keywords": ["halte senen toyota", "halte rangga"]},
    "Halte Sentral Senen": {"lat": -6.178, "lon": 106.843, "keywords": ["halte sentral senen"]},
    "Halte Senayan Bank DKI": {"lat": -6.2242, "lon": 106.8057, "keywords": ["halte senayan bank dki"]},
    "Halte Bundaran Senayan": {"lat": -6.226, "lon": 106.802, "keywords": ["halte bundaran senayan", "halte bunsen"]},
    "Halte Pemuda Pramuka": {"lat": -6.202, "lon": 106.879, "keywords": ["halte pemuda pramuka"]},
    "Halte Bendungan Hilir": {"lat": -6.215, "lon": 106.814, "keywords": ["halte bendungan hilir", "halte benhil"]},
    "Halte Kwitang": {"lat": -6.181, "lon": 106.839, "keywords": ["halte kwitang"]},
    "Halte Kampung Melayu": {"lat": -6.227, "lon": 106.868, "keywords": ["halte kampung melayu"]},
    "Halte Kramat Sentiong": {"lat": -6.189, "lon": 106.847, "keywords": ["halte kramat sentiong"]},
    "Halte Bidara Cina": {"lat": -6.2297, "lon": 106.8671, "keywords": ["halte bidara cina"]},
    "Halte Cililitan": {"lat": -6.259, "lon": 106.86, "keywords": ["halte cililitan"]},
    "Halte Semanggi": {"lat": -6.2204, "lon": 106.8132, "keywords": ["halte semanggi"]},
    "Halte Petamburan": {"lat": -6.199, "lon": 106.803, "keywords": ["halte petamburan"]},
    "Halte Widya Candra": {"lat": -6.227, "lon": 106.8173, "keywords": ["halte widya candra"]},
    "Halte Jatinegara": {"lat": -6.2305, "lon": 106.868, "keywords": ["halte jatinegara"]},
    "Halte Matraman Baru": {"lat": -6.2132, "lon": 106.8613, "keywords": ["halte matraman baru"]},
    "Halte Masjid Agung": {"lat": -6.233, "lon": 106.797, "keywords": ["halte masjid agung"]},
    "Halte GBK": {"lat": -6.2237, "lon": 106.8059, "keywords": ["halte gelora bung karno", "halte gbk"]},

    # Rail & MRT Stations
    "Stasiun Tanah Abang": {"lat": -6.1855, "lon": 106.8105, "keywords": ["stasiun tanah abang"]},
    "Stasiun Palmerah": {"lat": -6.2077, "lon": 106.798, "keywords": ["stasiun palmerah"]},
    "Stasiun MRT Istora": {"lat": -6.2223, "lon": 106.8085, "keywords": ["stasiun istora", "mrt istora"]},
    "Stasiun MRT ASEAN": {"lat": -6.237, "lon": 106.798, "keywords": ["stasiun asean", "mrt asean"]},
    "Stasiun Pasar Senen": {"lat": -6.1744, "lon": 106.8444, "keywords": ["stasiun pasar senen"]},

    # Gathering Points & Other Locations
    "Rumah Duka Affan": {"lat": -6.195, "lon": 106.834, "keywords": ["rumah duka affan", "menteng"]},
    "TPU Karet Bivak": {"lat": -6.2026, "lon": 106.8141, "keywords": ["karet bivak", "tpu karet"]},
    "FX Sudirman Mall": {"lat": -6.225, "lon": 106.805, "keywords": ["fx sudirman"]},
    "Mal Atrium Senen": {"lat": -6.18, "lon": 106.842, "keywords": ["mal atrium senen", "atrium senen"]},
    "Looted Shops Senen": {"lat": -6.181, "lon": 106.838, "keywords": ["toko dijarah", "minimarket dijarah"]},
    "Rumah Ahmad Sahroni": {"lat": -6.115, "lon": 106.8921, "keywords": ["rumah ahmad sahroni", "kebon bawang"]},
}

def simple_geoparse(input_filename="tweets.csv"):
    if not os.path.exists(input_filename):
        print(f"[ERROR] Input file '{input_filename}' not found.")
        return

    print(f"[INFO] Reading tweets from '{input_filename}'...")
    df = pd.read_csv(input_filename)
    df.dropna(subset=['full_text'], inplace=True)
    located_tweets = []

    print("[INFO] Starting simple dictionary search...")
    for index, row in df.iterrows():
        tweet_text = row['full_text'].lower()
        matched_in_tweet = set()

        for loc_name, loc_data in DEFINITIVE_LOCATIONS.items():
            for keyword in loc_data["keywords"]:
                if re.search(r'\b' + re.escape(keyword) + r'\b', tweet_text):
                    if loc_name not in matched_in_tweet:
                        print(f"  [Match] Found '{keyword}', mapping to '{loc_name}'.")
                        located_tweets.append({
                            'matched_location': loc_name,
                            'latitude': loc_data['lat'],
                            'longitude': loc_data['lon'],
                            'full_text': row['full_text'],
                            'created_at': row['created_at']
                        })
                        matched_in_tweet.add(loc_name)
    
    if not located_tweets:
        print("\n[RESULT] No tweets matched any locations in the dictionary.")
        return

    output_df = pd.DataFrame(located_tweets)
    output_filename = "map_data.csv"
    output_df.to_csv(output_filename, index=False)
    print(f"\n[SUCCESS] Found {len(output_df)} location mentions. Your data is ready in '{output_filename}'")

if __name__ == "__main__":
    simple_geoparse()

    output_df.to_csv(output_filename, index=False)
    print(f"\n[SUCCESS] Found {len(output_df)} location mentions. Your final data is ready in '{output_filename}'")

if __name__ == "__main__":
    combine_and_geoparse()
