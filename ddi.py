import streamlit as st
from firebase_admin import firestore
import requests
from streamlit_lottie import st_lottie
import torch
import pickle
from transformers import BertTokenizer
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from Bio import Entrez
from firebase_admin import firestore

nltk.download('punkt')

#def app():
    #if 'db' not in st.session_state:
        #st.session_state.db = ''

    #db = firestore.client()
    #st.session_state.db = db

    #ph



# Initialize Firebase
# Add your Firebase credentials initialization here



def app():

    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    searching = load_lottieurl("https://lottie.host/e82b4d89-e326-415a-9cbd-b1d19b0ccdb9/ME1kJJbrH3.json")

    st_lottie(searching,
            height=200,
            width=200,
            speed=1,
            loop=True,
            quality='high')

    st.title('Drug-Drug Interactions')

    st.header("What is this about? 📑")

    st.write("This section provides the interaction class of the drugs mentioned.")

    st.write("A drug-drug interaction (DDI), also known as a drug interaction, occurs when two or more drugs interact with each other \
            in a way that affects their effectiveness or leads to adverse effects when taken together. \
            These interactions can occur when drugs are taken simultaneously or sequentially.")

    st.write("")
    st.write("")

    def text_rank_algorithm(text, drug1, drug2, top_n=4):
        # Step 1: Tokenize the document into sentences
        sentences = nltk.sent_tokenize(text)
        
        # Step 2: Build a similarity matrix using TF-IDF vectors and cosine similarity
        vectorizer = TfidfVectorizer().fit_transform(sentences)
        vectors = vectorizer.toarray()
        cosine_matrix = cosine_similarity(vectors)
        
        # Step 3: Use the PageRank algorithm
        nx_graph = nx.from_numpy_array(cosine_matrix)
        scores = nx.pagerank(nx_graph)
        
        # Step 4: Modify the scores to prioritize sentences containing the drugs
        drugs = [drug1, drug2]
        for i, s in enumerate(sentences):
            if any(drug in s for drug in drugs):
                scores[i] *= 1.5  # Increasing the score by 50% if the sentence contains the drug
        
        # Step 5: Rank the sentences
        ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
        
        # Step 6: Extract the top sentences for the summary
        summary = " ".join([ranked_sentences[i][1] for i in range(top_n)])
        
        return summary

    def fetch_pubmed_ddi_articles(drug1, drug2):
        Entrez.email = "your.email@example.com"  # Replace with your email

        # Construct the search term with "Humans"[Mesh] to ensure human-related articles
        term = f'("{drug1}"[Title/Abstract] AND "{drug2}"[Title/Abstract]) AND "Drug Interactions"[Mesh] AND "Humans"[Mesh]'

        # Search for the term in PubMed with retmax=5 to get only the top 5 articles
        handle = Entrez.esearch(db="pubmed", term=term, retmax=5)
        record = Entrez.read(handle)
        handle.close()

        article_ids = record["IdList"]
        if not article_ids:
            st.write(f"No articles found for the drug pair: {drug1} and {drug2}")
            return

        # Fetch details for each PubMed ID
        handle = Entrez.efetch(db="pubmed", id=",".join(article_ids), retmode="xml")
        records = Entrez.read(handle)
        handle.close()

        for article in records['PubmedArticle']:
            abstract = article['MedlineCitation']['Article'].get('Abstract', {}).get('AbstractText', [''])[0]

            # Only consider articles with abstracts longer than 100 characters
            if len(abstract) > 250:
                title = article['MedlineCitation']['Article'].get('ArticleTitle', '')
                authors = []
                if 'AuthorList' in article['MedlineCitation']['Article']:
                    for author in article['MedlineCitation']['Article']['AuthorList']:
                        last_name = author.get('LastName', '')
                        fore_name = author.get('ForeName', '')
                        authors.append(last_name + ' ' + fore_name)
                url = f"https://pubmed.ncbi.nlm.nih.gov/{article['MedlineCitation']['PMID']}/"

                st.write("Drugs:", drug1, "and", drug2)
                st.write("Title:", title)
                st.write("Authors:", ', '.join(authors))
                st.write("Abstract:", abstract)
                st.write("URL:", url)
                st.write("-" * 50)




    # Add the check for user authentication
    if 'username' not in st.session_state or not st.session_state.username:
        st.warning('Please log in to access this page.')
        return

    st.subheader("Please fill in the following details:")
    user_details = st.text_input("📃 Enter text")

    if not user_details:
        st.warning("Please enter the text.")

    st.subheader("Enter Drug Names")
    drug1 = st.text_input("💊 Drug 1")
    drug2 = st.text_input("💊 Drug 2")

    # Load the BERT tokenizer
    tokenizer = BertTokenizer.from_pretrained("monologg/biobert_v1.1_pubmed")

    # Load the saved model
    model_pkl_file = "bert_classifier_model.pkl"  # Replace with the actual path to your saved model
    with open(model_pkl_file, 'rb') as file:
        model = pickle.load(file)

    # Mapping of DDI classes to labels and descriptions
    labels = {0: 'advise', 1: 'effect', 2: 'int', 3: 'mechanism'}
    descriptions = {
        'mechanism': 'This type is used to annotate DDIs that are described by their PK mechanism (e.g. Grepafloxacin may inhibit the metabolism of theobromine).',
        'effect': 'This type is used to annotate DDIs describing an effect (e.g. In uninfected volunteers, 46% developed rash while receiving SUSTIVA and clarithromycin) or a PD mechanism (e.g. Chlorthalidone may potentiate the action of other antihypertensive drugs).',
        'advise': 'This type is used when a recommendation or advice regarding a drug interaction is given (e.g. UROXATRAL should not be used in combination with other alpha-blockers).',
        'int': 'This type is used when a DDI appears in the text without providing any additional information (e.g. The interaction of omeprazole and ketoconazole has been established).'
    }


    if st.button("Predict the DDI class!"):
        
        summary = text_rank_algorithm(user_details, drug1, drug2, top_n=4)
       
        if not (summary and drug1 and drug2):
            st.warning("Please fill in all the required details.")
        else:
            # Preprocess the user input
            text = [summary]

            # Tokenize and encode the input
            encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')

            # Forward pass to get the logits
            with torch.no_grad():
                outputs = model(**encoded_input)

            # Get the predicted probabilities
            probs = torch.softmax(outputs.logits, dim=1)

            # Get the predicted class for the input
            predicted_class = torch.argmax(probs).item()

            if predicted_class in labels:
                st.write(f"The predicted DDI class for the input is: {labels[predicted_class]}")
                st.write(f"Description: {descriptions[labels[predicted_class]]}")
                st.write(f"Summary: {summary}")
                st.divider()
                st.write("Recommended articles to refer to: ")
                fetch_pubmed_ddi_articles(drug1, drug2)

        # Store DDI result in Firestore
        # store_ddi_result_in_firestore(ddi_result)

        fetch_pubmed_ddi_articles(drug1, drug2)

    

# def store_ddi_result_in_firestore(ddi_result):
    # Add your Firestore collection and document reference
    # collection_name = "ddi_results"
    # document_id = f"{st.session_state.username}_{ddi_result['drug1']}_{ddi_result['drug2']}"

    # db = firestore.client()
    # doc_ref = db.collection(collection_name).document(document_id)
    # doc_ref.set(ddi_result)
