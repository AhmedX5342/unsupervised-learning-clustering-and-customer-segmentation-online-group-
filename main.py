import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

df = pd.read_excel('./online+retail/Online Retail.xlsx')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

features = df[['InvoiceNo', 'Quantity', 'UnitPrice', 'Country']].copy()

features[['Quantity', 'UnitPrice']] = features[['Quantity', 'UnitPrice']].apply(pd.to_numeric, errors='coerce')
features['InvoiceNo'] = pd.to_numeric(features['InvoiceNo'], errors='coerce')

features.dropna(subset=['InvoiceNo', 'Quantity', 'UnitPrice', 'Country'], inplace=True)
features = features[(features['Quantity'] > 0) & (features['UnitPrice'] > 0)]
features['InvoiceNo'] = features['InvoiceNo'].astype(int)
features['Total'] = features['Quantity'] * features['UnitPrice']
invoice_freq = features['InvoiceNo'].value_counts()
features['Frequency'] = features['InvoiceNo'].map(invoice_freq)

print(features.head())