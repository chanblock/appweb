
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
  return render(request, 'graficos.html')

def coin_detail(request,symbol,date):
  coin_detail= assetsUtil.coin_detail(symbol,date)
  return render(request, 'coin_detail.html',{'coin_detail': coin_detail})
  #return HttpResponse(JsonResponse(coin_detail))