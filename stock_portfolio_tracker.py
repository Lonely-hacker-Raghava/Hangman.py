"""
Stock Portfolio Performance Tracker
Datheon Python Programming Internship - Task 2

Tracks holdings using prices entered by the user. It does not fetch live prices.
"""

def positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("Enter a number greater than zero.")
        except ValueError:
            print("Invalid number. Try again.")

def positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Enter a whole number greater than zero.")
        except ValueError:
            print("Invalid quantity. Try again.")

def add_stock(portfolio):
    symbol = input("Stock symbol (e.g. AAPL): ").strip().upper()
    if not symbol or not symbol.isalnum():
        print("Enter a valid stock symbol.")
        return

    quantity = positive_int("Number of shares: ")
    price = positive_float("Purchase price per share: ")

    if symbol in portfolio:
        old = portfolio[symbol]
        total_quantity = old["quantity"] + quantity
        total_cost = old["quantity"] * old["purchase_price"] + quantity * price
        old["quantity"] = total_quantity
        old["purchase_price"] = total_cost / total_quantity
    else:
        portfolio[symbol] = {"quantity": quantity, "purchase_price": price}
    print(f"{symbol} holding saved.")

def view_portfolio(portfolio):
    if not portfolio:
        print("Your portfolio is empty.")
        return

    print("\n--- YOUR PORTFOLIO ---")
    print(f"{'Symbol':<12}{'Shares':>10}{'Avg Cost':>14}{'Total Cost':>16}")
    total_cost = 0.0
    for symbol, stock in sorted(portfolio.items()):
        cost = stock["quantity"] * stock["purchase_price"]
        total_cost += cost
        print(f"{symbol:<12}{stock['quantity']:>10}{stock['purchase_price']:>14.2f}{cost:>16.2f}")
    print(f"Total cost basis: {total_cost:.2f}")

def calculate_performance(portfolio):
    if not portfolio:
        print("Your portfolio is empty. Add a stock first.")
        return

    total_cost = 0.0
    total_value = 0.0
    print("\nEnter current prices manually (these are not live market prices).")
    print(f"{'Symbol':<10}{'Cost Basis':>14}{'Current Value':>17}{'Profit/Loss':>15}")

    for symbol, stock in sorted(portfolio.items()):
        cost = stock["quantity"] * stock["purchase_price"]
        current_price = positive_float(f"Current price for {symbol}: ")
        value = stock["quantity"] * current_price
        profit_loss = value - cost
        total_cost += cost
        total_value += value
        print(f"{symbol:<10}{cost:>14.2f}{value:>17.2f}{profit_loss:>15.2f}")

    overall_pl = total_value - total_cost
    percentage = overall_pl / total_cost * 100 if total_cost else 0
    print("-" * 56)
    print(f"Total cost basis: {total_cost:.2f}")
    print(f"Current portfolio value: {total_value:.2f}")
    print(f"Overall profit/loss: {overall_pl:.2f} ({percentage:.2f}%)")

def main():
    portfolio = {}
    while True:
        print("\n=== STOCK PORTFOLIO TRACKER ===")
        print("1. Add stock holding")
        print("2. View portfolio")
        print("3. Calculate performance")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_stock(portfolio)
        elif choice == "2":
            view_portfolio(portfolio)
        elif choice == "3":
            calculate_performance(portfolio)
        elif choice == "4":
            print("Thanks for using Stock Portfolio Tracker!")
            break
        else:
            print("Invalid choice. Select 1, 2, 3, or 4.")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed. Goodbye!")
