import json
import pickle
import pandas as pd

from django.shortcuts import render
from django.views.generic import View

from .forms import ManyQueryForm
from matplotlib import pyplot as plt
from pages.models import MianPage
import time

# Create your views here.
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

file_dict = "TrainData.sav"
analyzer = pickle.load(open(file_dict, 'rb'))


class MainPage(View):

    def get(self,request):
        return render(request,'index.html',context={'page':MianPage.objects.first()})

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
        progress_start_time = time.time()
        result_type_list = {
            'GÜÇLÜLÜK': 0,
            'İÇTEN': 0,
            'YETKİNLİK': 0,
            'OLUMSUZ': 0,
            'HEYECAN': 0,
        }
        query_list = request.POST.getlist('query_list',None)
        RESULT_LIST = []

        if query_list:
            def counter_result(result):
                for result_name,result_counter in result_type_list.items():
                    if result_name == result:
                         result_type_list[result_name] += 1


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

        for bit,count in result_type_list.items():
            if count > max_count:
                max_count = count
                max_result_type = bit
        progress_end_time = time.time()
        return render(request, 'many-query.html',
                      context={'ManyQueryForm':ManyQueryForm,'result':RESULT_LIST,'result_count':result_type_list,
                               'max_result':{'result_name':max_result_type,'counter':max_count},
                               'result_sum':sum(result_type_list.values()),
                               'passing_time':progress_end_time-progress_start_time,
                               })

