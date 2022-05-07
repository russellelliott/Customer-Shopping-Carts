import csv #for csv files
import os #exists to get current working directory
from loguru import logger #for log statements
from pathlib import Path
from send_email import send_email

current_dir = os.getcwd() #current working directory

def generate_email(recieved_contents):
    #recieved contents; specific info to change
    #in this case, recieved_contents is a dicitonary
    default = "-" #default in case variables are missing or incorrect
    expected_content = dict.fromkeys(["customer_name", "product", "mssg", "amount"], default) #content expected to recieve; dicitonary
    
    for content in expected_content:
        if content in recieved_contents:
            #if there is content, add it to corresponding recieving content
            expected_content[content] = recieved_contents[content]
        else:
            #no content found. log warning message and use default parameter for that data
            logger.warning(f"The value for {content} was not passed to write failure email. Default value {default} will be used.")
    
    #once you have contents you need, get email path
    email_template_path = Path(current_dir+"/templates/email_template.html") #get the email template html from file structure
    print(email_template_path) #print path for debugging purposes
    
    #check if path exists at locaiton you defined, and its a file
    if email_template_path.exists() and email_template_path.is_file:
        with open(str(email_template_path), "r") as message:
            html = message.read().format(**expected_content) #replace stuff in brackets in html for each of content types
    else:
        #If path doesn't exist
        logger.critical("email_template_path does not exist. Dumping expected content as string into email.")
        html = f"Error: email_template_path was not set or does not exist. Dumping email content as a string:<br/>{expected_content}"
    
    return html #return html message

#functions to loop through csv files
def search_customer_lists():
    customer_dir = current_dir+"/CSV_material_generator/customer_carts"
    inventory_file = current_dir+"/CSV_material_generator/inventory_items.csv"
    
    low_stock = {} #Dictionary of items that are low in stock
    no_stock = {} #Dictionary of items that are out of stock
    
    inventory_file = open(inventory_file, "r")
    inventory_reader = csv.reader(inventory_file, delimiter = ",")
    for row in inventory_reader:
        if "Amount" in row[1]: #Header of the row
            continue
        elif int(row[1])==0:
            no_stock[row[0]]=row[1]
        elif int(row[1])<=15:
            low_stock[row[0]] = row[1]
            
    filenames = os.listdir(customer_dir)
    for file_name in filenames:
        #Make sure the file in quesiton is a csv file
        if file_name.endswith("csv"):
            #generates list of files within specific directory
            file = open(os.path.join(customer_dir, file_name), "r")
            reader = csv.reader(file, delimiter = ",")
            for row in reader:
                print(row)
                if row[0] in no_stock: #if item out of stock
                    send_no_stock_email("Andy", row[0], no_stock[row[0]]) #send email indicating the item is out of stock
                elif row[0] in low_stock: #if item low in stock
                    send_low_stock_email("Andy", row[0], low_stock[row[0]]) #send email indicating the item is low in stock
    
def send_low_stock_email(cust_name, product, amount):
    mssg = "If you would still like to purchase this item, please proceed to your shopping card and continue with your purchase."
    email_contents = {
        "customer_name": cust_name,
        "product": product,
        "mssg": mssg,
        "amount": amount
    }
    
    body = generate_email(email_contents)
    send_email(body=body, subject="Warning! Low stock left for item in your cart!", files = [])

def send_no_stock_email(cust_name, product, amount):
    mssg = "The item has been removed from your card as it is no longer available and is out of stock."
    email_contents = {
        "customer_name": cust_name,
        "product": product,
        "mssg": mssg,
        "amount": amount
    }
    
    body = generate_email(email_contents)
    send_email(body=body, subject="Warning! No stock left for item in your cart!", files = [])

if __name__ == "__main__":
    search_customer_lists()
    