import csv
import json
import os

def generate_bank_mapping_json(csv_file_path, provider_name):
    # Initialize an empty dictionary to store the mapping
    bank_mapping = {}
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            # Create a CSV reader
            csv_reader = csv.DictReader(file)
            
            # Iterate through each row in the CSV
            for row in csv_reader:
                # Get the bank code and raffles pay mapping code
                bank_code = row['code']
                raffles_pay_code = row[provider_name]
                
                # Only add to the mapping if raffles pay code exists
                if raffles_pay_code and raffles_pay_code.strip():
                    bank_mapping[bank_code] = raffles_pay_code
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}, skipping...")
    except Exception as e:
        print(f"Error processing file {csv_file_path}: {e}")
    
    # Convert the dictionary to a JSON string
    return json.dumps(bank_mapping)  # 確保總是返回JSON字符串

# Example usage
if __name__ == "__main__":
    server_arr = ["lx1","lx2","cm2","cm4","cm7","cmnaga"]
    provider_arr = ["midas","raffles","viprqris"]
    for servername in server_arr:
        for providername in provider_arr:
            # Replace with the path to your CSV file
            csv_file_path = f"Bank list - {servername} {providername}.csv"
            # Generate the JSON
            json_result = generate_bank_mapping_json(csv_file_path, providername)
            
            # Print the JSON
            print(json_result)
            
            # Optionally, save the JSON to a file
            # Replace "bank_mapping.json" with the desired file name
            # Replace "utf-8" with the desired encoding
            json_file_name = f"{servername}_{providername}_bank_mapping.json"
            json_encoding = "utf-8"
            
            if json_result=="{}":
                print(f"No valid mappings found for {csv_file_path}, skipping file save.")
                continue
            with open(json_file_name, "w", encoding=json_encoding) as json_file:
                json_file.write(json_result)
                print(f"JSON has been saved to {json_file_name}")