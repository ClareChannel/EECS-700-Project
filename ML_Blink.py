import spacy
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# Load spacy's small English model for tokenization
nlp = spacy.load("en_core_web_sm")

# Sample training data (with labels)
TRAINING_DATA = [
    ("John Doe's email is john.doe@example.com and phone is 123-456-7890.", 
     [("John", "name"), ("Doe", "name"), ("john.doe@example.com", "email"), ("123-456-7890", "phone")]),
    ("Contact Jane Smith at jane.smith@domain.com or (321) 654-9870.", 
     [("Jane", "name"), ("Smith", "name"), ("jane.smith@domain.com", "email"), ("(321) 654-9870", "phone")])
]

# Feature extraction function: Convert tokens into features
def extract_features(doc):
    features = []
    for token in doc:
        token_features = {
            'text': token.text,
            'is_alpha': token.is_alpha,
            'is_digit': token.is_digit,
            'is_title': token.is_title,
            'shape': token.shape_,
            'prefix': token.prefix_,
            'suffix': token.suffix_,
            'length': len(token)
        }
        features.append(token_features)
    return features

# Prepare training data
def prepare_data(training_data):
    X, y = [], []
    for sentence, labels in training_data:
        doc = nlp(sentence)
        features = extract_features(doc)
        
        label_idx = 0
        for i, token in enumerate(doc):
            if label_idx < len(labels) and token.text == labels[label_idx][0]:
                y.append(labels[label_idx][1])
                label_idx += 1
            else:
                y.append("other")
            X.append(features[i])
    return X, y

# Train classifier using Decision Tree
def train_classifier(X, y):
    vectorizer = DictVectorizer(sparse=False)
    classifier = DecisionTreeClassifier()
    
    # Pipeline for vectorizing features and training the classifier
    clf_pipeline = Pipeline([
        ('vectorizer', vectorizer),
        ('classifier', classifier)
    ])
    
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Fit the model
    clf_pipeline.fit(X_train, y_train)
    
    # Print the accuracy
    accuracy = clf_pipeline.score(X_test, y_test)
    print(f"Training complete. Model accuracy: {accuracy * 100:.2f}%")
    
    return clf_pipeline

# Predict using trained model
def predict(text, clf_pipeline):
    doc = nlp(text)
    features = extract_features(doc)
    
    # Make predictions for each token
    predictions = clf_pipeline.predict(features)
    
    # Extract the relevant parts based on predictions
    extracted_info = {"name": [], "email": [], "phone": []}
    for token, label in zip(doc, predictions):
        if label in extracted_info:
            extracted_info[label].append(token.text)
    
    # Join multi-token names, etc.
    extracted_info["name"] = " ".join(extracted_info["name"]) if extracted_info["name"] else None
    extracted_info["email"] = " ".join(extracted_info["email"]) if extracted_info["email"] else None
    extracted_info["phone"] = " ".join(extracted_info["phone"]) if extracted_info["phone"] else None
    
    return extracted_info

# Prepare training data
X, y = prepare_data(TRAINING_DATA)

# Train the classifier
clf_pipeline = train_classifier(X, y)

# Example usage with a new input
input_text = "Reach out to Sarah Connor at sarah.connor@future.net or 555-867-5309."
extracted_info = predict(input_text, clf_pipeline)

print(extracted_info)
