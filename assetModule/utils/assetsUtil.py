

from contextlib import nullcontext
from symtable import Symbol
from tracemalloc import start
from types import NoneType
from django.utils.html import strip_tags
from pymongo import MongoClient
from datetime import date, datetime
from bokeh.embed import components
import numpy as np
from bokeh.layouts import layout
from bokeh.models import HoverTool,DateRangeSlider,BoxZoomTool,WheelZoomTool,ResetTool,PanTool,LinearAxis
from bokeh.plotting import figure, show

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
                                               
                # s[x]['metrics']['market_data']['last_trade_at']= datetime.strptime(s[x]['metrics']['market_data']['last_trade_at'], "%Y-%m-%dT%H:%M:%SZ").date()                                                        
                # s[x]['metrics']['marketcap']['current_marketcap_usd']=s[x]['metrics']['marketcap']['current_marketcap_usd']/pow(10,6)
                # #print(deltaChange(s[x]['symbol']),'getassets')
                # s[x]['change7']=deltaChange(s[x]['symbol'])
                
                # if s[x]['metrics']['market_data']['percent_change_usd_last_24_hours'] :
                #     if deltaChange(s[x]['symbol']):
                # #     s[x]['metrics']['market_data']['percent_change_usd_last_24_hours']=0
                
                #      s[x]['change7']=s[x]['metrics']['market_data']['percent_change_usd_last_24_hours']-deltaChange(s[x]['symbol'])
              
                #print(type(s[x]['change7']),'sssssss', type(s[x]['metrics']['market_data']['percent_change_usd_last_24_hours']))
                
    return list_assets

def deltaChange(symbol1):
    valor=0
    timestamp = datetime.now().date() 
    #scritp para consulta por fecha 
    d = datetime(timestamp.year, timestamp.month, (timestamp.day-7))
    #print(d) 
    assets_by_date = db.assets.find({"timestamp": {"$eq": d}},{"_id":0,"timestamp":0})
    for asset in assets_by_date:
        for coin in asset:
            if asset[coin]['symbol']== symbol1:
             #print(asset[coin]['name'],'hollaa')
             valor= asset[coin]['metrics']['market_data']['percent_change_usd_last_24_hours']
            #  print(asset[coin]['metrics']['market_data']['percent_change_usd_last_24_hours'])
            #  print(asset[coin]['metrics']['market_data']['last_trade_at'])

    return valor       
    
    
    

def coin_detail(symbol):
    coin = db.assets.find({},{"_id":0,"timestamp":0}).sort("_id",-1).limit(1)
    profile = db.profile.find({},{"_id":0,"timestamp":0}).sort("_id",-1).limit(1)
    listMetric = []
    for doc in coin:       
        for ind in doc:
            listMetric.append(doc[ind])                      
    asset_detail=list()   
    for c in listMetric:     
     if c['symbol']==symbol:    
         asset_detail={'name':c['name']}
         asset_detail['symbol']=c['symbol']
         asset_detail['metrics']=c['metrics']
         asset_detail['price_usd']=c['metrics']['market_data']['price_usd']
         asset_detail['price_btc']=c['metrics']['market_data']['price_btc']
         asset_detail['price_eth']=c['metrics']['market_data']['price_eth']         
         asset_detail['rank']=c['metrics']['marketcap']['rank']
         asset_detail['percent_change_usd_last_24_hours']=c['metrics']['market_data']['percent_change_usd_last_24_hours']
         asset_detail['percent_change_eth_last_24_hours']=c['metrics']['market_data']['percent_change_eth_last_24_hours']
         asset_detail['last_trade_at']=c['metrics']['market_data']['last_trade_at']

    roi_detail=[]
    for key , value in zip(asset_detail['metrics']['roi_by_year'].keys(),asset_detail['metrics']['roi_by_year'].values()):       
        roi_detail.append([key[:4] , value])
    
    asset_detail['roi_by_year']=roi_detail
    print(asset_detail['roi_by_year']) 
    #generacion de un list()para el tratamiento de los datos del profile
    profile_detail=list()
    for doc in profile:  
     for ind in doc:
        if doc[ind]['name']==asset_detail['name']:
         profile_detail={'category':doc[ind]['profile']['general']['overview']['category']}
         profile_detail['tagline']=doc[ind]['profile']['general']['overview']['tagline']
         profile_detail['sector']=doc[ind]['profile']['general']['overview']['sector']         
         #profile_detail['roadmap']=doc[ind]['profile']['general']['roadmap']
         profile_detail['roadmap']=format_date(doc[ind]['profile']['general']['roadmap'])
         profile_detail['economics']=doc[ind]['profile']['economics']
        

        #eliminacion de tag con strip_tags 
         profile_detail['project_details']=strip_tags(doc[ind]['profile']['general']['overview']['project_details'])        
         profile_detail['technology']=strip_tags(doc[ind]['profile']['technology']['overview']['technology_details'])
         profile_detail['regulatory_details']=strip_tags(doc[ind]['profile']['general']['regulation']['regulatory_details'])
         profile_detail['governance']=strip_tags(doc[ind]['profile']['governance']['governance_details'])
         profile_detail['economics_launchDetails']=strip_tags(doc[ind]['profile']['economics']['launch']['general']['launch_details'])
            # print(ind)
            # print(doc[ind]['profile']['general']['overview']['category'])

    #find symbol_tradingview para el requeste del widget 
    symbol_coins = db.ticker.find({},{"_id":0,"symbol":0}).sort("_id",-1).limit(1) 
    for symbol_coin in symbol_coins:
        for aux in symbol_coin:
         if aux == symbol:   
         # print(aux,':',symbol_coin[aux])
          profile_detail['symbol_tradingview']=symbol_coin[aux]
    

    coin_detail={'asset': asset_detail,'profile': profile_detail}  
   
    return coin_detail
def format_date(roadmap):
    for iterator in roadmap:
        aux = iterator['date'] 
        if iterator['date']:              
         dto = datetime.strptime(aux, "%Y-%m-%dT%H:%M:%SZ").date()                                         
         iterator['date']= dto
    
    return roadmap

def  grafica(symbol):
    
    coinmetric= client.coinmetric[symbol]    
    getvalues= list(coinmetric.find({},{"_id":0, "time":1,"AdrActCnt":1}))
    date1=[]
    refEth=[]
    for value in getvalues:
        auxdate= datetime.fromisoformat(value['time'])
        date1.append(auxdate)
        value1= float(value['AdrActCnt'])/1000000
        refEth.append(value1)
           
    # GRAFICA DATE
    plot = figure(x_axis_type="datetime", 
    title="Adresses Active Acount",
    sizing_mode="stretch_width",
    x_range=(date1[0],date1[-1]),
    tools=[HoverTool(
    formatters={
        '@x': 'datetime', # use 'datetime' formatter for '@date' field
    }
    ),
    BoxZoomTool(),
    WheelZoomTool(dimensions = 'height'),
    WheelZoomTool(dimensions = 'width'),
    ResetTool(),
    PanTool(),
    ],
    tooltips="Date: @x{%F}, Act count: @y M",
    )
    plot.xaxis.axis_label = 'Date'
    plot.yaxis.axis_label = 'Active Acount (M)'
    plot.grid.grid_line_alpha = 0

    yaxis = LinearAxis(minor_tick_line_color=None,
    axis_label = "Eje Y",
    axis_label_text_font_style = 'normal',
    name="yaxis")
    plot.add_layout(yaxis, 'right')
  
    plot.line(date1, refEth, legend_label=symbol,line_color = '#2B3040')
    # # set up RangeSlider
    range_slider = DateRangeSlider(
        title="Date range",
        start=date(2017, 1, 1),
        end=date(2020, 1, 1),
        step=1,
        value=(plot.x_range.start, plot.x_range.end),
    )
    range_slider.js_link("value", plot.x_range, "start", attr_selector=0)
    range_slider.js_link("value", plot.x_range, "end", attr_selector=1)
    # # create layout
    layout1 = layout(
        [
            [range_slider],
            [plot],
            
        ],
        sizing_mode='stretch_width',
        max_width=1450,
       
    )
    script, div = components(layout1)
    
    context= {
       'script': script,
       'div':div 

    }
    
    return context   






    