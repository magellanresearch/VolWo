import requests
import pandas as pd
from fake_useragent import UserAgent
from datetime import datetime

def update_fear_greed(start="2020-09-19", end=None,
                      csv_in="C:/Magellan/VolWo/program/database/fear-greed.csv",
                      csv_out="C:/Magellan/VolWo/program/database/all_fng_csv.csv",
                      pckl_out="C:/Magellan/VolWo/program/database/all_fng.pkl"):

    BASE_URL = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata/"
    ua = UserAgent()
    hdr = {"User-Agent": ua.random}

    if end is None:
        end = datetime.today().strftime('%Y-%m-%d')

    try:
        resp = requests.get(BASE_URL + start, headers=hdr, timeout=10)
        resp.raise_for_status()

        if not resp.text.strip():
            print("⚠️ Empty response from CNN API.")
            return

        json_data = resp.json()
        if "fear_and_greed_historical" not in json_data:
            print("⚠️ Unexpected JSON structure.")
            return

        json_dat = json_data["fear_and_greed_historical"]["data"]

    except requests.exceptions.RequestException as e:
        print(f"❌ CNN API error: {e}")
        print("➡️ Skipping Fear & Greed update.")
        return
    except ValueError as e:
        print(f"❌ JSON decode failed: {e}")
        print("➡️ Skipping Fear & Greed update.")
        return

    try:
        fng = (
            pd.read_csv(csv_in, parse_dates=["Date"])
              .drop_duplicates(subset="Date")
              .set_index("Date")[["Fear Greed"]]
        )

        full_idx = pd.date_range(start=fng.index.min(), end=end, freq="D")
        fng = fng.reindex(full_idx, fill_value=0)
        fng.index.name = "Date"

        df_new = pd.DataFrame([
            {
                "Date": datetime.fromtimestamp(item["x"]/1000).date(),
                "Fear Greed": item["y"]
            }
            for item in json_dat
        ]).set_index("Date")

        fng.update(df_new)
        fng.to_pickle(pckl_out)
        fng.reset_index().to_csv(csv_out, index=False)
        print("✅ Fear & Greed Index aktualisiert.")

    except Exception as e:
        print(f"❌ Data processing failed: {e}")
