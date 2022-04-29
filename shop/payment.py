import requests

user_id = '123123'
parameters = {
    "token": "39708:AAB4zl9Uvd9k1ksq5LbCDz85LORVMmEKpVs",
    "api_url": "https://pay.crypt.bot/"
}


# для наглядности

class CryptoPay(object):
    user_id = '123123'
    parameters = {
        "token": "39708:AAB4zl9Uvd9k1ksq5LbCDz85LORVMmEKpVs",
        "api_url": "https://pay.crypt.bot/"
    }

    def __init__(self, user_id, parameters) -> None:
        self.token = parameters['token']
        self.api_url = parameters['api_url']
        self.user_id = user_id
        self.headers = {
            "Crypto-Pay-API-Token": self.token
        }
        pass

    def get_me(self):
        getMe_url = f"{self.api_url}api/getMe"
        try:
            app_info = requests.get(getMe_url, headers=self.headers).json()
            return app_info
        except:
            return False

    def create_invoice(self, amount, asset, description=None, hidden_message='Оплата прошла успешно!',
                       expires_in=86400):
        payload = self.user_id
        invoice_url = f"{self.api_url}api/createInvoice"
        params = {
            "asset": asset,
            "amount": amount,
            "payload": payload,
            "hidden_message": hidden_message,
            "expires_in": expires_in
        }
        if description:
            params["description"] = description
        try:
            invoice_info = requests.get(invoice_url, headers=self.headers, params=params).json()
            return invoice_info
        except:
            return False

    def get_all_invoices(self):
        invoices_url = f"{self.api_url}api/getInvoices"
        invoice_info = requests.get(invoices_url, headers=self.headers).json()
        return invoice_info
        return False

    def get_invoice(self, invoice_id):
        invoices_list = self.get_all_invoices()
        if invoices_list:
            return [invoice for invoice in invoices_list["result"]["items"] if invoice["invoice_id"] == invoice_id]
        else:
            return False

    def get_exchange_rates(self, mon):
        rates_url = f'{self.api_url}api/getExchangeRates'
        exchange_rates = requests.get(rates_url, headers=self.headers).json()
        if exchange_rates['ok']:
            return [rate for rate in exchange_rates["result"] if rate['source'] == mon and rate['is_valid'] == True]
        else:
            return False

    def transfer(self, amount, spend_id, user_id=None, asset="TON"):
        transfer_url = f'{self.api_url}api/transfer'
        if not user_id:
            user_id = self.user_id
        params = {
            "amount": amount,
            "spend_id": spend_id,
            "user_id": user_id,
            "asset": asset,
        }
        try:
            transfer_info = requests.get(transfer_url, headers=self.headers, params=params).json()
            return transfer_info
        except:
            return False


