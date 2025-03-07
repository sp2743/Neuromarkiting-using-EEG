import os
import pandas as pd
import re  # Import regex module

def combine_text_files_to_dataframe(text_directory, label_directory, default_label="Unknown"):
    data = []

    for filename in os.listdir(text_directory):
        if filename.endswith(".txt"):
            base_name = os.path.splitext(filename)[0]  # Extract filename without extension
            
            # Extract name (before first underscore) and product ID (last number in filename)
            parts = base_name.split("_")
            name_part = parts[0]  # First part before "_"
            
            # Extract the last numeric part as the product ID
            numbers = re.findall(r'\d+', base_name)  # Find all numbers in the filename
            product_id = numbers[-1] if numbers else "Unknown"  # Take the last number, if available

            filepath = os.path.join(text_directory, filename)
            label_filepath = os.path.join(label_directory, base_name + ".lab")  # Corresponding label file
            
            # Read label (single value for all rows in the file)
            label = default_label
            if os.path.exists(label_filepath):
                with open(label_filepath, 'r', encoding='utf-8') as lab_file:
                    label = lab_file.read().strip() or default_label  # Handle empty label file
            
            # Read and process text file
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    values = line.strip().split()  # Split by space
                    if values:  # Ensure line is not empty
                        values.insert(0, name_part)  # Add extracted name as first column
                        values.insert(1, product_id)  # Add product ID as second column
                        values.append(label)  # Append label
                        data.append(values)
    
    # Convert list to DataFrame
    df = pd.DataFrame(data)

    # Define column names
    if not df.empty:
        df.columns = ["name", "product"] + [f"feature_{i}" for i in range(df.shape[1] - 3)] + ["label"]

    return df

if __name__ == "__main__":
    text_directory = r"C:\Users\shasw\OneDrive\Desktop\EEG-Neuromarkiting-Project\Data\25-users"
    label_directory = r"C:\Users\shasw\OneDrive\Desktop\EEG-Neuromarkiting-Project\Data\labels"
    
    df = combine_text_files_to_dataframe(text_directory, label_directory)
    
    if not df.empty:
        print(df.head())  # Display first few rows
        df.to_csv("combined_text_files.csv", index=False)  # Save as CSV
    else:
        print("No data found or processed.")
