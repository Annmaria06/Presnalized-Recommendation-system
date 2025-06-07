import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    """Load the datasets"""
    try:
        ratings = pd.read_csv('data/ratings.csv')
        movies = pd.read_csv('data/movies.csv')
        users = pd.read_csv('data/users.csv')
        return ratings, movies, users
    except FileNotFoundError:
        print("Data files not found. Please run data_collection.py first.")
        return None, None, None

def clean_and_preprocess_data(ratings, movies, users):
    """Clean and preprocess the data"""
    print("Starting data preprocessing...")
    
    # Check for missing values
    print("Missing values in ratings:", ratings.isnull().sum().sum())
    print("Missing values in movies:", movies.isnull().sum().sum())
    print("Missing values in users:", users.isnull().sum().sum())
    
    # Remove any missing values
    ratings = ratings.dropna()
    movies = movies.dropna(subset=['item_id', 'title'])
    users = users.dropna(subset=['user_id'])
    
    # Ensure ratings are within valid range (1-5)
    ratings = ratings[(ratings['rating'] >= 1) & (ratings['rating'] <= 5)]
    
    # Remove users and items with very few interactions
    min_ratings_per_user = 5
    min_ratings_per_item = 5
    
    # Count ratings per user and item
    user_counts = ratings['user_id'].value_counts()
    item_counts = ratings['item_id'].value_counts()
    
    # Filter users and items
    valid_users = user_counts[user_counts >= min_ratings_per_user].index
    valid_items = item_counts[item_counts >= min_ratings_per_item].index
    
    ratings_filtered = ratings[
        (ratings['user_id'].isin(valid_users)) & 
        (ratings['item_id'].isin(valid_items))
    ]
    
    print(f"Original ratings: {len(ratings)}")
    print(f"Filtered ratings: {len(ratings_filtered)}")
    print(f"Users: {ratings_filtered['user_id'].nunique()}")
    print(f"Items: {ratings_filtered['item_id'].nunique()}")
    
    # Create user-item matrix
    user_item_matrix = ratings_filtered.pivot_table(
        index='user_id', 
        columns='item_id', 
        values='rating'
    ).fillna(0)
    
    print(f"User-item matrix shape: {user_item_matrix.shape}")
    print(f"Sparsity: {(user_item_matrix == 0).sum().sum() / (user_item_matrix.shape[0] * user_item_matrix.shape[1]):.4f}")
    
    # Save processed data
    ratings_filtered.to_csv('data/ratings_processed.csv', index=False)
    user_item_matrix.to_csv('data/user_item_matrix.csv')
    
    return ratings_filtered, user_item_matrix

def normalize_ratings(user_item_matrix):
    """Normalize ratings by subtracting user mean"""
    print("Normalizing ratings...")
    
    # Calculate user means (excluding zeros)
    user_means = []
    normalized_matrix = user_item_matrix.copy()
    
    for user_id in user_item_matrix.index:
        user_ratings = user_item_matrix.loc[user_id]
        non_zero_ratings = user_ratings[user_ratings > 0]
        
        if len(non_zero_ratings) > 0:
            user_mean = non_zero_ratings.mean()
            user_means.append(user_mean)
            
            # Subtract mean from non-zero ratings
            mask = user_ratings > 0
            normalized_matrix.loc[user_id, mask] = user_ratings[mask] - user_mean
        else:
            user_means.append(0)
    
    # Save user means for later use
    user_means_df = pd.DataFrame({
        'user_id': user_item_matrix.index,
        'mean_rating': user_means
    })
    user_means_df.to_csv('data/user_means.csv', index=False)
    
    normalized_matrix.to_csv('data/user_item_matrix_normalized.csv')
    
    print("Rating normalization completed!")
    return normalized_matrix, user_means_df

# Load and process data
ratings, movies, users = load_data()

if ratings is not None:
    ratings_processed, user_item_matrix = clean_and_preprocess_data(ratings, movies, users)
    normalized_matrix, user_means = normalize_ratings(user_item_matrix)
    print("Data preprocessing completed successfully!")
else:
    print("Please run data_collection.py first to generate the dataset.")
