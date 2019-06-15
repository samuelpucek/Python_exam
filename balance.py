"""
Riešenie cieli na požiadavky "výborne"
"""

import sys
import json
import csv

try:
    # Read json file CUSTOMERS
    path_customers = sys.argv[1]
    file_customers = open(path_customers, encoding="utf-8")
    customers = json.load(file_customers)

    # Read csv file PAYMENTS
    path_payments = sys.argv[2]
    file_payments = open(path_payments)

    # Read csv file EXCHANGE
    path_exchange = sys.argv[3]
    file_exchange = open(path_exchange)

except IndexError as ex1:
    print("ERROR: Input file is missing")
    print(ex1)

except FileNotFoundError as ex2:
    print("ERROR: Input file was not found")
    print(ex2)

except json.decoder.JSONDecodeError as ex:
    print("ERROR: Input file is not readeble")
    print(ex)

else:
    # Close customers
    file_customers.close()

    # Read payments
    reader = csv.reader(file_payments)
    header = next(reader)
    payments = [row for row in reader]
    file_payments.close()

    # Read exchange
    # save it into dictionary for a good access
    exchange_rate = {}
    for line in file_exchange:
        split_line = line.split()
        exchange_rate[split_line[0]] = float(split_line[2])
    file_exchange.close()

    for i in range(len(header)):
        if header[i] == "vs":
            index_vs = i
        elif header[i] == "timestamp":
            index_timestamp = i
        elif header[i] == "account_no":
            index_account_no = i
        elif header[i] == "bank":
            index_bank = i
        elif header[i] == "amount":
            index_amount = i
        elif header[i] == "currency":
            index_currency = i

    print("BEFORE")
    for cust in customers:
        print(cust["id"], "\t", cust["name"], "\t",  cust["surname"], "\t\t", cust["balance_czk"], "CZK", "\t\t", cust["last_payment"])

    print()
    print(80 * "=")
    print()

    # Lets start accounting
    try:
        # Check format of file PAYMENTS
        # Some columns might be missing....
        for pay in payments:
            pay_vs = int(pay[index_vs])
            pay_timestamp = int(pay[index_timestamp])
            pay_amount = float(pay[index_amount])
            pay_currency = pay[index_currency]
            customer_exists = False

            for cust in customers:
                if cust["id"] == pay_vs:
                    customer_exists = True
                    if (cust["last_payment"] is None) or (cust["last_payment"] < pay_timestamp):
                        if pay_currency == "CZK":
                            cust["last_payment"] = pay_timestamp
                            cust["balance_czk"] += pay_amount
                        else:
                            # First try, if currency is in our exchange_rate dictionary
                            try:
                                pay_amount *= exchange_rate[pay_currency]
                            except KeyError as ex3:
                                print("Currency", ex3, "is not acceptable")
                                print("Payment failed: ", pay_vs, "/", pay_account_no, pay_bank, "/", pay_amount, pay_currency)
                            else:
                                cust["last_payment"] = pay_timestamp
                                cust["balance_czk"] += pay_amount
                        break

            # No pair between payment and customer database
            if not customer_exists:
                pay_account_no = pay[index_account_no]
                pay_bank = pay[index_bank]
                print("Customer with id", pay_vs, "does not exist")
                print("Payment failed: ", pay_vs, "/",pay_account_no, pay_bank, "/", pay_amount, pay_currency)

        print()
        print(80 * "=")
        print()

        print("AFTER")
        for cust in customers:
            print(cust["id"], "\t", cust["name"], "\t",  cust["surname"], "\t\t", cust["balance_czk"], "CZK", "\t\t", cust["last_payment"])

    except NameError as ex:
        print("ERROR: File PAYMENTS is in wrong format")
