from models import Address, Customer

from factory import Faker, Factory, Sequence, SubFactory, SelfAttribute, LazyAttribute
from faker_e164.providers import E164Provider
import pandas as pd


Faker.add_provider(E164Provider)

postal_df = pd.read_csv("zip-codes.csv", header=None, converters={0: lambda x: str(x)})
postal_df.columns = ["postal_code", "lat", "long", "city", "state", "county", "unique"]
# State abbreviations to remove. Shopify does not recognize these states.
# From: US District, Territory, and Possession Abbreviations and Capitals
# http://www.stateabbreviations.us/
for state in ['AS', 'DC', 'FM', 'GU', 'MH', 'MP', 'PW', 'PR', 'VI']:
    postal_df = postal_df[postal_df.state != state]


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
    phone = Faker("safe_e164", region_code='US')
    metafield = None
