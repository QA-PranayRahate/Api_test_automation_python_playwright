class CartAPI:
    """Encapsulates cart-related API interactions."""

    ENDPOINT = "/carts"

    def __init__(self, api_request_context):
        self.api_request_context = api_request_context

    def create_cart(self, access_token):
        return self.api_request_context.post(
            self.ENDPOINT,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def add_item_to_cart(self, access_token, cart_id, product_id, quantity):
        return self.api_request_context.post(
            f"{self.ENDPOINT}/{cart_id}/items",
            data={"productId": product_id, "quantity": quantity},
            headers={"Authorization": f"Bearer {access_token}"},
        )
