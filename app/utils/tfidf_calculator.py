def compute_idf(inv_idx, n_docs, min_df=10, max_df_ratio=0.95):
   '''
   Computes the idfs of all the terms

    pls return a dict and save it in a pkl file

   :param inv_idx: Not actually needed, just read the files from app/utils/data
   :param n_docs: Not actually needed, just read the n_docs file from app/utils/data
   '''
  None

def compute_doc_norms(index, idf, n_docs):
  '''
   Computes the doc_norms of all the documents

   build it into a dict and save it as a pkl file

   :param index: Loop thru all the json files and grab comment_ids and comments (look at how i do this in other docs like vectorizerv2.py)
   :param idf: dict of all the idfs, dont need this, just read a pkl file
   '''