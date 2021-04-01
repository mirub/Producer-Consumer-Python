"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.produced_goods = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.producer_id = self.marketplace.register_producer()

    def run(self):
        while 1:
            for i in range(len(self.produced_goods)):
                # Get the goods and their paratmeters
                (prod, quantity, waiting_time) = self.produced_goods[i]
                j = 0
                while j < quantity:
                    # Produce the goods
                    check = self.marketplace.publish(str(self.producer_id), prod)
                    if not check:
                        # If the product could not be published
                        time.sleep(self.republish_wait_time)
                    else:
                        # Wait before producing another item
                        time.sleep(waiting_time)
                        j += 1
