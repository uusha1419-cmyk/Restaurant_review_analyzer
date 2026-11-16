# Restaurant Review Analyzer

A web app that analyzes restaurant reviews and shows overall sentiment and category-level insights (food, service, cleanliness, waiting time).

## How it works
- **Sentiment:** pre-trained Hugging Face model (DistilBERT, SST-2)
- **Categories:** keyword rules find the sentences about each category, then the same model scores those sentences
- **Backend:** FastAPI
- **Frontend:** Streamlit

## Run locally
```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
In a second terminal:
```
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

## Limitations
- The model gives only positive or negative for each text
- Categories depend on a fixed keyword list