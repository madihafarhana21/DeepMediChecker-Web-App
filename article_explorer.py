import streamlit as st
from Bio import Entrez


def app():

    st.title('PubMed Article Recommender')

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
            if len(abstract) > 100:
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
    
    drug1 = st.text_input('Enter Drug 1')
    drug2 = st.text_input('Enter Drug 2')

    if st.button('Recommend Articles'):
        fetch_pubmed_ddi_articles(drug1, drug2)
    


