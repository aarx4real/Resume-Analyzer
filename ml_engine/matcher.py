from sentence_transformers import SentenceTransformer, util

# Load a lightweight, high-performance model
# 'all-MiniLM-L6-v2' is perfect for resumes: fast and accurate
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_similarity(job_description: str, resume_text: str) -> float:
    """
    Computes the semantic similarity score between JD and Resume.
    Returns a percentage (0 to 100).
    """
    # 1. Encode both texts into 'embeddings' (vectors)
    embeddings1 = model.encode(job_description, convert_to_tensor=True)
    embeddings2 = model.encode(resume_text, convert_to_tensor=True)
    
    # 2. Compute Cosine Similarity
    cosine_score = util.cos_sim(embeddings1, embeddings2)
    
    # 3. Convert to a standard float and round to 2 decimal places
    score = float(cosine_score)
    return round(score * 100, 2)