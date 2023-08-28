import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')

# Sample correct answer and student answer
correct_answer = "The capital of France is Paris."
student_answer = "Germany is not the capital of Mexico."

# Preprocess the text data
def preprocess_text(text):
    words = nltk.word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stopwords.words('english')]
    return ' '.join(words)

def evaluateQ(correct_answer, student_answer):
    # Preprocess the text data
    preprocessed_correct = preprocess_text(correct_answer)
    preprocessed_student = preprocess_text(student_answer)

    # Vectorize the text using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([preprocessed_correct, preprocessed_student])

    # Calculate cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

    # Print the cosine similarity
    print("Cosine Similarity:", cosine_sim)
    
    if cosine_sim > 0.5:
        return True
    else:
        return False
print(evaluateQ(correct_answer, student_answer))