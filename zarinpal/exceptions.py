class Error(Exception):
    """Base Error"""

class TooSmallException(Error):
    """The required amount to start the payment is at least 1000."""

class MerchantIDException(Error):
    """MerchantID is empty or not valid."""

class ZarinPalSandBoxException(Error):
    """ZARINPALSANDBOX is empty or not valid."""

class CallBackURLException(Error):
    """Callbackurl is empty or not valid."""


