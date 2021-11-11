


class Crypto():

    def __init__(self, asset_info):
        """
        Constructor de crypto

        Args:
            asset_info: Información del asset obtenida a partir del método de la API de binance get_exchange_info.
        """
        self.symbol = ''
        self.status = ''
        self.base_asset = ''
        self.quote_asset = ''
        self.quote_precision = ''
        self.quote_asset_precision = ''
        self.base_comission_precision = ''
        self.quote_comission_precision = ''
        self.order_types = dict()
        self.iceberg_allowed = bool
        self.oco_allowed = bool
        self.quote_order_qty_market_allowed = bool
        self.is_spot_trading_allowed = bool
        self.is_margin_trading_allowed = bool
        self.filters = list()
        self.permissions = list()