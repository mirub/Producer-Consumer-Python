"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import BoundedSemaphore, currentThread

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.max_queue_size = queue_size_per_producer
        # Correlate (product, producer_id)
        self.products = {}
        # Correlate (producer_id, [products])
        self.producer_queues = {}
        # All the available products in the marketplace
        self.available_prod = []
        # Correlate (cart_id, [cart_products])
        self.carts = {}
        # Number of producers
        self.num_prod = 0
        # Number of carts
        self.num_cart = 0

        # Mutexes implemented with BoundedSmaphore
        self.producer_log_mutex = BoundedSemaphore(1)
        self.producer_publish_mutex = BoundedSemaphore(1)
        self.producer_cart_mutex = BoundedSemaphore(1)
        self.consumer_add_mutex = BoundedSemaphore(1)
        self.consumer_order_mutex = BoundedSemaphore(1)

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.producer_log_mutex:
            # Using mutex to safely increment a value
            self.num_prod += 1
            new_id = self.num_prod

        # Initialize a queue for the new producer
        self.producer_queues[new_id] = []
        return new_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # If there are too many products in the queue
        with self.producer_publish_mutex:
            if len(self.producer_queues[int(producer_id)]) >= self.max_queue_size:
                return False

            # Add the product to the prod queues and available_prod
            self.producer_queues[int(producer_id)].append(product)
            self.products[product] = int(producer_id)
            self.available_prod.append(product)

        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """

        with self.producer_cart_mutex:
            # Using mutex to safely increment cart number
            self.num_cart += 1
            new_cart = self.num_cart

        # Initialize a queue for the new cart
        self.carts[self.num_cart] = []

        return new_cart

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        with self.consumer_add_mutex:
            if product in self.available_prod:
                # Remove the product from producer queue and available products
                self.available_prod.remove(product)

                for (producer, p_list) in self.producer_queues.items():
                    # Remove the product from the producer's queue
                    if product in p_list:
                        self.producer_queues[producer].remove(product)
                        self.products[product] = producer
                        break

            # Add the product to the cart
            self.carts[cart_id].append(product)
            return True

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        # Remove the product from cart
        if product in self.carts[cart_id]:
            self.carts[cart_id].remove(product)
            self.available_prod.append(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        # Get the cart products
        order_list = self.carts[cart_id]
        # Remove the cart list from the cart map
        self.carts.pop(cart_id)
        for product in order_list:
            # Mutex to print the messages correctly
            with self.consumer_order_mutex:
                print(f"{currentThread().getName()} bought {product}")
        return order_list
