import random
import time

from datetime import datetime, timedelta
from factories import CustomerFactory, OrderCreateFactory, get_random_number_with_dist
from models import OrderLineItemCreate, Customer, Address

from shopify_utils import publish, get_all_resources
import shopify


num_orders = 100
products = get_all_resources(shopify.Product)
customers = get_all_resources(shopify.Customer)

end = datetime.now()
start = end - timedelta(days=100)

for _ in range(num_orders):
    try:
        line_items = []

        for _ in range(get_random_number_with_dist(4, [0.5, 0.25, 0.15, 0.1])):
            random_product = random.choice(products)
            random_variant = random.choice(random_product.variants)
            line_item = OrderLineItemCreate(
                title=random_variant.title,
                variant_id=random_variant.id,
                quantity=get_random_number_with_dist(4, [0.5, 0.25, 0.15, 0.1]),
                price=float(random_variant.price)
            )
            line_items.append(line_item)

        if random.random() > 0.8:
            random_customer = CustomerFactory()
        else:
            random_customer = random.choice(customers)
            try:
                default_address = Address.from_kwargs(**random_customer.default_address.to_dict())
            except AttributeError:
                default_address = Address.from_kwargs(**random_customer.default_address.__dict__)
            random_customer.default_address = default_address
            random_customer.addresses = [random_customer.default_address]
            random_customer = Customer(**random_customer.to_dict())

        random_date = start + (end - start) * random.random()
        fulfillment_status = "fulfilled"
        financial_status = "paid"

        if random.random() > 0.9:
            random_date = end - timedelta(days=7) + timedelta(days=7) * random.random()
            fulfillment_status = None
            if random_date >= end - timedelta(days=1) and random.random() > 0.5:
                financial_status = 'pending'
        elif random.random() > 0.8:
            fulfillment_status = None
            financial_status = 'refunded'

        random_order = OrderCreateFactory(
            customer=random_customer,
            line_items=line_items,
            processed_at=random_date.isoformat(),
            tags='first-run', fulfillment_status=fulfillment_status, financial_status=financial_status)

        upstream_order = publish(random_order, shopify.Order)
    except Exception as e:
        raise e
        print("Unable to create order", e)

    time.sleep(15)
