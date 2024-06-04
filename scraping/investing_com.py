import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

import requests
from bs4 import BeautifulSoup
import json
import logging
from datetime import datetime
from dateutil import parser
from tabulate import tabulate
from custom_constants import defs

# Configure logging to file and stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('scraping_output.log'),
                        logging.StreamHandler(sys.stdout)
                    ])

def scrape_investing_com(pair_id, period):
    url = "https://www.investing.com/technical/Service/GetStudiesContent"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.investing.com/technical/gbp-usd-technical-analysis",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "pairID": pair_id,
        "period": period,
    }

    payload_encoded = f"pairID={pair_id}&period={period}"

    response = requests.post(url, headers=headers, data=payload_encoded)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        data = {}

        # Summary Box
        data['pair'] = soup.select_one('#quoteLink').text.strip() if soup.select_one('#quoteLink') else 'N/A'
        data['last_value'] = soup.select_one('.lastValue').text.strip() if soup.select_one('.lastValue') else 'N/A'
        data['update_time'] = soup.select_one('.updateTime').text.strip() if soup.select_one('.updateTime') else 'N/A'
        data['summary'] = soup.select_one('.summary .buy').text.strip() if soup.select_one('.summary .buy') else 'N/A'

        # Find the correct Moving Averages and Technical Indicators Summary
        ma_summary = None
        ti_summary = None
        for div in soup.select('#techStudiesInnerBoxRight .summaryTableLine'):
            if 'Moving Averages' in div.text:
                ma_summary = div
            elif 'Technical Indicators' in div.text:
                ti_summary = div

        if ma_summary:
            data['moving_averages'] = {
                'buy': ma_summary.find(string='Moving Averages:').find_next('i', {'id': 'maBuy'}).text.strip() if ma_summary.find(string='Moving Averages:') else 'N/A',
                'sell': ma_summary.find(string='Moving Averages:').find_next('i', {'id': 'maSell'}).text.strip() if ma_summary.find(string='Moving Averages:') else 'N/A'
            }
        else:
            data['moving_averages'] = {
                'buy': 'N/A',
                'sell': 'N/A'
            }

        if ti_summary:
            data['technical_indicators'] = {
                'buy': ti_summary.find(string='Technical Indicators:').find_next('i', {'id': 'maBuy'}).text.strip() if ti_summary.find(string='Technical Indicators:') else 'N/A',
                'sell': ti_summary.find(string='Technical Indicators:').find_next('i', {'id': 'maSell'}).text.strip() if ti_summary.find(string='Technical Indicators:') else 'N/A'
            }
        else:
            data['technical_indicators'] = {
                'buy': 'N/A',
                'sell': 'N/A'
            }

        # Pivot Points
        pivot_points = []
        for row in soup.select('#curr_table tbody tr'):
            cols = row.find_all('td')
            if len(cols) >= 8:
                pivot_points.append({
                    'name': cols[0].text.strip(),
                    's3': cols[1].text.strip(),
                    's2': cols[2].text.strip(),
                    's1': cols[3].text.strip(),
                    'pivot_points': cols[4].text.strip(),
                    'r1': cols[5].text.strip(),
                    'r2': cols[6].text.strip(),
                    'r3': cols[7].text.strip(),
                })
        data['pivot_points'] = pivot_points

        # Technical Indicators
        technical_indicators = []
        for row in soup.select('.technicalIndicatorsTbl tbody tr'):
            cols = row.find_all('td')
            if len(cols) == 3:
                technical_indicators.append({
                    'name': cols[0].text.strip(),
                    'value': cols[1].text.strip(),
                    'action': cols[2].text.strip(),
                })
        data['technical_indicators_details'] = technical_indicators

        # Moving Averages
        moving_averages = []
        for row in soup.select('.movingAvgsTbl tbody tr'):
            cols = row.find_all('td')
            if len(cols) == 3:
                moving_averages.append({
                    'period': cols[0].text.strip(),
                    'simple': cols[1].text.strip(),
                    'exponential': cols[2].text.strip(),
                })
        data['moving_averages_details'] = moving_averages

        # Format update_time
        update_time = data["update_time"]
        if update_time != 'N/A':
            # Remove the timezone part
            update_time = update_time.split(' (')[0]
            update_time = parser.parse(update_time).strftime('%Y-%m-%d %H:%M')
            data["update_time"] = update_time

        return data
    else:
        logging.error(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def calculate_percentage(data):
    for entry in data:
        ma_buy = int(entry['moving_averages']['buy']) if entry['moving_averages']['buy'] != 'N/A' else 0
        ma_sell = int(entry['moving_averages']['sell']) if entry['moving_averages']['sell'] != 'N/A' else 0
        total_signals = ma_buy + ma_sell

        if total_signals > 0:
            ma_bullish_percentage = (ma_buy / total_signals) * 100
            ma_bearish_percentage = (ma_sell / total_signals) * 100
        else:
            ma_bullish_percentage = 0
            ma_bearish_percentage = 0

        entry['ma_bullish_percentage'] = ma_bullish_percentage
        entry['ma_bearish_percentage'] = ma_bearish_percentage

        entry['ma_bullish_percentage_str'] = f"{ma_bullish_percentage:.2f}%"
        entry['ma_bearish_percentage_str'] = f"{ma_bearish_percentage:.2f}%"

        # Log the percentages
        logging.info(f"Pair ID: {entry['pair_id']}, Time Frame: {entry['time_frame']}, Bullish: {entry['ma_bullish_percentage_str']}, Bearish: {entry['ma_bearish_percentage_str']}")

        # Include the calculated percentages in the response
        entry['moving_averages']['bullish_percentage'] = entry['ma_bullish_percentage_str']
        entry['moving_averages']['bearish_percentage'] = entry['ma_bearish_percentage_str']


def log_to_table(data):
    headers = ["pair_id", "time_frame", "updated", "pair_name", "last_value", "summary/S3", "ma_buy/S2", "ma_sell/S1", "ti_buy/Pivot", "ti_sell/R1", "R2", "R3", "ma_bullish%", "ma_bearish%"]
    table_data = []

    for entry in data:
        row = [
            str(entry.get("pair_id", "N/A")),
            str(entry.get("time_frame", "N/A")),
            str(entry.get("update_time", "N/A")),
            entry.get("pair", "N/A"),
            entry.get("last_value", "N/A"),
            entry.get("summary", "N/A"),
            str(entry["moving_averages"].get("buy", "N/A")),
            str(entry["moving_averages"].get("sell", "N/A")),
            str(entry["technical_indicators"].get("buy", "N/A")),
            str(entry["technical_indicators"].get("sell", "N/A")),
            entry.get('ma_bullish_percentage_str', "0.00%"),
            entry.get('ma_bearish_percentage_str', "0.00%")
        ]

        table_data.append(row)

        for pivot_point in entry.get("pivot_points", []):
            pivot_row = [
                entry.get("pair_id", "N/A"),
                entry.get("time_frame", "N/A"),
                entry.get("update_time", "N/A"),
                entry.get("pair", "N/A"),
                "Pivot: " + pivot_point.get("name", "N/A"),
                pivot_point.get("s3", "N/A"),
                pivot_point.get("s2", "N/A"),
                pivot_point.get("s1", "N/A"),
                pivot_point.get("pivot_points", "N/A"),
                pivot_point.get("r1", "N/A"),
                pivot_point.get("r2", "N/A"),
                pivot_point.get("r3", "N/A"),
                entry.get('ma_bullish_percentage_str', "0.00%"),
                entry.get('ma_bearish_percentage_str', "0.00%")
            ]
            table_data.append(pivot_row)

    table_str = tabulate(table_data, headers=headers, tablefmt="plain")

    # Log the table to the file and print to stdout
    logging.info("\n" + table_str)
    print("\n" + table_str)


def investing_com():
    pair_ids = range(1, 9)  # Pair IDs between 1 and 8
    periods = [3600, 86400]  # Hourly and daily periods (assuming these are in seconds)

    all_data = []

    for pair_id in pair_ids:
        for period in periods:
            logging.info(f"Fetching data for pair_id: {pair_id}, period: {period}")
            data = scrape_investing_com(pair_id, period)
            if data:
                logging.info(data)
                data["pair_id"] = pair_id
                data["time_frame"] = period
                all_data.append(data)
            else:
                logging.info(f"No data found for pair_id: {pair_id}, period: {period}")

    # Calculate percentages
    calculate_percentage(all_data)

    # Save to JSON
    with open('all_pairs_data.json', 'w') as f:
        json.dump(all_data, f, indent=4)
    logging.info("Data saved to all_pairs_data.json")

    # Log to table format and print to stdout
    log_to_table(all_data)


def get_pair(pair_name, tf):
    

    if tf not in defs.TFS:
        tf = defs.TFS['H1']
    else:
        tf = defs.TFS[tf]

    if pair_name in defs.INVESTING_COM_PAIRS:
        pair_id = defs.INVESTING_COM_PAIRS[pair_name]['pair_id']
        return scrape_investing_com(pair_id, tf)