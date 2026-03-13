import pywhatkit as kit
import pandas as pd
import time
import random
import re

# 1. Load the message
try:
    with open("message.txt", "r", encoding="utf-8") as f:
        message_content = f.read()
except FileNotFoundError:
    print("Error: 'message.txt' not found. Please create it first.")
    exit()

# 2. Process the CSV
try:
    # Replace 'numbers.csv' with your actual filename
    df = pd.read_csv("numbers.csv")
    # Make sure we use the correct column name from your file
    column_name = 'Phone' 
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit()

def format_india_number(num):
    clean_num = re.sub(r'\D', '', str(num))
    if len(clean_num) == 12 and clean_num.startswith('91'):
        return f"+{clean_num}"
    if len(clean_num) == 10:
        return f"+91{clean_num}"
    if str(num).startswith('+'):
        return str(num)
    return f"+91{clean_num}"

# Apply formatting
numbers = df[column_name].apply(format_india_number).tolist()

print(f"Checking {len(numbers)} numbers. Starting the run...")

# 3. Execution Loop with Error Handling
for index, number in enumerate(numbers):
    try:
        print(f"--- Processing {index + 1}/{len(numbers)} ---")
        print(f"Sending to: {number}")
        
        # Send the message
        # wait_time is how long the tab stays open before clicking send
        kit.sendwhatmsg_instantly(
            phone_no=number,
            message=message_content,
            wait_time=25,      # Increased slightly for network reliability
            tab_close=True,
            close_time=5       # Gives the browser time to finish the send action
        )
        
        print(f"Success: Message queued for {number}")

        # 4. Anti-Ban Random Delay
        # Spacing out 110 messages is critical for account safety
        sleep_time = random.randint(50, 110)
        print(f"Sleeping for {sleep_time} seconds to avoid detection...")
        time.sleep(sleep_time)

    except Exception as e:
        # This block catches errors for a specific number and keeps the loop running
        print(f"!!! ERROR for {number}: {e}")
        print("Skipping to next number...")
        continue 

print("\nAll tasks completed. Check the terminal output above for any failed numbers.")