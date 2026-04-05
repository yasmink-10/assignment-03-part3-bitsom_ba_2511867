# Task 1 — File Read & Write Basics
# Part A
with open("python_notes.txt", "w", encoding="utf-8") as  f:
    f.write("Topic 1: Variables store data. Python is dynamically typed.\n")
    f.write("Topic 2: Lists are ordered and mutable.\n")
    f.write("Topic 3: Dictionaries store key-value pairs.\n")
    f.write("Topic 4: Loops automate repetitive tasks.\n")
    f.write("Topic 5: Exception handling prevents crashes.\n")
print("File written successfully.")
with open("python_notes.txt", "a", encoding="utf-8") as f:
    f.write("Topic 6: Tuples store multiple values in single variable.\n")
    f.write("Topic 7: Function is used to define dataset anytime & anywhere.\n")
print("Lines appended")

# Part B

with open("python_notes.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
print("\nFile Content:")

#print each line numbered

for i in range(len(lines)):
    line = lines[i].strip()
    print(f"{i+1}. {line}")

#counting total lines

print("\nTotal lines:", len(lines))

# Search using keyword

keyword = input("\nEnter keyword to search: "). lower()
found = False
for line in lines:
    if keyword in line.lower():
        print(line.strip())
        found = True
if not found:
    print("No matching lines found")

#Task 2 — API Integration

import requests
url = "https://dummyjson.com/products?limit=20"
# Step 1
response = requests.get(url)
data = response.json()

products = data["products"]

print("ID  | Title                          | Category      | Price    | Rating")
print("1   | iPhone 9                       | smartphones   | $549.99  | 4.69")

for p in products:
    print(f"{p['id']:<3} | {p['title'][:25]:<25} | {p['category']:<12} | ${p['price']:<7} | {p['rating']}")

# Step 2
filtered = []
for p in products:
    if p["rating"] >= 4.5:
        filtered.append(p)
# sort in descending price
filtered.sort(key=lambda x: x["price"], reverse=True)
print("\nFiltered (rating ≥ 4.5) & Sorted by price:\n")
for p in filtered:
    print(p["title"], "-", p["price"], "-", p["rating"])

# Step 3
print("\nLaptop Category:\n")
url2 = "https://dummyjson.com/products/category/laptops"
response2 = requests.get(url2)
data2 = response2.json()

for p in data2["products"]:
    print(p["title"], "-", p["price"])

# Step 4
print("\nPOST Request Response:\n")
new_product = {
  "title": "My Custom Product",
  "price": 999,
  "category": "electronics",
  "description": "A product I created via API"
}
post_url = "https://dummyjson.com/products/add"
response3 = requests.post(post_url, json=new_product)
data3 = response3.json()
print("Product Added:")
print("ID:", data3["id"])
print("Title:", data3["title"])
print("Price:",data3["price"])
print("Cateogory:", data3["category"])

#Task 3 — Exception Handling
#Part A
def safe_divide(a,b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"
print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("ten", 2))

#Part B
def read_file_safe(filename):
    try:
        with open(filename, "r", encoding ="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        print("File operation attempt complete.")
print(read_file_safe("python_notes.txt"))
print(read_file_safe("ghost_file.txt"))

#Part C
import requests
url = "https://dummyjson.com/products?limit=5"

try:
    response = requests.get(url, timeout=5)
    data = response.json()
    print(data)
except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet connection.")
except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")
except Exception as e:
    print("Error:", e)

# Part D
import requests
while True:
    user_input = input("Enter a product ID to look up (1–100), or 'quit' to exit: ")
    if user_input.lower() == "quit":
        break
    if not user_input.isdigit():
        print("Invalid input! Enter a Number.")
        continue
    product_id = int(user_input)
    if product_id < 1 or product_id> 100:
        print("Enter Id between 1 and 100.")
        continue
    try:
        url = f"https://dummyjson.com/products/{product_id}"
        response = requests.get(url, timeout=5)
        if response.status_code == 404:
            print("Product not found.")
        elif response.status_code == 200:
            data = response.json()
            print("Product:", data["title"], "-", data["price"])
    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet connection.")
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
    except Exception as e:
        print("Error:", e)

#Task 4 — Logging to File

import requests
from datetime import datetime

def log_error(function_name, error_type, message):
    with open("error_log.txt", "a", encoding="utf-8") as f:
        time = datetime.now().strftime("%Y-%m-%D %H:%M:%S")
        f.write(f"[{time}] ERROR in {function_name}: {error_type} - {message}\n")
try:
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except requests.exceptions.ConnectionError as e:
    log_error("fetch_products", "ConnectionError", str(e))
    print("Connection error logged.")

try:
    url = "https://dummyjson.com/products/000"
    response = requests.get(url, timeout=5)
    if response.status_code !=200:
        log_error("lookup_product", "HTTPError", f"{response.status_code} Not Found for product ID 000")
        print("HTTP error logged.")
except Exception as e:
    log_error("lookup_product", "Exception", str(e))

print("/nError log:\n")

with open("error_log.txt", "r", encoding="utf-8") as f:
    print(f.read())