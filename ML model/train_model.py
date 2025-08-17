import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

def train_model():
    print("Loading battle data...")
    df = pd.read_csv('battle_data.csv')

    # --- Feature Engineering & Preprocessing ---
    print("Preprocessing data...")
    
    # Handle missing Type 2 data
    df['p1_Type 2'].fillna('None', inplace=True)
    df['p2_Type 2'].fillna('None', inplace=True)

    # Encode categorical features (Pokémon types)
    # We create one encoder and fit it on all possible types to ensure consistency
    all_types = pd.concat([df['p1_Type 1'], df['p1_Type 2'], df['p2_Type 1'], df['p2_Type 2']]).unique()
    type_encoder = LabelEncoder().fit(all_types)
    
    df['p1_Type 1_encoded'] = type_encoder.transform(df['p1_Type 1'])
    df['p1_Type 2_encoded'] = type_encoder.transform(df['p1_Type 2'])
    df['p2_Type 1_encoded'] = type_encoder.transform(df['p2_Type 1'])
    df['p2_Type 2_encoded'] = type_encoder.transform(df['p2_Type 2'])
    
    # Define features (X) and target (y)
    features = [
        'p1_HP', 'p1_Attack', 'p1_Defense', 'p1_Speed', 'p1_Type 1_encoded', 'p1_Type 2_encoded',
        'p2_HP', 'p2_Attack', 'p2_Defense', 'p2_Speed', 'p2_Type 1_encoded', 'p2_Type 2_encoded'
    ]
    target = 'Winner'

    X = df[features]
    y = df[target]
    
    # --- Model Training ---
    print("Splitting data and training model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # We'll use a RandomForestClassifier, which is great for this kind of task
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # --- Evaluation ---
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    
    # --- Saving the Model and Encoder ---
    print("Saving model and type encoder...")
    joblib.dump(model, 'battle_predictor.pkl')
    joblib.dump(type_encoder, 'type_encoder.pkl')
    
    print("Training complete. 'battle_predictor.pkl' and 'type_encoder.pkl' have been saved.")

if __name__ == "__main__":
    train_model()
