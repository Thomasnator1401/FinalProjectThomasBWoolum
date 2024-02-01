available_pizzas = ['margarita', 'pollo', '4cheese', 'bolognese', 'vegetarian']
available_toppings = ['mushroom', 'onions', 'green pepper', 'extra cheese']
pizza_prices = {'margarita': 5, 'pollo': 7, '4cheese': 6, 'bolognese': 8, 'vegetarian': 6.5}
topping_prices = {'mushroom':1, 'onions': 2, 'green pepper':3, 'extra cheese':4}

class PizzaOrder:
    def __init__(self, pizza, toppings, quantity):
        self.pizza = pizza
        self.toppings = toppings
        self.quantity = quantity
        self.price = self.calculate_price()

    def calculate_price(self):
        # calculate the price of the order based on the pizza and topping prices
        base_price = pizza_prices[self.pizza]
        toppings_price = sum([topping_prices[t] for t in self.toppings])
        total_price = (base_price + toppings_price) * self.quantity
        return total_price

def choose_pizza():
    # display the menu
    print("Please choose a pizza:")
    for i, pizza in enumerate(available_pizzas):
        print(f"{i+1}. {pizza} ${pizza_prices[pizza]}")
    # ask the user to enter a valid choice
    while True:
        choice = input("Enter the number of the pizza you want to order: ")
        try:
            choice = int(choice)
            if choice > 0 and choice <= len(available_pizzas):
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    # get the pizza name from the choice
    pizza = available_pizzas[choice-1]
    # ask the user to enter a valid quantity
    while True:
        quantity = input(f"How many {pizza} pizzas do you want to order? ")
        try:
            quantity = int(quantity)
            if quantity > 0:
                break
            else:
                print("Invalid quantity. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    # return the pizza and quantity as a tuple
    return (pizza, quantity)

def choose_toppings():
    # display the available toppings
    print("This is the list of available extra toppings: ")
    for i, topping in enumerate(available_toppings):
        print(f"{i+1}. {topping} ${topping_prices[topping]}")
    # ask the user to enter the numbers of the toppings they want, separated by commas
    toppings = []
    while True:
        choice = input("Enter the numbers of the toppings you want to add, separated by commas, or enter 0 to skip: ")
        try:
            choice = [int(c) for c in choice.split(",")]
            if choice == [0]:
                break
            elif all([c > 0 and c <= len(available_toppings) for c in choice]):
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")
    # get the topping names from the choice
    for c in choice:
        topping = available_toppings[c-1]
        toppings.append(topping)
    # return the toppings as a list
    return toppings

def confirm_order(order):
    # display the order summary
    print("Your order summary is:")
    print(f"Pizza: {order.pizza}")
    print(f"Toppings: {', '.join(order.toppings) if order.toppings else 'None'}")
    print(f"Quantity: {order.quantity}")
    print(f"Price: ${order.price}")
    # ask the user to confirm or cancel the order
    while True:
        choice = input("Do you want to confirm or cancel the order? Enter 'confirm' or 'cancel': ")
        if choice.lower() == 'confirm':
            return True
        elif choice.lower() == 'cancel':
            return False
        else:
            print("Invalid input. Please enter 'confirm' or 'cancel'.")

import stripe

# set your secret key
stripe.api_key = "sk_test_..."

def process_payment(order):
    # create a payment intent with the order amount and currency
    intent = stripe.PaymentIntent.create(
        amount=int(order.price * 100), # convert to cents
        currency='usd',
    )
    # display the payment link
    print(f"Please follow this link to complete the payment: {intent['next_action']['use_stripe_sdk']['stripe_js']}")

    # wait for the payment to be completed
    print("Waiting for payment confirmation...")
    while True:
        # retrieve the payment intent status
        intent = stripe.PaymentIntent.retrieve(intent['id'])
        if intent['status'] == 'succeeded':
            print("Payment successful!")
            return True
        elif intent['status'] == 'canceled':
            print("Payment canceled!")
            return False

def deliver_order(order):
    # display the delivery details
    print(f"Your order of {order.quantity} {order.pizza} pizza(s) with {', '.join(order.toppings) if order.toppings else 'no'} extra toppings will be delivered to your address in 30 minutes.")
    # thank the user for their order
    print("Thank you for choosing our pizza service. We hope you enjoy your meal!")

def main():
    # greet the user
    print("Hi, welcome to our text based pizza ordering service.")
    # choose a pizza and quantity
    pizza, quantity = choose_pizza()
    # choose extra toppings
    toppings = choose_toppings()
    # create a pizza order object
    order = PizzaOrder(pizza, toppings, quantity)
    # confirm the order
    if confirm_order(order):
        # process the payment
        if process_payment(order):
            # deliver the order
            deliver_order(order)
        else:
            # cancel the order
            print("Your order has been canceled.")
    else:
        # cancel the order
        print("Your order has been canceled.")
    # say goodbye
    print("Have a nice day!")

# run the program
main()


