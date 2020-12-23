from sentence_transformers import SentenceTransformer
import scipy
embedder = SentenceTransformer('roberta-large-nli-stsb-mean-tokens')


# current_input = from_amt 

threshold = 0.75
kb = []
# kb.append(current_input)
kb_embeddings = embedder.encode(kb)
current_input_embeddings = embedder.encode(current_input)

#cosine similarity score
dist = scipy.spatial.distance.cdist([current_input_embeddings], kb_embeddings, "cosine")[0]
sim_score = 1 - dist


