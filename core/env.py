from dotenv import load_dotenv
import os

load_dotenv()

token = os.environ.get('TOKEN')
webAddress = os.environ.get('WEBADDRESS')
itemSoloAddress = os.environ.get('ITEMSOLOADDRESS')
itemImageAddress = os.environ.get('ITEMIMAGEADDRESS')
databaseFile = os.environ.get('DATABASEFILE')