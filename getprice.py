import json
import re

# Assuming `json_data` is your JSON string with the sections
# If the JSON data is in a file, you can load it like this:
# with open('extracted_data_with_prices.json', 'r') as f:
#     sections = json.load(f)

# Let's say json_data is your JSON string
with open ('lunch.json', 'r') as f:
    sections = json.load(f)
def process_sections_extract_prices(sections):
    for section in sections:
        # Join the body text if it's stored as a list
        body_text = " ".join(section["body"]) if isinstance(section["body"], list) else section["body"]
        # Find price patterns
        price_match = re.search(r'\$?(\d+(\.\d{1,2})?)', body_text)
        if price_match:
            # Update the section with the found price
            section["price"] = price_match.group(0)
            # Optionally, remove the price from the body text
            section["body"] = re.sub(r'\$?(\d+(\.\d{1,2})?)', '', body_text).strip()
        else:
            # If no price is found, you might want to handle this case (e.g., set price to None or a placeholder)
            section["price"] = None

    return sections

# Process the sections to extract prices and update the structure
processed_sections = process_sections_extract_prices(sections)

# Convert back to JSON to see the result or save it
processed_json = json.dumps(processed_sections, indent=4)
print(processed_json)

# Optionally, save the processed data back to a file
with open('processed_data_with_prices.json', 'w') as f:
    f.write(processed_json)
