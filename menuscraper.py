import fitz  # PyMuPDF
import json

def extract_sections_to_json(pdf_path, header_font_min, header_font_max):
    doc = fitz.open(pdf_path)
    sections = []
    current_section = None

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if header_font_min <= span["size"] <= header_font_max:
                            # New header found, start a new section
                            if current_section:  # Save the previous section before starting a new one
                                sections.append(current_section)
                            current_section = {"header": text, "body": []}
                        elif current_section:  # Add text to the body of the current section
                            current_section["body"].append(text)
                        # If text doesn't qualify as a header or body (or we haven't started a section), ignore it

    # Append the last section if it exists
    if current_section:
        sections.append(current_section)

    # Convert the sections list to JSON
    json_output = json.dumps(sections, indent=4)
    return json_output

# Adjust these values based on your observations of the font sizes
header_font_min = 17.5  # Minimum font size to consider as header
header_font_max = 18.5  # Maximum font size to consider as header

pdf_path = 'menuu.pdf'  # Update with your PDF path
json_data = extract_sections_to_json(pdf_path, header_font_min, header_font_max)

# Print the JSON data
print(json_data)

# Optionally, save the JSON data to a file
json_file_path = 'extracted_data.json'
with open(json_file_path, 'w') as f:
    f.write(json_data)
