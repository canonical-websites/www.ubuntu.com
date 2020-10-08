from requests.exceptions import HTTPError


class AdvantageContracts:
    def __init__(
        self,
        session,
        authentication_token,
        token_type="Macaroon",
        api_url="https://contracts.staging.canonical.com",
    ):
        """
        Expects a Talisker session in most circumstances,
        from `talisker.requests.get_session()`
        """

        self.session = session
        self.authentication_token = authentication_token
        self.token_type = token_type
        self.api_url = api_url.rstrip("/")

    def _request(self, method, path, json=None):
        headers = {}

        headers["Authorization"] = (
            f"{self.token_type} " f"{self.authentication_token}"
        )

        response = self.session.request(
            method=method,
            url=f"{self.api_url}/{path}",
            json=json,
            headers=headers,
        )
        response.raise_for_status()

        return response

    def get_accounts(self):
        response = self._request(method="get", path="v1/accounts")

        return response.json().get("accounts", [])

    def get_account_contracts(self, account):
        account_id = account["id"]
        response = self._request(
            method="get", path=f"v1/accounts/{account_id}/contracts"
        )

        return response.json().get("contracts", [])

    def get_contract_token(self, contract):
        contract_id = contract["contractInfo"]["id"]
        response = self._request(
            method="post", path=f"v1/contracts/{contract_id}/token", json={}
        )

        return response.json().get("contractToken")

    def get_contract_machines(self, contract):
        contract_id = contract["contractInfo"]["id"]

        response = self._request(
            method="get", path=f"v1/contracts/{contract_id}/context/machines"
        )

        return response.json()

    def put_customer_info(
        self, account_id, payment_method_id, address, name, tax_id
    ):
        try:
            response = self._request(
                method="put",
                path=f"v1/accounts/{account_id}/customer-info/stripe",
                json={
                    "defaultPaymentMethod": {"Id": payment_method_id},
                    "paymentMethodID": payment_method_id,
                    "address": address,
                    "name": name,
                    "taxID": tax_id,
                },
            )
        except HTTPError as http_error:
            return http_error.response.json()

        return response.json()

    def put_anonymous_customer_info(self, account_id, address, tax_id):
        try:
            response = self._request(
                method="put",
                path=f"v1/accounts/{account_id}/customer-info/stripe",
                json={"address": address, "taxID": tax_id},
            )
        except HTTPError as http_error:
            return http_error.response.json()

        return response.json()

    def post_stripe_invoice_id(self, tx_type, tx_id, invoice_id):
        try:
            response = self._request(
                method="post",
                path=f"v1/{tx_type}/{tx_id}/payment/stripe/{invoice_id}",
            )
        except HTTPError as http_error:
            return http_error.response.json()

        return response.json()

    def get_renewal(self, renewal_id):
        response = self._request(
            method="get", path=f"v1/renewals/{renewal_id}"
        )

        return response.json()

    def accept_renewal(self, renewal_id):
        try:
            response = self._request(
                method="post", path=f"v1/renewals/{renewal_id}/acceptance"
            )
        except HTTPError as http_error:
            if http_error.code == 500:
                return response.json()
            else:
                raise http_error

        return {}

    def post_renewal_preview(self, renewal_id):
        response = self._request(
            method="post", path=f"v1/renewals/{renewal_id}/purchase/preview"
        )

        return response.json()

    def get_marketplace_product_listings(self, marketplace: str) -> dict:
        response = self._request(
            method="get", path=f"v1/marketplace/{marketplace}/product-listings"
        )

        return response.json()

    def get_account_subscriptions_for_marketplace(
        self, account_id: str, marketplace: str
    ) -> dict:
        response = self._request(
            method="get",
            path=(
                f"v1/accounts/{account_id}"
                f"/marketplace/{marketplace}/subscriptions"
            ),
        )

        return response.json()

    def get_account_purchases(self, account_id: str) -> dict:
        response = self._request(
            method="get", path=f"v1/accounts/{account_id}/purchases"
        )

        return response.json()

    def get_purchase(self, purchase_id: str) -> dict:
        response = self._request(
            method="get", path=f"v1/purchase/{purchase_id}"
        )

        return response.json()

    def get_purchase_account(self, email: str, payment_method_id: str) -> dict:
        try:
            response = self._request(
                method="post",
                path="v1/purchase-account",
                json={
                    "email": email,
                    "defaultPaymentMethod": {"Id": payment_method_id},
                },
            )
        except HTTPError as http_error:
            guest = email and payment_method_id

            if guest and http_error.response.status_code == 401:
                return http_error.response.json()
            else:
                raise http_error

        return response.json()

    def purchase_from_marketplace(
        self, marketplace: str, purchase_request: dict
    ) -> dict:
        response = self._request(
            method="post",
            path=f"v1/marketplace/{marketplace}/purchase",
            json=purchase_request,
        )

        return response.json()

    def preview_purchase_from_marketplace(
        self, marketplace: str, purchase_request: dict
    ) -> dict:
        response = self._request(
            method="post",
            path=f"v1/marketplace/{marketplace}/purchase/preview",
            json=purchase_request,
        )

        return response.json()
