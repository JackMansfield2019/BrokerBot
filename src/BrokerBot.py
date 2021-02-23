import DataHandler
import ExecutionHandler
import PortfolioManager
import StrategyHandler


class BrokerBot:
  def __init__(self, API_key_id, API_secret_key, base_url):

  	self.headers = {"APCA-API-KEY-ID": API_key_id,
  	    "APCA-API-SECRET-KEY": API_secret_key}



    self.base_url = base_url
    self.account_url= "{}/v2/account".format(self.base_url)
    self.order_url = "{}/v2/orders".format(self.base_url)

    self.Data

  def get_account(self):
  	r = requests.get(self.account_url,headers)
  	return json.loads(r.content)
