
from django.http import HttpResponse, JsonResponse
from .utils import assetsUtil
from django.shortcuts import render



# Create your views here.
def getAssets(request):
  listMetric= assetsUtil.getAssets() 
  return render(request, 'indicadores.html',{'assets': listMetric})
  #return HttpResponse(listMetric)


def home(request):
  return render(request, 'home.html')

def graficos(request):
  context= assetsUtil.grafica('btc')
  return render(request, 'graficos.html', context)

def coin_detail(request,symbol):
  coin_detail= assetsUtil.coin_detail(symbol)
  return render(request, 'coin_detail.html',{'coin_detail': coin_detail})
  #return HttpResponse(JsonResponse(coin_detail))


def graficos1(request,symbol):
  context= assetsUtil.grafica(symbol)
  print(context.get('div'))
  return HttpResponse({context.get('div'),context.get('script')})