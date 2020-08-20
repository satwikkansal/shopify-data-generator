from dataclasses import field
from typing import List, Optional

from marshmallow_dataclass import dataclass


@dataclass
class Address:
    id: Optional[int] = None
    customer_id: Optional[int] = None
    default: Optional[bool] = None
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

    @classmethod
    def from_kwargs(cls, **kwargs):
        # split the kwargs into native ones and new ones
        native_args, new_args = {}, {}
        for name, val in kwargs.items():
            if name in cls.__annotations__:
                native_args[name] = val
            else:
                new_args[name] = val

        # use the native ones to create the class ...
        ret = cls(**native_args)

        # # ... and add the new ones by hand
        # for new_name, new_val in new_args.items():
        #     setattr(ret, new_name, new_val)
        return ret


@dataclass
class ShippingAddress(Address):
    latitude: Optional[float] = None
    longitiude: Optional[float] = None


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
    accepts_marketing_updated_at: str
    addresses: List[Address]
    currency: str
    created_at: str
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
    updated_at: str
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

    @classmethod
    def from_kwargs(cls, **kwargs):
        # split the kwargs into native ones and new ones
        native_args, new_args = {}, {}
        for name, val in kwargs.items():
            if name in cls.__annotations__:
                native_args[name] = val
            else:
                new_args[name] = val

        # use the native ones to create the class ...
        ret = cls(**native_args)

        # # ... and add the new ones by hand
        # for new_name, new_val in new_args.items():
        #     setattr(ret, new_name, new_val)
        return ret

@dataclass
class OrderLineItemCreate:
    title: str
    # product_id: int
    variant_id: int
    quantity: int
    price: float
    taxable: bool = True


@dataclass
class OrderCreate:
    billing_address: Address
    customer: Customer
    #customer: dict
    currency: str
    discount_codes: List[dict]  # Added extra for create api
    email: str
    financial_status: str
    fulfillment_status: str
    line_items: List[OrderLineItemCreate]
    shipping_address: Address
    source_name: str
    tax_lines: List[dict]
    transactions: List[dict]  # Added extra for create api
    total_tax: float
    processed_at: str
    tags: str

    def get_create_object(self):
        data = self.Schema().dump(self)
        return data


"""
@dataclass
class Image:
    id: int = field(metadata=dict(load_only=True))
    created_at: datetime = field(metadata=dict(load_only=True))
    updated_at: datetime = field(metadata=dict(load_only=True))

    product_id: int = field(metadata=dict(load_only=True))
    position: int
    src: str
    variant_ids: List[int] = field(default_factory=list)
    width: int = 110
    height: int = 140


@dataclass
class Price:
    currency_code: str
    amount: float


@dataclass
class PresentmentPrice:
    price: Price
    compare_at_price: Price


@dataclass
class PriceSet:
    shop_money: Price
    presentment_money: Price


@dataclass
class ProductVariant:
    id: int = field(metadata=dict(load_only=True))
    created_at: datetime = field(metadata=dict(load_only=True))
    updated_at: datetime = field(metadata=dict(load_only=True))

    product_id: int = field(metadata=dict(load_only=True))
    image_id: int = field(metadata=dict(load_only=True))
    inventory_item_id: int = field(metadata=dict(load_only=True))

    barcode = Optional[str]
    compare_at_price: float
    grams: int
    inventory_management: str
    inventory_policy: str  # deny, continue
    inventory_quantity: int = field(metadata=dict(load_only=True))
    old_inventory_quantity: int
    inventory_quantity_adjustment: int
    option1: Optional[str]
    option2: Optional[str]
    option3: Optional[str]
    presentment_prices: List[PresentmentPrice]
    position: int = field(metadata=dict(load_only=True))
    price: float
    requires_shipping: bool  # deprecated
    sku: str
    taxable: bool
    tax_code: str
    title: str
    weight: int
    fulfillment_service: str = "manual"
    weight_unit: str = "g"


@dataclass
class Product:
    body_html: str
    created_at: datetime = field(metadata=dict(load_only=True))
    id: int = field(metadata=dict(load_only=True))
    # handle: str # autogenerated from title
    images: List[Image]
    options: List[dict]
    product_type: str
    published_at: datetime # null means unpublished
    published_scope: str  # web or global
    tags: str  # comma-separated
    title: str
    updated_at: datetime = field(metadata=dict(load_only=True))
    variants: List[ProductVariant]

    template_suffix: Optional[str]
    vendor: Optional[str]


@dataclass
class OrderDiscount:
    type: str  # discount_code, manual, script
    title: str
    description: str
    code: Optional[str]
    value: float
    value_type: str
    allocated_method: str # a cross, each, one
    target_selection: str
    target_type: str

@dataclass
class DiscountCode:
    code: str
    amount: float
    type: str # fixed_amount, percentage, shipping

@dataclass
class TaxLine:
    title: str
    price: float
    #price_set: Optional[PriceSet]
    rate: float

@dataclass
class OrderLineItem:
    fulfillable_quantity: int
    fulfillment_service: str
    fulfillment_status: str
    grams: int
    id: int = field(metadata=dict(load_only=True)) # TODO: check
    price: float
    product_id: int = field(metadata=dict(load_only=True))
    quantity: int
    requires_shipping: bool
    sku: str
    title: str
    variant_id: int
    variant_title: str
    name: str
    price_set: PriceSet
    properties: List[dict]
    taxable: bool
    tax_lines: List[TaxLine]
    total_discount: float = field(metadata=dict(load_only=True))
    total_discount_set: PriceSet
    discount_allocattion: List[dict]  # TODO: update later on if discount is used
    origin_location: Address
    duties: List[dict]
    admin_graph_ql_api_id: str
    gift_card: bool = False


@dataclass
class Order:
    app_id: int = field(metadata=dict(load_only=True))
    billing_address: Address
    browser_ip: str = field(metadata=dict(load_only=True))
    buyer_accepts_marketing: bool
    cancel_reason: Optional[str]
    cancelled_at: str = field(metadata=dict(load_only=True))
    client_details: dict = field(metadata=dict(load_only=True))
    closed_at: datetime = field(metadata=dict(load_only=True))
    created_at: datetime = field(metadata=dict(load_only=True))
    currency: str
    current_total_duties_set: dict = field(metadata=dict(load_only=True))
    customer: Customer
    customer_locale: str
    discount_applications: List[OrderDiscount]
    discount_codes: List[dict]  # Added extra for create api
    email: str
    financial_status: str  # authorized, pending, partially_paid, paid, partially_refunded, refunded, voided
    fulfillments: List[dict]
    fulfillment_status: str  # partial, fulfilled, null, restocked
    id: int = field(metadata=dict(load_only=True))
    landing_site: str = field(metadata=dict(load_only=True))
    line_items: List[OrderLineItem]
    location_id: int = field(metadata=dict(load_only=True))
    name: str = field(metadata=dict(load_only=True))
    note: str
    note_attributes: List[dict]
    number: int = field(metadata=dict(load_only=True))
    order_number: int = field(metadata=dict(load_only=True))
    original_total_duties_set: PriceSet = field(metadata=dict(load_only=True))
    payment_details: dict
    payment_gateway_names: List[str]
    phone: str
    presentment_currency: str
    processed_at: datetime = field(metadata=dict(load_only=True))
    processing_method: str = field(metadata=dict(load_only=True))
    referring_site: str
    refunds: List[dict] = field(metadata=dict(load_only=True))
    shipping_address: ShippingAddress
    shipping_lines: List[dict]  # TODO: later if needed
    source_name: str  # Possible values; web, pos, shopify_draft_order, iphone, and android
    subtotal_price: float
    subtotal_price_set: PriceSet
    tags: str
    tax_lines: List[TaxLine]
    taxes_included: bool
    token: str = field(metadata=dict(load_only=True))
    total_discounts: float
    total_discounts_set: PriceSet
    total_line_items_price: PriceSet
    total_price: float
    total_price_set: PriceSet
    total_tax: float
    total_tax_set: PriceSet
    total_tip_received: float
    total_weight: int
    transactions: List[dict]  # Added extra for create api
    updated_at: datetime = field(metadata=dict(load_only=True))
    user_id: int
    order_status_url: str = field(metadata=dict(load_only=True))
    gateway: str = "shopify_payments"
    test: bool = True
"""
