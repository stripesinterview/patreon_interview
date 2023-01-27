"""
Question Description
We want to protect an API endpoint with an in-memory rate limiter.
The rate limiter should be initialized with a value that represents the maximum requests
per second we want to allow. When a request hits the endpoint, the rate limiter is
asked whether it has capacity to process this request and will reject or accept the request appropriately.

Assume:
_ Time is measured in millisecond resolution
- API requests come in sequentially

Design the interface and implement the logic for the rate limiter.

Example at a max of 2 requests/sec:
12:00:01.100 PASS
12:00:01.200 PASS
12:00:01.300 FAIL
12:00:02.100 PASS
12:00:02.150 FAIL
12:00:02.200 PASS 
"""
from collections import deque as queue
class Bucket:
    def __init__(self, window_size_ms, max_requests_per_window):
        self.window_size_ms = window_size_ms
        self.max_requests_per_window = max_requests_per_window
        self.current_num_requests_in_window = 0
        self.queue = queue([])

    def submit_request(self, timestamp_ms):
        if self.queue:
            last_time_stamp = self.queue[0]
            time_diff = timestamp_ms - last_time_stamp

            if time_diff >= self.window_size_ms:
                self.current_num_requests_in_window -= 1
                self.queue.popleft()
         
        if self.current_num_requests_in_window < self.max_requests_per_window:
            self.queue.append(timestamp_ms)
            self.current_num_requests_in_window += 1
            return True
        return False

def test():
    bucket = Bucket(1000, 2)
    for timestamp in (1100, 1200, 1300, 2100, 2150, 2200):
        print(timestamp, bucket.submit_request(timestamp))


# Follow ups:
# 1. What if you have lots of users with different user ids? How do you handle their limits?
## Map<userId, bucket>
# 2. What if you want to weight the requests, what do you do?
## Change the weight in submitRequest
# 3. What if you have a distributed system? How do you manage the rate limiter?
## Use a cache like Redis, potentially backed by a DB. Use SQL for consistency, NOSQL
## if consistency isn't a must.


def cd(current, new):
    current = current.strip("/")
    path_so_far = [] if (current == "") else current.split("/")
    parts = new.split("/")
    for part in parts:
        if not part:
            continue
        if part == "..":
            if path_so_far:
                path_so_far.pop()
        elif part == ".":
            continue
        else:
            path_so_far.append(part)
    result = "/".join(path_so_far)
    return "/" + result

# Test cases:
current = "/"
new = "a"
output = "/a"

current = "/b"
new = "c"
output = "/b/c"

current = "/d"
new = "/e"
output = "/e"

current = "/foo/bar"
new = ".."
output = "/foo"

current = "/r/s"
new = "../p/q"
output = "/r/p/q"

current = "/x/y"
new = "p/./q"
output = "/x/y/p/q"



"""
You're building a shopping cart pricer app for
your local grocery store. They sell many types of
items and accept coupons. One type of coupon
discounts an item's price by a percentage (e.g.
10% off). Another tybe of coupon gives the
shopper a dollar amount discount if a minimum
count of the item is purchased (e.g. $5 off if you
buy 2 or more). A shopper may only use one coupon on a type of item. 
The app should compute the price given a shopping cart and 
a set of coupons applied.

Keep in mind the grocery store is planning to
accept new types of coupons next quarter but 
you don't yet know the details of those.

Given this information. design the interface(s)
and data model to represent the shopping cart,
implement the shopping cart pricer, and test
your code. 

As an example, a shopping cart has 10 apples ($1
each). 2 loaves of bread $5 each, and 1
chocolate ($1 each).

The shopper has two coupons 10%-off apples and 
$4 off it you buy 2 or more loaves of bread. The 
pricer should return $16
"""

# Happy path test case

# Write a test for computing the best price of a cart when you 
# have multiple coupons on the same item

# A test for when you remove an item from the cart.

# A test for adding an item with a negative price

# Discuss a broader variety of coupons, like coupons that 
# apply when you have multiple different items with minimum
# quantities


# Code the cart to assume that the most recent coupon for an item
# is the one that will be used.

# Then change the code to accept all coupons for an item and compute
# which discount would be the best for the item.

from collections import defaultdict

ITEM_TO_UNIT_PRICE = {
    "apples" : 100,
    "bread": 500,
    "chocolate": 100
}

class PercentCoupon(object):

    def __init__(self, item_name, discount_percent):
        self.name = item_name
        self.discount_percent = discount_percent
    
    def discount_amount(self, cart) -> int:
        quantity = cart.get(self.name, 0)
        unit_price = ITEM_TO_UNIT_PRICE[self.name]
        return (quantity * unit_price * self.discount_percent) // 100

class DollarAmountCoupon(object):
    
    def __init__(self, item_name, min_quantity, discount):
        self.name = item_name
        self.min_quantity = min_quantity
        self.discount = discount
    
    def discount_amount(self, cart) -> int:
        quantity = cart.get(self.name, 0)
        if quantity >= self.min_quantity:
            return self.discount
        return 0

class Cart(object):

    def __init__(self):
        self.item_to_quantity = defaultdict(int)
        self.item_to_coupons = defaultdict(list)
    
    def add_item(self, item_name, quantity) -> None:
        self.item_to_quantity[item_name] += quantity
    
    def add_coupon(self, coupon) -> None:
        # Change this code depending on which version of the coupon
        # system the interviewer wants you to use
        self.item_to_coupons[coupon.name].append(coupon)
    
    def checkout(self) -> int:
        total = 0
        for item_name, quantity in self.item_to_quantity:
            price = quantity * ITEM_TO_UNIT_PRICE[item_name]
            best_discount = 0
            for coupon in self.item_to_coupons[item_name]:
                best_discount = max(
                    best_discount, 
                    coupon.discount_amount(self.item_to_quantity)
                )
            total += price - best_discount
        return total

