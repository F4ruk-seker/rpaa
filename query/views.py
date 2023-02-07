import json
import pickle
import pandas as pd

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import JsonResponse

from .forms import ManyQueryForm

# Create your views here.
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

file_dict = "TrainData.sav"
analyzer = pickle.load(open(file_dict, 'rb'))


class MainPage(View):
    def get(self,request):
        return render(request,'index.html')

    def post(self,request):
        text = request.POST.get('analizetext',None)
        result = None
        if text:
            Query = pd.Series(text)
            Result = analyzer.predict(Query)
            result = Result[0]
        return render(request,'index.html',context={'result':result,'comment':text})


class ManyQuery(View):
    def get(self,request):
        return render(request, 'many-query.html',context={'ManyQueryForm':ManyQueryForm,'result':[]})


    def post(self,request,*args,**kwargs):
        result_type_list = [
            {'result_name': 'GÜÇLÜ',
             'counter': 0},
            {'result_name': 'İÇTEN',
             'counter': 0},
            {'result_name': 'YETKİNLİK',
             'counter': 0},
            {'result_name': 'OLUMSUZ',
             'counter': 0},
            {'result_name': 'HEYECAN',
             'counter': 0},
        ]
        query_list = request.POST.getlist('query_list',None)
        RESULT_LIST = []

        if query_list:

            def counter_result(result):
                for result_obj in result_type_list:
                    if result_obj['result_name'] == result:
                         result_obj['counter'] += 1


            for query in json.loads(query_list[0]):
                if query.get('result',None):
                    """
                    kullanıcılar arka arkaya sorgu yapabiliyor 
                    soru sayısı artıkça zaten cevaplanmış soruları tekrar hesaplamadan
                    geri yolluyoruz böylece zaman kazanıcaz
                    """
                    __result = query.get('result',None)
                    RESULT_LIST.append({
                        'query':query.get('query',None),
                        'result':__result
                    })
                    counter_result(__result)
                else:
                    Query = pd.Series(query.get('query',None))
                    Result = analyzer.predict(Query)

                    ragno = {
                        'query':query.get('query',None),
                        'result':Result[0]
                    }
                    RESULT_LIST.append(ragno)
                    counter_result(Result[0])

        # ençok ağır basan sounç
        max_count = 0
        max_result_type = ""

        for bit in result_type_list:
            if bit["counter"] > max_count:
                max_count = bit["counter"]
                max_result_type = bit["result_name"]

        return render(request, 'many-query.html',
                      context={'ManyQueryForm':ManyQueryForm,'result':RESULT_LIST,'result_count':result_type_list,'max_result':{'result_name':max_result_type,'counter':max_count}
                               })

