import pandas as pd 
import numpy as np
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import pickle 


WF_SVC_Final = pickle.load(open('model.pkl', 'rb'))

coefficients = WF_SVC_Final.named_steps["svc"].coef_   #since svc is the name of the estimator we call it here