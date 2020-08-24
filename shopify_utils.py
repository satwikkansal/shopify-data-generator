import os
from dotenv import load_dotenv
import shopify

load_dotenv()


def fetch_mandatory_env_var(key):
    val = os.getenv(key)
    if not val:
        raise ValueError(f"Please set {API_KEY} in the .env file or environment variables")
    return val


API_KEY = fetch_mandatory_env_var('API_KEY')
PASSWORD = fetch_mandatory_env_var('PASSWORD')
SHOP_NAME = fetch_mandatory_env_var('SHOP_NAME')
API_VERSION = fetch_mandatory_env_var('API_VERSION')

shop_url = F"https://{API_KEY}:{PASSWORD}@{SHOP_NAME}.myshopify.com/admin/api/{API_VERSION}"
shopify.ShopifyResource.set_site(shop_url)


def publish(obj, target_class):
    data = obj.get_create_object()
    new_obj = target_class().create(data)
    if new_obj.errors:
        # something went wrong!
        for message in new_obj.errors.full_messages():
            print(message)
    else:
        print(f'Object of type {new_obj.__class__.__name__} created with ID #{new_obj.id}')
    return new_obj


def delete(obj, target_class):
    if target_class.exists(obj.id):
        upstream_obj = target_class.find(obj.id)
        upstream_obj.destroy()
        print("[DELETED] object #{} of class {}".format(obj.id, upstream_obj.__class__.__name__))
    else:
        print("[WARNING]: object #{} of class {} not found.".format(obj.id, target_class))


def get_all_resources(target_class):
    results = []
    page = target_class.find()
    results += page

    while page.has_next_page():
        page = target_class.find(from_=page.next_url)
        results += page

    return results
