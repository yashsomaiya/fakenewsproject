import pandas as pd
import numpy as np
from sklearn.metrics import *
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network.multilayer_perceptron import MLPClassifier



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


print("Setting up..")
cDict = loadCanonDict()
qs_Examples = ArticleExample.objects.filter(quality_class__lt = 5)

print("Processing examples")
(Y_vector, examplesMatrix) = processExamples(qs_Examples, cDict)


X_train, X_test, y_train, y_test = train_test_split(examplesMatrix, Y_vector, test_size=0.2)
#model = SVC(gamma='scale', probability = True)
#model = MLPClassifier(hidden_layer_sizes=(128,64,32,16,8), max_iter=2500)
model = LogisticRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)


print("***************")
print("Accuracy score: " + str(accuracy_score(predictions, y_test)))
print("Confusion Matrix: ")
print(confusion_matrix(predictions, y_test))
print("Classification report: ")
print(classification_report(predictions, y_test))
print("***************")

mae = mean_absolute_error(y_test, predictions)
print("Mean absolute Error:"+ str(mae))