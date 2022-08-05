
from types import NoneType
from django.utils.html import strip_tags
from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
db = client.messari

def getAssets():   
    # find by date
    timestamp = str(datetime.now().date())
    list_assets =list (db.prueba1.find({'date':timestamp},{"_id":0}))    
    if len(list_assets)==0:
        # find by last record
        last_record = db.prueba1.find({},{"_id":0,"date":1}).sort("_id",-1).limit(1)
        last_record=list(last_record)[0]['date']
        list_assets = list(db.prueba1.find({'date':last_record},{"_id":0}))
    for assets in list_assets:
        assets['metrics']['marketcap']['current_marketcap_usd']=assets['metrics']['marketcap']['current_marketcap_usd']/pow(10,6)

               #print(deltaChange(s[x]['symbol']),'getassets')
    #             s[x]['change7']=deltaChange(s[x]['symbol'])
                
    #             if s[x]['metrics']['market_data']['percent_change_usd_last_24_hours'] :
    #                 if deltaChange(s[x]['symbol']):
    #             #     s[x]['metrics']['market_data']['percent_change_usd_last_24_hours']=0
                
    #                  s[x]['change7']=s[x]['metrics']['market_data']['percent_change_usd_last_24_hours']-deltaChange(s[x]['symbol'])
    #             #
    #             #print(type(s[x]['change7']),'sssssss', type(s[x]['metrics']['market_data']['percent_change_usd_last_24_hours']))
                
    return list_assets

def deltaChange(symbol1):
    valor=0
    timestamp = datetime.now().date()
    #consultar por fecha
    d = datetime(timestamp.year, timestamp.month, (timestamp.day-7))
    #print(d) 
    assets_by_date = db.assets.find({"timestamp": {"$eq": d}},{"_id":0,"timestamp":0})
    for asset in assets_by_date:
        for coin in asset:
            if asset[coin]['symbol']== symbol1:
             valor= asset[coin]['metrics']['market_data']['percent_change_usd_last_24_hours']
            #  print(asset[coin]['metrics']['market_data']['percent_change_usd_last_24_hours'])
            #  print(asset[coin]['metrics']['market_data']['last_trade_at'])
                        
    return valor       

def coin_detail(symbol,date):
    detail=list( db.prueba1.find({"symbol":symbol, "date":date}).limit(1))   
    listMetric = detail[0]
    profile = db.profile.find({},{"_id":0,"timestamp":0}).sort("_id",-1).limit(1)                
 
    roi_detail1=[]
    for key , value in zip(listMetric['metrics']['roi_by_year'].keys(),listMetric['metrics']['roi_by_year'].values()):       
        roi_detail1.append([key[:4] , value])
    
    listMetric['metrics']['roi_by_year']=roi_detail1

    #generacion de un list()para el tratamiento de los datos del profile
    profile_detail=list()
    for doc in profile:  
     for ind in doc:
        if doc[ind]['name']==listMetric['name']:
         profile_detail={'category':doc[ind]['profile']['general']['overview']['category']}
         profile_detail['tagline']=doc[ind]['profile']['general']['overview']['tagline']
         profile_detail['sector']=doc[ind]['profile']['general']['overview']['sector']         
         profile_detail['roadmap']=format_date(doc[ind]['profile']['general']['roadmap'])
         profile_detail['economics']=doc[ind]['profile']['economics']
        #eliminacion de tag con strip_tags 
         profile_detail['project_details']=strip_tags(doc[ind]['profile']['general']['overview']['project_details'])        
         profile_detail['technology']=strip_tags(doc[ind]['profile']['technology']['overview']['technology_details'])
         profile_detail['regulatory_details']=strip_tags(doc[ind]['profile']['general']['regulation']['regulatory_details'])
         profile_detail['governance']=strip_tags(doc[ind]['profile']['governance']['governance_details'])
         profile_detail['economics_launchDetails']=strip_tags(doc[ind]['profile']['economics']['launch']['general']['launch_details'])


    #find symbol_tradingview para el requeste del widget 
    symbol_coins = db.ticker.find({},{"_id":0,"symbol":0}).sort("_id",-1).limit(1) 
    for symbol_coin in symbol_coins:
        for aux in symbol_coin:
         if aux == symbol:   
         # print(aux,':',symbol_coin[aux])
          profile_detail['symbol_tradingview']=symbol_coin[aux]
    
    coin_detail={'asset': listMetric,'profile': profile_detail}  
   
    return coin_detail
def format_date(roadmap):
    for iterator in roadmap:
        aux = iterator['date'] 
        if iterator['date']:              
         dto = datetime.strptime(aux, "%Y-%m-%dT%H:%M:%SZ").date()                                         
         iterator['date']= dto
    
    return roadmap

    






    