from dataclasses import field
from datetime import datetime
from typing import List, Optional

from marshmallow_dataclass import dataclass
import marshmallow.validate


@dataclass
class Address:
    id: int
    customer_id: int
    default: bool
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None
    phone: Optional[str] = None
    province_code: Optional[str] = None
    country_code: Optional[str] = None
    country_name: Optional[str] = None


@dataclass
class MetaField:
    key: str
    namespace: str
    value: str
    value_type: str # can be either "string" or "integer"


@dataclass
class Customer:
    """
    https://shopify.dev/docs/admin-api/rest/reference/customers/customer
    """
    accepts_marketing: bool
    accepts_marketing_updated_at: datetime
    addresses: List[Address]
    currency: str
    created_at: datetime
    default_address: Address
    email: str
    first_name: str
    id: int
    last_name: str
    last_order_id: int
    last_order_name: str
    orders_count: int
    state: str  # can be disabled, invited, enabled, declined
    tags: str
    tax_exempt: bool
    tax_exemptions: List[str]
    total_spent: float
    updated_at: datetime
    verified_email: bool
    admin_graphql_api_id: str
    marketing_opt_in_level: Optional[str] = None  # can be single_opt_in, confirmed_opt_in, unknown
    multipass_identifier: Optional[str] = None
    note: Optional[str] = None
    phone: Optional[str] = None
    metafield: MetaField = field(default=None)

    def __post__init(self):
        pass

    def get_create_object(self):
        data = self.Schema(exclude=['id', 'default_address.id', 'default_address.customer_id']).dump(self)
        del data['addresses'][0]['id']
        del data['addresses'][0]['customer_id']
        return data
