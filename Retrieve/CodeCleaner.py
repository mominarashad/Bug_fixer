import pandas as pd
import re
import nltk
import os

# Downloads only once
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Load Excel
input_path = "Sheharyar 2 with description.xlsx"
output_path = "ultra_refined_descriptions.xlsx"

df = pd.read_excel(input_path, sheet_name="Tickets")

# Refiner
def ultra_refine(text):
    if pd.isna(text) or not isinstance(text, str):
        return ""
    
    text = text.lower()
    sentences = sent_tokenize(text)
    text = ' '.join(sentences[:2])
    text = re.sub(r"[^\w\s]", "", text)

    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered = [word for word in words if word not in stop_words]

    return ' '.join(filtered)

# Apply and add new column
df["Detailed Description"] = df["Detailed Description"].apply(ultra_refine)

# Save using openpyxl
df.to_excel(output_path, index=False, engine='openpyxl')

# Confirm save
if os.path.exists(output_path):
    print(f" File saved as: {output_path}")
else:
    print(" Save failed.")
