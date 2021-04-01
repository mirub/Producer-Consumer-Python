"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import BoundedSemaphore
import queue

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
        self.products = {}
        self.producer_q_sizes = []
        self.available_prod = []
        self.carts = {}
        self.num_prod = 0
        self.num_cart = 0

        self.producer_log_mutex = BoundedSemaphore(1)
        self.producer_cart_mutex = BoundedSemaphore(1)
        self.consumer_add_mutex = BoundedSemaphore(1)

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.producer_log_mutex.acquire()
        self.num_prod += 1
        new_id = self.num_prod
        self.producer_q_sizes.append(0)
        self.producer_log_mutex.release()

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
        if self.producer_q_sizes[int(producer_id)] >= self.max_queue_size:
            return False
        
        self.producer_q_sizes[int(producer_id)] += 1
        self.products[product] = producer_id
        self.available_prod.append(product)

        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.producer_cart_mutex.acquire()
        self.num_cart += 1
        self.carts[self.num_cart] = queue.Queue()
        self.producer_cart_mutex.release()

        return self.num_cart

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        self.consumer_add_mutex.acquire()
        if product in self.available_prod:
            self.producer_q_sizes[self.products[product]] -= 1
            self.available_prod.remove(product)
            self.carts[cart_id].put(product)
            return True
        self.consumer_add_mutex.release()

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        # We do not need a lock because Queue is thread-safe
        self.carts[cart_id].get(product)
        self.available_prod.append(product)
        self.producer_q_sizes[self.products[product]] += 1


    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        pass
