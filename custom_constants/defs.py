API_KEY = "39c92c26d426cd80aea158e639fe42eb-732f53d33748678f48d4ae448fe6d286"
ACCOUNT_ID = "101-004-27643856-001"
OANDA_URL = "https://api-fxpractice.oanda.com/v3/"

SECURE_HEADER = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type":"application/json"
}

SELL = -1
BUY = 1
NONE = 0

MONGO_CONN_STR = "mongodb+srv://Negarin:Negarin610@negarin.j2jmyuo.mongodb.net/?retryWrites=true&w=majority"