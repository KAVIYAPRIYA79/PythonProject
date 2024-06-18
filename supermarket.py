import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import re

#gst calculation
def calculate_gst(bill_amount, gst_amount=0.18):
    """Calculates the GST for a given bill amount."""
    return bill_amount * gst_amount

#sending mail
def send_email(to_email, subject, body):
    """Sends an email with the specified subject and body to the given email address."""
    from_email = "youremail@1234.com"
    from_password = "yourpassword"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        print(f"Email sent successfully to {to_email}!")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Failed to send email: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server.quit()

def is_valid_email(email):
    """Validates the email format."""
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    return re.match(regex, email)

def get_user_input():
    """Gets user input for name and email with validation."""
    name = input("Enter your name: ")
    email = input("Enter your email ID: ")
    while not is_valid_email(email):
        print("Invalid email format. Please enter a valid email ID.")
        email = input("Enter your email ID: ")
    return name, email

def get_products():
    """Gets the list of products and their prices from the user."""
    products = []
    final_amount = 0.0
    while True:
        product_name = input("Enter product name (or 'done' to finish): ")
        if product_name.lower() == 'done':
            break
        try:
            product_price = float(input(f"Enter price for {product_name}: "))
            if product_price < 0:
                raise ValueError("Price cannot be negative.")
            products.append((product_name, product_price))
            final_amount += product_price
        except ValueError as ve:
            print(f"Invalid price: {ve}")
    return products, final_amount

def create_bill_details(name, email, products, final_amount):
    """Creates the bill details string."""
    gst_amount = calculate_gst(final_amount)
    total_bill = final_amount + gst_amount

    current_datetime = datetime.datetime.now()
    date_str = current_datetime.strftime("%Y-%m-%d")
    time_str = current_datetime.strftime("%H:%M:%S")

    bill_details = (
        f"--- Bill Details ---\n"
        f"Name: {name}\n"
        f"Email ID: {email}\n"
        f"Date: {date_str}\n"
        f"Time: {time_str}\n"
        f"Products Purchased:\n"
    )
    for product, price in products:
        bill_details += f"- {product}: {price:.2f}\n"
    bill_details += (
        f"\nTotal Amount: {final_amount:.2f}\n"
        f"GST (18%): {gst_amount:.2f}\n"
        f"Total Bill: {total_bill:.2f}\n"
        "---------------------"
    )
    return bill_details

def main(): 
    
    """Main function to run the bill generation and email sending process."""
    name, email = get_user_input()
    products, final_amount = get_products()
    bill_details = create_bill_details(name, email, products, final_amount)
    print(bill_details)
    send_email(email, "Your supermarket purchase Bill", bill_details)
    print("your billing is over!")

if __name__ == "__main__":
    main()
