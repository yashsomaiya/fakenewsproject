import pickle
import numpy as np
import os, sys, re, time

proj_path = 'e:/fakenews'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fakenews.settings')
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.contrib.gis.views import feed
from fakebot.models import *
from fakebot.utils import *
from fakebot.strainer import *



#Method:
# 1. Load the models from disk
print("Loading brain...")
#log_model = pickle.load(open('fakebot/log_model.sav', 'rb'))
#svc_model = pickle.load(open('fakebot/svc_model.sav', 'rb'))
mlp_model = pickle.load(open('fakebot/MLPC_model.sav', 'rb'))
print("Brain load successful.")


# 2. Use SoupStrainer to get the URL and process the article
print("Initializing dictionaries...")
cDict = loadCanonDict()
ss = SoupStrainer()
ss.init()

# 3. Get user input to get a URL
url = input("URL to analyze: ")

print("Attempting URL: " + url)
if(ss.loadAddress(url)):
    articleX = buildExampleRow(ss.extractText, cDict)
else:
    print("Error on URL, exiting")
    exit(0)

articleX = articleX.reshape(1, -1)

# 5. Send the X row to the model to produce a prediction

#log_prediction = log_model.predict(articleX)
#log_probabilities = log_model.predict_proba(articleX)

#svc_prediction = svc_model.predict(articleX)
#svc_probabilities = svc_model.predict_proba(articleX)

mlp_prediction = mlp_model.predict(articleX)
mlp_probabilities = mlp_model.predict_proba(articleX)

# 6. Display the processed text and the results
'''print("*** SVC ")
print("Prediction on this article is: ")
print(svc_prediction)
print("Probabilities:")
print(svc_probabilities)'''

'''print("*** Logistic ")
print("Prediction on this article is: ")
print(log_prediction)
print("Probabilities:")
print(log_probabilities)
'''
print("*** MLP ")
print("Prediction on this article is: ")
print(mlp_prediction)
print("Probabilities:")
print(mlp_probabilities)

