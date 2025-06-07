import pandas as pd
import numpy as np
import requests
import zipfile
import os
from io import BytesIO

def download_movielens_data():
    """Download and extract MovieLens 100K dataset"""
    print("Downloading MovieLens 100K dataset...")
    
    # MovieLens 100K dataset URL
    url = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Extract the zip file
        with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
            zip_file.extractall("data/")
        
        print("Dataset downloaded and extracted successfully!")
        
        # Load the main datasets
        ratings = pd.read_csv('data/ml-100k/u.data', sep='\t', 
                            names=['user_id', 'item_id', 'rating', 'timestamp'])
        
        movies = pd.read_csv('data/ml-100k/u.item', sep='|', encoding='latin-1',
                           names=['item_id', 'title', 'release_date', 'video_release_date',
                                 'imdb_url', 'unknown', 'Action', 'Adventure', 'Animation',
                                 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama',
                                 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
                                 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'])
        
        users = pd.read_csv('data/ml-100k/u.user', sep='|',
                          names=['user_id', 'age', 'gender', 'occupation', 'zip_code'])
        
        # Save as CSV for easier access
        ratings.to_csv('data/ratings.csv', index=False)
        movies.to_csv('data/movies.csv', index=False)
        users.to_csv('data/users.csv', index=False)
        
        print(f"Ratings shape: {ratings.shape}")
        print(f"Movies shape: {movies.shape}")
        print(f"Users shape: {users.shape}")
        
        return ratings, movies, users
        
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        return None, None, None

def create_sample_dataset():
    """Create a sample dataset for demonstration"""
    print("Creating sample dataset...")
    
    np.random.seed(42)
    
    # Generate sample data
    n_users = 1000
    n_items = 500
    n_ratings = 10000
    
    user_ids = np.random.randint(1, n_users + 1, n_ratings)
    item_ids = np.random.randint(1, n_items + 1, n_ratings)
    ratings = np.random.choice([1, 2, 3, 4, 5], n_ratings, p=[0.1, 0.1, 0.2, 0.3, 0.3])
    timestamps = np.random.randint(1000000000, 1600000000, n_ratings)
    
    # Create ratings dataframe
    ratings_df = pd.DataFrame({
        'user_id': user_ids,
        'item_id': item_ids,
        'rating': ratings,
        'timestamp': timestamps
    })
    
    # Remove duplicates (same user rating same item multiple times)
    ratings_df = ratings_df.drop_duplicates(subset=['user_id', 'item_id'])
    
    # Create movies dataframe
    movies_df = pd.DataFrame({
        'item_id': range(1, n_items + 1),
        'title': [f'Movie {i}' for i in range(1, n_items + 1)],
        'genre': np.random.choice(['Action', 'Comedy', 'Drama', 'Horror', 'Romance'], n_items)
    })
    
    # Create users dataframe
    users_df = pd.DataFrame({
        'user_id': range(1, n_users + 1),
        'age': np.random.randint(18, 65, n_users),
        'gender': np.random.choice(['M', 'F'], n_users)
    })
    
    # Save datasets
    os.makedirs('data', exist_ok=True)
    ratings_df.to_csv('data/ratings.csv', index=False)
    movies_df.to_csv('data/movies.csv', index=False)
    users_df.to_csv('data/users.csv', index=False)
    
    print(f"Sample dataset created!")
    print(f"Ratings: {len(ratings_df)} records")
    print(f"Movies: {len(movies_df)} records")
    print(f"Users: {len(users_df)} records")
    
    return ratings_df, movies_df, users_df

# Try to download MovieLens data, fallback to sample data
ratings, movies, users = download_movielens_data()

if ratings is None:
    print("Falling back to sample dataset...")
    ratings, movies, users = create_sample_dataset()

print("Data collection completed!")
