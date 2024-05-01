import json
from datetime import datetime

class CryptoInvestment:
    def __init__(self):
        self.investments = {}

    def add_investment(self, crypto_name, pounds, amount, date):
        if crypto_name not in self.investments:
            self.investments[crypto_name] = []
        self.investments[crypto_name].append({"date": date, "pounds": pounds, "amount": amount})

    def calculate_profit(self, crypto_name, current_price):
        if crypto_name not in self.investments:
            return "No investments found for this cryptocurrency."

        total_pounds = 0
        for investment in self.investments[crypto_name]:
            total_pounds += investment["pounds"]

        current_value = sum(investment["amount"] * current_price for investment in self.investments[crypto_name])
        profit = current_value - total_pounds

        return profit

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.investments, file)

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            self.investments = json.load(file)

def main():
    crypto_investment = CryptoInvestment()

    while True:
        print("\n1. Add investment")
        print("2. Calculate profit")
        print("3. Save investments to file")
        print("4. Load investments from file")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            try:
                crypto_name = input("Enter the name of the cryptocurrency: ")
                pounds = float(input("Enter the amount you paid in pounds: "))
                amount = float(input("Enter the amount of crypto you own: "))
                date_str = input("Enter the date of investment (YYYY-MM-DD): ")
                date = datetime.strptime(date_str, "%Y-%m-%d")
                crypto_investment.add_investment(crypto_name, pounds, amount, date_str)
                print("Investment added successfully!")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif choice == "2":
            try:
                crypto_name = input("Enter the name of the cryptocurrency: ")
                current_price = float(input("Enter the current price of the crypto: "))
                profit = crypto_investment.calculate_profit(crypto_name, current_price)
                print(f"Your profit for {crypto_name} is: £{profit:.2f}")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif choice == "3":
            filename = input("Enter the filename to save investments to: ")
            crypto_investment.save_to_file(filename)
            print(f"Investments saved to {filename}")

        elif choice == "4":
            filename = input("Enter the filename to load investments from: ")
            crypto_investment.load_from_file(filename)
            print(f"Investments loaded from {filename}")

        elif choice == "5":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
