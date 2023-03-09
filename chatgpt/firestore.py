import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./hedgehog-c9b07-gcloud-admin-key.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

def addSummary(article, summary):
  doc_ref = db.collection(u'summaries').document(article['stock_ticker']).collection('articles').document(article['title'])
  doc_ref.set({
      u'source': article['url'],
      u'title': article['title'],
      u'stock_ticker': article['stock_ticker'],
      u'pub_time': article['pub_time'],
      u'update_time': article['update_time'],
      u'summary': summary
  })