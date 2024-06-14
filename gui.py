import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

def scrape_data(urls, name_classes, date_classes, location_classes, description_classes, pricing_classes, referers):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    all_data = []  # List to store data from all URLs

    for i, url in enumerate(urls):
        try:
            referer = referers[i]
            response = requests.get(url=url, headers=header)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            bsobj = soup(response.content, 'html.parser')

            # Extract event names
            name_list = []
            for name_class in name_classes[i]:
                names = bsobj.select(f'.{name_class}')
                if names:
                    name_list = [name.text.strip() for name in names if name.text.strip()]
                    break
            # Fallback to meta tag content if names are not found
            if not name_list:
                meta_tags = bsobj.select('meta[content]')
                name_list = [meta['content'] for meta in meta_tags if 'content' in meta.attrs and meta['content']]
            if not name_list:
                name_list = ["N/A"]

            # Extract event dates
            date_list = []
            for date_class in date_classes[i]:
                dates = bsobj.select(f'.{date_class}')
                if dates:
                    date_list = [date.text.strip() for date in dates if date.text.strip()]
                    break
            if not date_list:
                date_list = ["N/A"]

            # Extract event locations
            location_list = []
            for location_class in location_classes[i]:
                locations = bsobj.select(f'.{location_class}')
                if locations:
                    location_list = [location.text.strip() for location in locations if location.text.strip()]
                    break
            if not location_list:
                location_list = ["N/A"]

            # Extract event descriptions
            description_list = []
            for description_class in description_classes[i]:
                descriptions = bsobj.select(f'.{description_class}')
                if descriptions:
                    description_list = [description.text.strip() for description in descriptions if description.text.strip()]
                    break
            if not description_list:
                description_list = ["N/A"]

            # Extract event pricing using both class and data-testid attributes
            pricing_list = []
            for pricing_class in pricing_classes[i]:
                pricings = bsobj.select(f'.{pricing_class}, [data-testid="{pricing_class}"]')
                if pricings:
                    pricing_list = [pricing.text.strip() for pricing in pricings if pricing.text.strip()]
                    break

            # Specific handling for nested pricing
            if not pricing_list:
                pricings = bsobj.select(f'[style="--TypographyColor: #585163;"] .{pricing_classes[i][-1]}')
                if pricings:
                    pricing_list = [pricing.text.strip() for pricing in pricings if pricing.text.strip()]

            if not pricing_list:
                pricings = bsobj.select(f'[data-testid="ticket-card-compact-size-display-price"] .{pricing_classes[i][-1]}')
                if pricings:
                    pricing_list = [pricing.text.strip() for pricing in pricings if pricing.text.strip()]

            if not pricing_list:
                pricings = bsobj.select(f'[class="eds-text-bm eds-text-weight--heavy"] .{pricing_classes[i][-1]}')
                if pricings:
                    pricing_list = [pricing.text.strip() for pricing in pricings if pricing.text.strip()]

            if not pricing_list:
                pricing_list = ["N/A"]

            # Make sure the lists have the same length
            min_length = min(len(name_list), len(date_list), len(location_list), len(description_list), len(pricing_list))

            # Create a DataFrame for current URL data
            df = pd.DataFrame({
                'Event Name': name_list[:min_length],
                'Event Date(s)': date_list[:min_length],
                'Location (if applicable)': location_list[:min_length],
                'Website URL': [url] * min_length,
                'Description': description_list[:min_length],
                'Pricing': pricing_list[:min_length]
            })

            all_data.append(df)  # Append current URL's data DataFrame to the list

        except requests.RequestException as e:
            # Handle exceptions for failed requests
            print(f"Failed to fetch data from {url}: {str(e)}")

    if all_data:
        # Concatenate all DataFrames in the list into a single DataFrame
        result_df = pd.concat(all_data, ignore_index=True)
        return result_df
    else:
        return None

def start_scraping():
    urls = url_entry.get("1.0", tk.END).strip().split("\n")
    name_classes = [name_entry.get().split(",") for name_entry in name_entries]
    date_classes = [date_entry.get().split(",") for date_entry in date_entries]
    location_classes = [location_entry.get().split(",") for location_entry in location_entries]
    description_classes = [desc_entry.get().split(",") for desc_entry in desc_entries]
    pricing_classes = [price_entry.get().split(",") for price_entry in price_entries]
    referers = ref_entry.get("1.0", tk.END).strip().split("\n")

    result_df = scrape_data(urls, name_classes, date_classes, location_classes, description_classes, pricing_classes, referers)

    if result_df is not None:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, result_df.to_string(index=False))
        messagebox.showinfo("Scraping Complete", "Data scraping and processing completed successfully.")
    else:
        messagebox.showerror("Error", "Failed to scrape data from provided URLs.")

# GUI Setup
root = tk.Tk()
root.title("Event Data Scraper")

# URL Input
url_frame = ttk.LabelFrame(root, text="Enter URLs (one per line):")
url_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
url_entry = ScrolledText(url_frame, wrap=tk.WORD, height=5)
url_entry.pack(fill=tk.BOTH, expand=True)

# Class Input
class_frame = ttk.LabelFrame(root, text="Enter CSS Classes/IDs (comma-separated):")
class_frame.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

name_entries = [tk.Entry(class_frame) for _ in range(6)]
date_entries = [tk.Entry(class_frame) for _ in range(6)]
location_entries = [tk.Entry(class_frame) for _ in range(6)]
desc_entries = [tk.Entry(class_frame) for _ in range(6)]
price_entries = [tk.Entry(class_frame) for _ in range(6)]

tk.Label(class_frame, text="Event Name Classes/IDs:").grid(row=0, column=0, sticky="w")
for i, entry in enumerate(name_entries):
    entry.grid(row=0, column=i+1)

tk.Label(class_frame, text="Event Date Classes/IDs:").grid(row=1, column=0, sticky="w")
for i, entry in enumerate(date_entries):
    entry.grid(row=1, column=i+1)

tk.Label(class_frame, text="Location Classes/IDs:").grid(row=2, column=0, sticky="w")
for i, entry in enumerate(location_entries):
    entry.grid(row=2, column=i+1)

tk.Label(class_frame, text="Description Classes/IDs:").grid(row=3, column=0, sticky="w")
for i, entry in enumerate(desc_entries):
    entry.grid(row=3, column=i+1)

tk.Label(class_frame, text="Pricing Classes/IDs:").grid(row=4, column=0, sticky="w")
for i, entry in enumerate(price_entries):
    entry.grid(row=4, column=i+1)

# Referrer Input
ref_frame = ttk.LabelFrame(root, text="Enter Referrer URLs (one per line):")
ref_frame.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)
ref_entry = ScrolledText(ref_frame, wrap=tk.WORD, height=2)
ref_entry.pack(fill=tk.BOTH, expand=True)

# Result Display
result_frame = ttk.LabelFrame(root, text="Scraped Data:")
result_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
result_text = ScrolledText(result_frame, wrap=tk.WORD, height=10)
result_text.pack(fill=tk.BOTH, expand=True)

# Start Button
start_button = ttk.Button(root, text="Start Scraping", command=start_scraping)
start_button.pack(pady=10)

# Run the GUI main loop
root.mainloop()
