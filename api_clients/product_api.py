class ProductAPI:
    """Encapsulates product-related API interactions."""

    ENDPOINT = "/products"

    def __init__(self, api_request_context):
        self.api_request_context = api_request_context

    def get_products(self):
        return self.api_request_context.get(self.ENDPOINT)

    def get_product_not_in_stock(self):
        return self.api_request_context.get(self.ENDPOINT, params={"inStock": "false"})

    def get_product_by_id(self, product_id):
        return self.api_request_context.get(f"{self.ENDPOINT}/{product_id}")

    def get_product_by_name(self, name):
        return self.api_request_context.get(self.ENDPOINT, params={"name": name})


