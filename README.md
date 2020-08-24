# Shopify Orders Generator

> A script to generate simulated orders in your Shopify store.

## One-time set up

- Create a Private app on Shopify
- Add the credentials to a `.env` file in the project directory
```
API_KEY=''
PASSWORD=''
SHOP_NAME='my-awesome-store-for-dev'
API_VERSION='2020-07'
```
- Import some products and customers through Shopify Dashboard. You can use the exports provided in the data folder (generated using [simple-sample-data](https://apps.shopify.com/simple-sample-data) app). 
- Install the dependencies
```shell script
$ pip install -r requirements.txt
```

## Runing the script
`python generate.py -n 10 -d 10` will generate 10 orders no older than 10 days from the current date.
```shell script
$ python generate.py -h

usage: generate.py [-h] [-n NUM_ORDERS] [-d BACK_DAYS]

Populate data in your Shopify store

optional arguments:
  -h, --help            show this help message and exit
  -n NUM_ORDERS, --num_orders NUM_ORDERS
                        Number of orders to generate
  -d BACK_DAYS, --back_days BACK_DAYS
                        Number of days to go back from the current date to generate the orders
```

**Note:** Shopify doesn't allow to create more than 5 orders per minute through the Orders API, so the script has a sleep time of 15 seconds after every order creation.