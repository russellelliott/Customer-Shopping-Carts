# Customer Shopping Carts
Headstarter Spring Fellowship Week 1 Sample Project

## Functionality
This program sends an email to customers if they have an item in their cart that is low in stock or out of stock. An item is out of stock if it has a quantity of 0. An item is low in stock if it has a quantity less than or equal to 15.

## Program Library Information
The sample project and my program uses the library smtplib. This library uses the SMTP protocol to send emails. To use this program to send emails from a Gmail account, a setting must be changed in your Google account.
Go into your Google Account’s security settings and turn on [“Enable Less Secure Apps”](https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4N6IDE0TUlrohDkGGugp7KdT9rkm00XVjREzmsX79duDzTD_m56zDUtnIPEZAFD4yNoF7WEjJstM2gDMo9Oo59Ca3TrCQ). This will enable the program to work properly.
Note: Google will be disabling less secure app access on May 30, 2022. The program may be affected by this.

## Running the Program
To run the program, clone this repository and open it. From there, run the file `generate_email.py`. If items out of stock are detected in the user's cart, an email will be sent out to the user for each item out of stock in their cart. Similarly, if items low in stock are detected in the user's cart, an email will be sent out to the user for each of those. If no items low in stock or out of stock are detected in the shopping cart, no email pertaining to that customer will be sent.

## Files
### generate_email.py
Parses through the carts and finds items low in stock or out of stock. If any of such items are found, an email will be sent to the customer for each item low in stock or out of stock.

### send_email.py
Sends each of the individual emails generated.

### .env
Contains the environment variables neccesary for the program. They are:
- `EMAIL_USER`: The email you are sending it from
- `EMAIL_PASS`: The password to the email account you are sending the emails from
- `EMAIL_RECIEVE`: The person(s) to recieve emails. Represented as a "," delimited string.
    - For multiple emails, seperate them with commas
- `EMAIL_CC`: Secondary recipients of the emails. Represented as a "," delimited string.
    - For multiple emails, seperate them with commas
    - This field is left blank in the repo, as I had no need for it in the implementation.
    - If you wish to utilize CC emails on your end, do the following:
        - modify line 13 of `send_email.py` to :`CC_EMAILS = os.environ.get("EMAIL_CC")`
        - Add email(s) in quotes to the EMAIL_CC environment varaible in the `.env` file

The `.env` file should look something like this. There should be no spaces between the varaible name, the equal sign, and the value of the varaible (all strings in quotes). The variables themselves are just normal strings. They can have spaces.

`EMAIL_USER="email@domain.com"`
`EMAIL_PASS="p@$$w0rd"`
`EMAIL_RECIEVE="another@domain.com"`
- For multiple emails: `EMAIL_RECIEVE="another@domain.com, third@domain..com, ..., etc"`

`EMAIL_CC="somebody@domain.com"`
- For multiple emails: `EMAIL_CC="somebody@domain.com, third@domain.com, ..., etc"`

### .gitignore
File that prevents files of a given type from being pushed. Used to prevent the `.env` file from being pushed onto a git repo or otherwise being visible to others. Also prevents `.DS_Store` files (appear when you open a folder in MacOS) from being pushed

### email_template.html
Email template for the emails sent out from the program. The fields in the email correspond to a varaible in the program.

### inventory_items.csv
A list of inventory items, their quantities, and prices.