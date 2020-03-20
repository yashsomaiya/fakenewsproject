from django.shortcuts import render
import pandas as pd
import numpy as np
import pickle


import os, sys, re, time

proj_path = 'e:/fakenews'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fakenews.settings')
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from fakebot.models import *
#from fakebot.forms import *
from fakebot.strainer import *
from fakebot.utils import *

def index(request):

    url = request.GET.get('u')
    
    if((url is not None) and (len(url) > 5)):
        print("Setting up")
        #svc_model = pickle.load(open('fakebot/svc_model.sav', 'rb'))
        mlp_model = pickle.load(open('fakebot/MLPC_model.sav', 'rb'))
        log_model = pickle.load(open('fakebot/log_model.sav', 'rb'))
        cDict = loadCanonDict()        
        ss = SoupStrainer()
        ss.init()
        print("Setup complete")
        print("Attempting URL: " + url)
        if(ss.loadAddress(url)):
            articleX = buildExampleRow(ss.extractText, cDict)
        else:
            print("Error on URL, exiting")
            return render(request, 'urlFail.html', {'URL', url})

        articleX = articleX.reshape(1, -1)


        #svc_prediction = svc_model.predict(articleX)
        #svc_probabilities = svc_model.predict_proba(articleX)'''
 
        mlp_prediction = mlp_model.predict(articleX)
        mlp_probabilities = mlp_model.predict_proba(articleX)
 
        log_prediction = log_model.predict(articleX)
        log_probabilities = log_model.predict_proba(articleX)
    
        mlp_prb = (mlp_probabilities[0][0]*100, mlp_probabilities[0][1]*100, mlp_probabilities[0][2]*100, mlp_probabilities[0][3]*100)
        mlp_totFake = (mlp_probabilities[0][0]*100) + (mlp_probabilities[0][1]*100)
        mlp_totReal = (mlp_probabilities[0][2]*100) + (mlp_probabilities[0][3]*100)

        log_prb = (log_probabilities[0][0]*100, log_probabilities[0][1]*100, log_probabilities[0][2]*100, log_probabilities[0][3]*100)
        log_totFake = (log_probabilities[0][0]*100) + (log_probabilities[0][1]*100)
        log_totReal = (log_probabilities[0][2]*100) + (log_probabilities[0][3]*100)
        
        fin_prb = ( (((mlp_probabilities[0][0]*100)+(log_probabilities[0][0]*100))/2), 
                    (((mlp_probabilities[0][1]*100)+(log_probabilities[0][1]*100))/2),
                    (((mlp_probabilities[0][2]*100)+(log_probabilities[0][2]*100))/2),
                    (((mlp_probabilities[0][3]*100)+(log_probabilities[0][3]*100))/2) )
        fin_totFake = (mlp_totFake + log_totFake)/2
        fin_totReal = (mlp_totReal + log_totReal)/2

        context = {'headline':ss.recHeadline, 'words': ss.extractText, 'url' : url,
         #         ''''svc_totFake': svc_totFake, 
          #        'svc_totReal': svc_totReal, 
           #       'svc_prediction': svc_prediction, 
                  #'svc_probabilities': svc_prb, 
                  'mlp_totFake': mlp_totFake, 
                  'mlp_totReal': mlp_totReal, 
                  'mlp_prediction': mlp_prediction, 
                  'mlp_probabilities': mlp_prb,
                  'log_totFake': log_totFake, 
                  'log_totReal': log_totReal, 
                  'log_prediction': log_prediction, 
                  'log_probabilities': log_prb,
                  'fin_totFake': fin_totFake, 
                  'fin_totReal': fin_totReal, 
                  'fin_probabilities': fin_prb
                  }
 




      
        return render(request, 'fakebot/results.html', context)
    else:
        return render(request, 'fakebot/urlForm.html')