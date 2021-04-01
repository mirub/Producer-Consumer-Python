Name: Miruna-Elena Banu

Group: 331CAa


# Homework 1

## Description

I chose to implement this solution because it is my first idea regading the problem. Initially, I wanted to use queues instead of lists for both the producer queue and the cart, because they are thread-safe, but I realised that I actually needed to remove a certain element and you cannot do so in queues, you can just pop the first element.

I also thought about using a deque but I am not familiar with the concept and I chose to play it safe.

I chose to implement the mutexes with Bounded Semaphore because it was a suggestion in the second lab that it can reproduce a pthreads mutex.

I believe that this project was useful since I certainly learnt more about both Python and multi-threading.

Implementation-wise, I certainly think that, had I started working on this project as early as I would have wanted, I could have come up with a better solution (see the deque comment I made above). However, I do not think that my solution is very inefficient either.


## Implementation

The current project represents an implementation for a producer-consumer problem that uses a marketplace as intermediary for both of the instances.

The producer implementation (*producer.py*) represents the producer thread, which continously creates products based on the given commands.

The consumer impementation (*consumer.py*) represents the consumer thread, which changes the carts by the commands given.

The marketplace implementation (*marketplace.py*) is responsible for the logic of the program. It handles every possible operation:
* **register_producer()**: creates an id and a queue for the current producer and returns the id
  
* **publish(producer_id, product)**: adds the product to the marketplace and to the producer queue
  
* **new_cart()**: initializes a new cart id and list and returns the id

* **add_to_cart(cart_id, product)**: adds the product to the cart and removes it from the marketplace and the producer queue

* **remove_from_cart(self, cart_id, product)**: removes the product from the cart and adds it to the marketplace and the producer queue

* **place_order(cart_id)**: returns the product list and prints the message

The project is fully implemented.

Something that I actually found interesting is the following difference:

```
        with self.producer_publish_mutex:
            if len(self.producer_queues[int(producer_id)]) >= self.max_queue_size:
                return False
```

versus 

```
        self.producer_publish_mutex.acquire()
            if len(self.producer_queues[int(producer_id)]) >= self.max_queue_size:
                return False
        self.producer_publish_mutex.release()
```

The first version actually handles the release of the mutex by itself after the return, whereas the second one creates a deadlock since upon return it cannot call the release.

## Resources

[1] https://ocw.cs.pub.ro/courses/asc/laboratoare/02

[2] https://web.archive.org/web/20201108091210/http://effbot.org/pyfaq/what-kinds-of-global-value-mutation-are-thread-safe.htm

[3] https://realpython.com/intro-to-python-threading/


## GIT

My git repository is private (for obvious reasons), however, I have added the .git folder to the uploaded archive. Nevertheless, here is the link to my repository:

https://github.com/mirub/Producer-Consumer-Python.git
