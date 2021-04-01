"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def execute_operation(self, operation, cart_id, product):
        """
        Auxiliary function to execute add or remove

        :type operation: String
        :param operation: the operation to be executed

        :type cart_id: Int
        :param cart_id: the id of the cart

        :type product: product
        :param: the product to be changed
        """
        if operation == "add":
            return (self.marketplace.add_to_cart(cart_id, product), 1)
        return (self.marketplace.remove_from_cart(cart_id, product), 0)

    def run(self):
        # Get the first cart
        for entry in self.carts:
            # Allocate an id for the current cart
            cart_id = self.marketplace.new_cart()
            for current_cart in entry:
                j = 0
                # Get the parameters to execute the instructions
                (instruc, product, quantity) = tuple(current_cart.values())
                while j < quantity:
                    (check, cond) = self.execute_operation(instruc, cart_id, product)
                    if cond == 1 and not check:
                        # If the operation is add and it fails, wait
                        time.sleep(self.retry_wait_time)
                    else:
                        j += 1
            # PLace the order
            self.marketplace.place_order(cart_id)
