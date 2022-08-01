import json
from typing import Dict
import requests

class MonzoClient:
    
    
    def __init__(self, access_token: str) -> None:
        """
        Initialises the Monzo client object with the required attributes. 
        """
        self.access_token = access_token
        self.monzo_base_url = "https://api.monzo.com"
        self.headers = {"Authorization" : f'Bearer {self.access_token}'}
        self.validate_access_token()
        
    
    def validate_access_token(self) -> None: 
        """
        Verifies if the the Monzo access token is valid
        """
        if not isinstance(self.access_token, str):
            raise TypeError('Error: Access token should be a string')
        elif len(self.access_token) != 239:
            raise ValueError("Error: Length of access token is wrong. Please check that your access token is valid")

    
    def make_request(self, monzo_endpoint: str, params=None) -> requests: 
        """
        Makes a GET request to a monzo endpoint and returns a response object
        """
        if params:
            res = requests.get(self.monzo_base_url + monzo_endpoint, headers=self.headers, params=params)
        else:
            res = requests.get(self.monzo_base_url + monzo_endpoint, headers=self.headers) 

        if res.status_code != 200:
            return (f"Error talking to Monzo API. Status code: {res.status_code}")
        return res
    
    
    def whoami(self) -> json: 
        """
        Returns the response for the /ping/whoami API endpoint
        More details here: https://docs.monzo.com/#acquire-an-access-token
        """
        res = self.make_request("/ping/whoami")
        return res.json()
    
    
    def get_accounts(self) -> json:
        """
        Returns the response for the "/accounts API endpoint
        More details here: https://docs.monzo.com/#accounts
        """
        res = self.make_request("/accounts")
        return res.json()

    
    def get_account_ids(self):
        """
        Returns a list of account Id's from the response of the /accounts API endpoint
        More details here: https://docs.monzo.com/#accounts
        """
        json_res = self.get_accounts()

        return [item['id'] for item in json_res['accounts']]
    
    
    def get_balance(self, account_id: Dict[str, str]) -> json:
        """
        Returns the response for the "/balance API endpoint
        More details here: https://docs.monzo.com/#balance
        """
        
        params= {
            "account_id" : account_id
            }
        
        res = self.make_request("/balance", params=params)
        return res.json()
   
    
    def get_transactions(self, account_id: str, since=None, before=None,  limit=None) -> json:
        """
        Returns the response for the "/transactions API endpoint
        More details here: https://docs.monzo.com/#transactions
        """
        
        params = {
            "expand[]": "merchant",
            "account_id": account_id,
            "before": before,
            "since": since,
            "limit": limit,
        }
        
        res = self.make_request("/transactions", params=params)
        return res.json()
    
    
    def get_transaction(self, transaction_id: str) -> json:
        """
        Returns the response for the /transactions/{transaction_id} API endpoint
        More details here: https://docs.monzo.com/#transactions
        """

        params = {
            "expand[]": "merchant",
        }
        path = f"/transactions/{transaction_id}"
        
        res = self.make_request(path, params=params)
        return res.json()
        

    def get_pots(self, account_id: str) -> json:
        """
        Returns the response for the /pots API endpoint
        More details here: https://docs.monzo.com/#pots
        """
        
        params = {
            "current_account_id": account_id
        }
        
        res = self.make_request("/pots", params=params)
        return res.json()
   