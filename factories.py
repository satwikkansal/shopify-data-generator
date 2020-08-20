import random

from models import Address, Customer, OrderCreate, OrderLineItemCreate

from factory import Faker, Factory, Sequence, SubFactory, SelfAttribute, LazyAttribute
from faker_e164.providers import E164Provider
import pandas as pd
import numpy as np


Faker.add_provider(E164Provider)

postal_df = pd.read_csv("zip-codes.csv", header=None, converters={0: lambda x: str(x)})
postal_df.columns = ["postal_code", "lat", "long", "city", "state", "county", "unique"]
# State abbreviations to remove. Shopify does not recognize these states.
# From: US District, Territory, and Possession Abbreviations and Capitals
# http://www.stateabbreviations.us/
for state in ['AS', 'DC', 'FM', 'GU', 'MH', 'MP', 'PW', 'PR', 'VI']:
    postal_df = postal_df[postal_df.state != state]


def get_random_number_with_dist(
        end, dist, start=1):
    return np.random.choice(np.arange(start, end+1), p=dist)


class AddressFactory(Factory):
    class Meta:
        model = Address

    _state_info = postal_df.sample(n=1)
    id = Sequence(lambda n: n)
    customer_id = ''
    default = True
    name = "Home"
    first_name = ""
    last_name = ""
    company = Faker("company")
    address1 = Faker("street_address")
    address2 = ''
    city = Faker("city")
    province = _state_info.iloc[0]['state']
    country = 'US'
    zip = _state_info.iloc[0]['postal_code']
    phone = ''
    province_code = _state_info.iloc[0]['state']
    country_code = 'US'
    country_name = 'United States'


class CustomerFactory(Factory):
    class Meta:
        model = Customer

    _start_date = '-2years'

    _state_values = 'disabled,invited,enabled,declined'.split(',')
    _opt_in_levels = 'single_opt_in,confirmed_opt_in,unknown'.split(',')

    accepts_marketing = Faker("pybool")
    accepts_marketing_updated_at = Faker("date_time_between", start_date=_start_date)
    currency = Faker("currency_code")
    created_at = Faker("date_time_between", start_date=_start_date)
    default_address = SubFactory(
        AddressFactory,
        customer_id=SelfAttribute('..id'),
        first_name=SelfAttribute('..first_name'),
        last_name=SelfAttribute('..last_name'), phone=SelfAttribute('..phone')
    )
    addresses = LazyAttribute(lambda o: [o.default_address])
    email = Faker("safe_email")
    first_name = Faker("first_name")
    id = Sequence(lambda n: n)
    last_name = Faker("last_name")
    last_order_id = Faker("random_int")
    last_order_name = ''
    orders_count = 0  # To be incremented with actual orders
    state = Faker('random_element', elements=_state_values)  # can be disabled, invited, enabled, declined
    tags = ''
    tax_exempt = Faker("pybool")
    tax_exemptions = []
    total_spent = 0.0  # To be incremented with actual orders
    updated_at = SelfAttribute('created_at')
    verified_email = True
    admin_graphql_api_id = "dfsdfd"
    marketing_opt_in_level = Faker('random_element', elements=_opt_in_levels)
    multipass_identifier = ''
    note = ''
    phone = Faker("safe_e164")
    metafield = None

"""
class TaxLineFactory(Factory):
    class Meta:
        model = TaxLine

    price = 13.5
    rate = 0.06
    title = "State tax"
"""

class OrderLineItemFactory(Factory):
    class Meta:
        model = OrderLineItemCreate

    title = Faker("name")  # TODO: get it from actual product
    # product_id = 5605681594534
    variant_id = 35682265563302
    quantity = random.randint(1, 4)
    price = 30 + random.randint(0, 60)
    taxable = True


def calculate_total(o):
    subtotal = sum([li.price * li.quantity for li in o.line_items])
    if o.discount_codes:
        # only apply 1 discount
        if o.discount_codes[0]['type'] == 'percentage':
            subtotal -= subtotal * float(o.discount_codes[0]['amount']) / 100.0
        if o.discount_codes[0]['type'] == 'fixed_amount':
            subtotal -= float(o.discount_codes[0]['amount'])
    return subtotal + o.total_tax


class OrderCreateFactory(Factory):
    class Meta:
        model = OrderCreate

    currency = "USD"
    line_items = LazyAttribute(lambda o: [OrderLineItemFactory()])
    fulfillment_status = 'fulfilled'
    tax_lines = LazyAttribute(lambda o: [
          {
            "price": sum([li.price * li.quantity for li in o.line_items]) * 0.06,
            "rate": 0.06,
            "title": "State tax"
          },
          {
            "price": sum([li.price * li.quantity for li in o.line_items]) * 0.025,
            "rate": 0.025,
            "title": "County tax"
          }
        ]
    )
    total_tax = LazyAttribute(lambda o: sum([tl['price'] for tl in o.tax_lines]))
    financial_status = "paid"  # authorized, pending, partially_paid, paid, partially_refunded, refunded, voided
    # Order with a new customer
    customer = SubFactory(CustomerFactory)
    # Order with existing customer
    # customer = {
    #     "id": 3939692576934
    # }
    billing_address = LazyAttribute(lambda o: o.customer.default_address)
    shipping_address = LazyAttribute(lambda o: o.customer.default_address)
    email = LazyAttribute(lambda o: o.customer.email)
    processed_at = Faker("date_time_between", start_date='-1year')
    tags = 'generated'

    discount_codes = [random.choice([
        {
            "code": "FRIYAY",
            "amount": "10.00",
            "type": "percentage"
        },
        {
            "code": "OFF5",
            "amount": "5.00",
            "type": "fixed_amount"
        }
    ])]

    source_name = np.random.choice(["website", "ios", "phone"], p=[0.4, 0.35, 0.25])

    transactions = LazyAttribute(lambda o: (
        [{
            'kind': 'sale',
            'status': 'success',  # TODO: add randomness and failure here
            'amount': calculate_total(o)
        }]
    ))
