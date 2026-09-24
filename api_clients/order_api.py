class OrderAPI:
    """Encapsulates order-related API interactions."""

    ENDPOINT = "/orders"

    def __init__(self, api_request_context):
        self.api_request_context = api_request_context

    def create_order(self, access_token, cart_id, customer_name):
        return self.api_request_context.post(
            self.ENDPOINT,
            headers={"Authorization": f"Bearer {access_token}"},
            data={"cartId": cart_id, "customerName": customer_name},
        )

    def get_all_orders(self, access_token):
        return self.api_request_context.get(
            self.ENDPOINT,
            headers={"Authorization": f"Bearer {access_token}"},
        )
