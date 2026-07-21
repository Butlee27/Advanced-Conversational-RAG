from sentence_transformers import CrossEncoder
from config import cross_encoder_model

def get_reranker():

    return CrossEncoder(cross_encoder_model)

def rerank_document(query,documents,top_k=3):
    reranker=get_reranker()

    sentence_pairs=[(query,doc.page_content) for doc in documents]

    scores=reranker.predict(sentence_pairs)

    ranked_docs=list(zip(documents,scores))

    ranked_docs.sort(
        key=lambda x:x[1],
        reverse=True
    )

    return [doc for doc,score in ranked_docs[:top_k]]
