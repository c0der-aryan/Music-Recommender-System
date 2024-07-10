from transformers import AutoTokenizer, AutoModel
import torch , ast

# Load pre-trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')


def sent_maker (sent): 
    sent = ast.literal_eval(sent)[:2]
    sent = ", ".join(sent)    
    return sent

def get_sentence_embedding(sentence):
    inputs = tokenizer(sentence, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    sentence_embedding = outputs.last_hidden_state[:, 0, :]
    return sentence_embedding

def cosine_similarity_genres(sentence1, sentence2):
    embedding1 = get_sentence_embedding(sent_maker(sentence1))
    embedding2 = get_sentence_embedding(sent_maker(sentence2))

    embedding1 = torch.nn.functional.normalize(embedding1, p=2, dim=1)
    embedding2 = torch.nn.functional.normalize(embedding2, p=2, dim=1)

    return torch.nn.functional.cosine_similarity(embedding1, embedding2)

# genres1 = "['classic bollywood', 'filmi']"
# genres2 = "['desi pop', 'filmi', 'modern bollywood', 'desi pop', 'filmi', 'modern bollywood']"

# similarity = cosine_similarity_genres(genres1, genres2)
# print(f"Cosine Similarity: {similarity.item()}")

# good if above 86%

# sentiments1 = "[0, 0, 0, 0, 0.4986305832862854, 0, 0]"
# sentiments2 = "[0, 0, 0, 0, 0.7067436575889587, 0, 0]"


# similarity = cosine_similarity_genres(sentiments1, sentiments2)
# print(f"Cosine Similarity: {similarity.item()}")

from scipy.spatial.distance import cosine

vec1 = [0, 0, 0, 0, 0.4986305832862854, 0, 0]
vec2 = [0, 0, 0, 0, 0.7067436575889587, 0, 0]

# # Cosine similarity is 1 - cosine distance
# similarity = 1 - cosine(vec1, vec2)
# print(f"Cosine Similarity: {similarity}")

import numpy as np

def euclidean_distance(vec1, vec2):
    return np.sqrt(np.sum((np.array(vec1) - np.array(vec2))**2))

vec1 = [0, 0, 0, 0, 0.4986305832862854, 0, 0]
vec2 = [0, 0, 0, 0, 0.2067436575889587, 0.2, 0]

import numpy as np

def pearson_correlation_sentiments (vec1, vec2):
    mean_vec1 = np.mean(vec1)
    mean_vec2 = np.mean(vec2)
    numerator = np.sum((np.array(vec1) - mean_vec1) * (np.array(vec2) - mean_vec2))
    denominator = np.sqrt(np.sum((np.array(vec1) - mean_vec1)**2)) * np.sqrt(np.sum((np.array(vec2) - mean_vec2)**2))
    return numerator / denominator

# correlation = pearson_correlation_sentiments(vec1, vec2)
# print(f"Pearson Correlation Coefficient: {correlation}")



set1 = ["hi", "mr"]
set2 = ["en" , "hi"]

languages = [
    "af", "als", "am", "an", "ar", "arz", "as", "ast", "av", "az", 
    "azb", "ba", "bar", "bcl", "be", "bg", "bh", "bn", "bo", "bpy", 
    "br", "bs", "bxr", "ca", "cbk", "ce", "ceb", "ckb", "co", "cs", 
    "cv", "cy", "da", "de", "diq", "dsb", "dty", "dv", "el", "eml", 
    "en", "eo", "es", "et", "eu", "fa", "fi", "fr", "frr", "fy", 
    "ga", "gd", "gl", "gn", "gom", "gu", "gv", "he", "hi", "hif", 
    "hr", "hsb", "ht", "hu", "hy", "ia", "id", "ie", "ilo", "io", 
    "is", "it", "ja", "jbo", "jv", "ka", "kk", "km", "kn", "ko", 
    "krc", "ku", "kv", "kw", "ky", "la", "lb", "lez", "li", "lmo", 
    "lo", "lrc", "lt", "lv", "mai", "mg", "mhr", "min", "mk", "ml", 
    "mn", "mr", "mrj", "ms", "mt", "mwl", "my", "myv", "mzn", "nah", 
    "nap", "nds", "ne", "new", "nl", "nn", "no", "oc", "or", "os", 
    "pa", "pam", "pfl", "pl", "pms", "pnb", "ps", "pt", "qu", "rm", 
    "ro", "ru", "rue", "sa", "sah", "sc", "scn", "sco", "sd", "sh", 
    "si", "sk", "sl", "so", "sq", "sr", "su", "sv", "sw", "ta", "te", 
    "tg", "th", "tk", "tl", "tr", "tt", "tyv", "ug", "uk", "ur", "uz", 
    "vec", "vep", "vi", "vls", "vo", "wa", "war", "wuu", "xal", "xmf", 
    "yi", "yo", "yue", "zh"
]

# def get_lang_vec (set1 , set2)  :
#     output = pipe(lrcs[:514])[0]
#     scores = {i["label"] :  i["score"] for i in output if i["score"]>0.1}
#     lst = ["anger" , "disgust" , "fear" , "joy" , "neutral" , "sadness" , "surprise"]
#     sentiments = [scores.get(key, 0) for key in lst]
#     languages = langs(lrcs)


def create_language_distribution_vector(word_set, languages):
    vector = [0.0] * len(languages)
    distribution_value = 1.0 / len(word_set)  # Even distribution across all words in word_set
    
    for word in word_set:
        if word in languages:
            index = languages.index(word)
            vector[index] = distribution_value
    
    return vector

# Example usage
language_vector1 = create_language_distribution_vector(set1, languages)
language_vector2 = create_language_distribution_vector(set2, languages)

euclidean_dist = euclidean_distance(language_vector2 , language_vector1)

# Convert Euclidean distance to similarity
similarity = 1 / (1 + euclidean_dist)
print(similarity)

def custom_similarity(vector1, vector2):
    # Initialize similarity score
    similarity_score = 0.0
    
    # Loop through each word in vector1
    for word1 in vector1:
        # Check if word1 is in vector2
        if word1 in vector2:
            # Increase similarity score when there's an exact match
            similarity_score += 1.0  # You can adjust the weight as needed
    
    # Normalize similarity score (optional)
    similarity_score /= max(len(vector1), len(vector2))  # Normalize by the maximum length of vectors
    
    return similarity_score


# Compute custom similarity
similarity = custom_similarity(set1, set2)
print(f"Custom Similarity between vector1 and vector2: {similarity}")
