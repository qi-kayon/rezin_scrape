# -*- coding: utf-8 -*-
"""Rez_Scrape_Historic_Reco

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dPAz_tq009DNKulIpxFpiHA3TK-iw3YS
"""

!pip install PyPDF2
import requests
import io
import PyPDF2
import pandas as pd
from datetime import datetime

# List of all valid dates
valid_dates = [
    "2024-09-06", "2024-08-30", "2024-08-23", "2024-08-16", "2024-08-09", "2024-08-02",
    "2024-07-26", "2024-07-19", "2024-07-12", "2024-07-05", "2024-06-28", "2024-06-21",
    "2024-06-14", "2024-06-07", "2024-05-31", "2024-05-24", "2024-05-17", "2024-05-10",
    "2024-05-03", "2024-04-26", "2024-04-19", "2024-04-12", "2024-04-05", "2024-03-29",
    "2024-03-22", "2024-03-15", "2024-03-08", "2024-03-01", "2024-02-23", "2024-02-16",
    "2024-02-09", "2024-02-02", "2024-01-26", "2024-01-19", "2024-01-12", "2024-01-05",
    # 2023 dates
    "2023-12-29", "2023-12-22", "2023-12-15", "2023-12-08", "2023-12-01", "2023-11-24",
    "2023-11-17", "2023-11-10", "2023-11-03", "2023-10-27", "2023-10-20", "2023-10-13",
    "2023-10-06", "2023-09-29", "2023-09-22", "2023-09-15", "2023-09-08", "2023-09-01",
    "2023-08-25", "2023-08-18", "2023-08-11", "2023-08-04", "2023-07-28", "2023-07-21",
    "2023-07-14", "2023-07-07", "2023-06-30", "2023-06-23", "2023-06-16", "2023-06-09",
    "2023-06-02", "2023-05-26", "2023-05-19", "2023-05-12", "2023-05-05", "2023-04-28",
    "2023-04-21", "2023-04-14", "2023-04-07", "2023-03-31", "2023-03-24", "2023-03-17",
    "2023-03-10", "2023-03-03", "2023-02-24", "2023-02-17", "2023-02-10", "2023-02-03",
    "2023-01-27", "2023-01-20", "2023-01-13", "2023-01-06",
    # 2022 dates
    "2022-12-30", "2022-12-23", "2022-12-16", "2022-12-09", "2022-12-02", "2022-11-25",
    "2022-11-18", "2022-11-11", "2022-11-04", "2022-10-28", "2022-10-21", "2022-10-14",
    "2022-10-07", "2022-09-30", "2022-09-23", "2022-09-16", "2022-09-09", "2022-09-02",
    "2022-08-26", "2022-08-19", "2022-08-12", "2022-08-05", "2022-07-29", "2022-07-22",
    "2022-07-15", "2022-07-08", "2022-07-01", "2022-06-24", "2022-06-17", "2022-06-10",
    "2022-06-03", "2022-05-27", "2022-05-20", "2022-05-13", "2022-05-06", "2022-04-29",
    "2022-04-22", "2022-04-15", "2022-04-08", "2022-04-01", "2022-03-25", "2022-03-18",
    "2022-03-11", "2022-03-04", "2022-02-25", "2022-02-18", "2022-02-11", "2022-02-04",
    "2022-01-28", "2022-01-21", "2022-01-14", "2022-01-07",
    # 2021 dates
    "2021-12-31", "2021-12-24", "2021-12-17", "2021-12-10", "2021-12-03", "2021-11-26",
    "2021-11-19", "2021-11-12", "2021-11-05", "2021-10-29", "2021-10-22", "2021-10-15",
    "2021-10-08", "2021-10-01", "2021-09-24", "2021-09-17", "2021-09-10", "2021-09-03",
    "2021-08-27", "2021-08-20", "2021-08-13", "2021-08-06", "2021-07-30", "2021-07-23",
    "2021-07-16", "2021-07-09", "2021-07-02", "2021-06-25", "2021-06-18", "2021-06-11",
    "2021-06-04", "2021-05-28", "2021-05-21", "2021-05-14", "2021-05-07", "2021-04-30",
    "2021-04-23", "2021-04-16", "2021-04-09", "2021-04-02", "2021-03-26", "2021-03-19",
    "2021-03-12", "2021-03-05", "2021-02-26", "2021-02-19", "2021-02-12", "2021-02-05",
    "2021-01-29", "2021-01-22", "2021-01-15", "2021-01-08", "2021-01-01",
    # 2020 dates
    "2020-12-25", "2020-12-18", "2020-12-11", "2020-12-04", "2020-11-27", "2020-11-20",
    "2020-11-13", "2020-11-06", "2020-10-30", "2020-10-23", "2020-10-16", "2020-10-09",
    "2020-10-02", "2020-09-25", "2020-09-18", "2020-09-11", "2020-09-04", "2020-08-28",
    "2020-08-21", "2020-08-14", "2020-08-07", "2020-07-31", "2020-07-24", "2020-07-17",
    "2020-07-10", "2020-07-02", "2020-06-26", "2020-06-19", "2020-06-12", "2020-06-05",
    "2020-05-29", "2020-05-22", "2020-05-15", "2020-05-08", "2020-05-01", "2020-04-24",
    "2020-04-17", "2020-04-10", "2020-04-03", "2020-03-27", "2020-03-20", "2020-03-13",
    "2020-03-06", "2020-02-28", "2020-02-21", "2020-02-14", "2020-02-07", "2020-01-31",
    "2020-01-24", "2020-01-17", "2020-01-10", "2020-01-03",
    # 2019 dates
    "2019-12-27", "2019-12-20", "2019-12-13", "2019-12-06", "2019-11-29", "2019-11-22",
    "2019-11-15", "2019-11-08", "2019-11-01", "2019-10-25", "2019-10-18", "2019-10-11",
    "2019-10-04", "2019-09-27", "2019-09-20", "2019-09-13", "2019-09-06", "2019-08-30",
    "2019-08-23", "2019-08-16", "2019-08-09", "2019-08-02", "2019-07-26", "2019-07-19",
    "2019-07-12", "2019-07-05", "2019-06-28", "2019-06-21", "2019-06-14", "2019-06-07",
    "2019-05-31", "2019-05-24", "2019-05-17", "2019-05-10", "2019-05-03", "2019-04-26",
    "2019-04-19", "2019-04-12", "2019-04-05", "2019-03-29", "2019-03-22", "2019-03-15",
    "2019-03-08", "2019-03-01", "2019-02-22", "2019-02-15", "2019-02-08", "2019-02-01",
    "2019-01-25", "2019-01-18", "2019-01-11", "2019-01-04",
    # 2018 dates
    "2018-12-28", "2018-12-21", "2018-12-14", "2018-12-07", "2018-11-30", "2018-11-16",
    "2018-11-09", "2018-11-02", "2018-10-26", "2018-10-19", "2018-10-05", "2018-09-28",
    "2018-09-21", "2018-09-14", "2018-09-07", "2018-08-31", "2018-08-24", "2018-08-17",
    "2018-08-10", "2018-08-03", "2018-07-27", "2018-07-20", "2018-07-13", "2018-07-06",
    "2018-06-29", "2018-06-22", "2018-06-15", "2018-06-08", "2018-06-01", "2018-05-25",
    "2018-05-18", "2018-05-11", "2018-05-04", "2018-04-27", "2018-04-20", "2018-04-13",
    "2018-04-06", "2018-03-30", "2018-03-23", "2018-03-16", "2018-03-09", "2018-03-02",
    "2018-02-23", "2018-02-16", "2018-02-09", "2018-02-02", "2018-01-26", "2018-01-18",
    "2018-01-12", "2018-01-05"
]

# URL template (replace date placeholder with actual date)
url_template = "https://knowthefactsmmj.com/wp-content/uploads/ommu_updates/{year}/{date}-OMMU-Update.pdf"

def download_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Successfully downloaded PDF from {url}")
        return io.BytesIO(response.content)
    else:
        print(f"Failed to download PDF from {url}. Status code: {response.status_code}")
        return None

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_table_from_text(text):
    lines = text.split('\n')
    table_data = []
    headers = ["MMTC Name", "Dispensing Locations", "Medical Marijuana (mgs THC)",
               "Low-THC Cannabis (mgs CBD)", "Marijuana in a Form for Smoking (oz)"]

    for i, line in enumerate(lines):
        if "Trulieve" in line:  # Start of the table data
            for j in range(i, len(lines)):
                parts = lines[j].split()
                if len(parts) >= 5 and parts[0] != "Total":
                    try:
                        smoking = float(parts[-1].replace(',', ''))
                        low_thc = int(parts[-2].replace(',', ''))
                        medical_marijuana = int(parts[-3].replace(',', ''))
                        locations = int(parts[-4])
                        mmtc_name = " ".join(parts[:-4])
                        table_data.append([mmtc_name, locations, medical_marijuana, low_thc, smoking])
                        print(f"Processed row: {mmtc_name}")
                    except ValueError as e:
                        print(f"Error processing line {j}: {e}")
                        print(f"Line content: {lines[j]}")
                elif "Total" in lines[j]:
                    print(f"Table end found on line {j}: {lines[j]}")
                    break
            break  # Exit the outer loop once we've processed the table

    print(f"Extracted {len(table_data)} rows of data")
    return headers, table_data

def process_data(data, headers, report_date):
    if not data:
        print("No data to process")
        return None
    df = pd.DataFrame(data, columns=headers)
    df['Report Date'] = report_date
    return df

def process_single_report(url, report_date):
    pdf_file = download_pdf(url)
    if pdf_file:
        pdf_text = extract_text_from_pdf(pdf_file)
        headers, table_data = extract_table_from_text(pdf_text)
        if table_data:
            return process_data(table_data, headers, report_date)
        else:
            print("No data extracted from PDF")
            return None
    else:
        print("Failed to download PDF")
        return None

# Main execution
if __name__ == "__main__":
    combined_data = pd.DataFrame()  # Create an empty DataFrame to hold all data

    for report_date_str in valid_dates:
        report_date = datetime.strptime(report_date_str, "%Y-%m-%d")
        url = url_template.format(year=report_date.year, date=report_date.strftime("%m%d%y"))

        print(f"Processing report for {report_date_str}...")
        processed_data = process_single_report(url, report_date_str)

        if processed_data is not None:
            combined_data = pd.concat([combined_data, processed_data], ignore_index=True)

    # After looping through all the dates, save the combined data to CSV
    if not combined_data.empty:
        combined_data.to_csv('combined_cannabis_data.csv', index=False)
        print("\nAll reports processed and saved to 'combined_cannabis_data.csv'")
    else:
        print("No data was processed.")

