## About 

The script will generate specified number of orders.

## Steps

- Create a Private app
- Add the credentials to a `.env` file
- Import the products and customers through Shopify Dashboard.
- Run the script to generate the orders
```shell script
$ pip install -r requirements.txt
$ python generate.py
```
**Note:** Shopify doesn't allow to create more than 5 orders per minute through the Orders API, so the script has a sleep time of 15 seconds after every order creation.