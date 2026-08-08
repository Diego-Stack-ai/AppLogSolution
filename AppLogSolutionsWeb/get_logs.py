import os
import datetime
from google.cloud import logging

# Imposta le credenziali prima di importare client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'H:\Il mio Drive\App\AppLogSolutionsWeb\cantiere_key.json'

client = logging.Client(project='log-solutions-cantiere')
filter_str = 'resource.type="cloud_run_revision" AND resource.labels.service_name="elabora-centro-costi"'

print("Recupero gli ultimi log...")
for entry in client.list_entries(filter_=filter_str, order_by=logging.DESCENDING, max_results=20):
    print(f"[{entry.timestamp}] {entry.severity}: {entry.payload}")
