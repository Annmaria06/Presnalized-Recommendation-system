import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

def load_processed_data():
    """Load processed data"""
    try:
        ratings = pd.read_csv('data/ratings_processed.csv')
        user_item_matrix = pd.read_csv('data/user_item_matrix.csv', index_col=0)
        return ratings, user_item_matrix
    except FileNotFoundError:
        print("Processed data not found. Please run data_preprocessing.py first.")
        return None, None

def analyze_rating_distribution(ratings):
    """Analyze the distribution of ratings"""
    print("=== Rating Distribution Analysis ===")
    
    rating_counts = ratings['rating'].value_counts().sort_index()
    print("Rating distribution:")
    for rating, count in rating_counts.items():
        percentage = (count / len(ratings)) * 100
        print(f"Rating {rating}: {count} ({percentage:.1f}%)")
    
    # Calculate basic statistics
    print(f"\nRating Statistics:")
    print(f"Mean rating: {ratings['rating'].mean():.2f}")
    print(f"Median rating: {ratings['rating'].median():.2f}")
    print(f"Standard deviation: {ratings['rating'].std():.2f}")
    
    return rating_counts

def analyze_user_behavior(ratings):
    """Analyze user rating behavior"""
    print("\n=== User Behavior Analysis ===")
    
    # Ratings per user
    user_rating_counts = ratings['user_id'].value_counts()
    
    print(f"User Statistics:")
    print(f"Total users: {ratings['user_id'].nunique()}")
    print(f"Average ratings per user: {user_rating_counts.mean():.2f}")
    print(f"Median ratings per user: {user_rating_counts.median():.2f}")
    print(f"Max ratings by a user: {user_rating_counts.max()}")
    print(f"Min ratings by a user: {user_rating_counts.min()}")
    
    # User rating patterns
    user_avg_ratings = ratings.groupby('user_id')['rating'].mean()
    print(f"\nUser Rating Patterns:")
    print(f"Average user rating: {user_avg_ratings.mean():.2f}")
    print(f"Users who rate above 4.0: {(user_avg_ratings > 4.0).sum()}")
    print(f"Users who rate below 3.0: {(user_avg_ratings < 3.0).sum()}")
    
    return user_rating_counts, user_avg_ratings

def analyze_item_popularity(ratings):
    """Analyze item popularity"""
    print("\n=== Item Popularity Analysis ===")
    
    # Ratings per item
    item_rating_counts = ratings['item_id'].value_counts()
    
    print(f"Item Statistics:")
    print(f"Total items: {ratings['item_id'].nunique()}")
    print(f"Average ratings per item: {item_rating_counts.mean():.2f}")
    print(f"Median ratings per item: {item_rating_counts.median():.2f}")
    print(f"Most rated item: {item_rating_counts.max()} ratings")
    print(f"Least rated item: {item_rating_counts.min()} ratings")
    
    # Item rating quality
    item_avg_ratings = ratings.groupby('item_id')['rating'].mean()
    print(f"\nItem Quality Patterns:")
    print(f"Average item rating: {item_avg_ratings.mean():.2f}")
    print(f"Items rated above 4.0: {(item_avg_ratings > 4.0).sum()}")
    print(f"Items rated below 3.0: {(item_avg_ratings < 3.0).sum()}")
    
    # Popular items (most rated)
    top_items = item_rating_counts.head(10)
    print(f"\nTop 10 Most Rated Items:")
    for item_id, count in top_items.items():
        avg_rating = ratings[ratings['item_id'] == item_id]['rating'].mean()
        print(f"Item {item_id}: {count} ratings (avg: {avg_rating:.2f})")
    
    return item_rating_counts, item_avg_ratings

def analyze_sparsity(user_item_matrix):
    """Analyze matrix sparsity"""
    print("\n=== Sparsity Analysis ===")
    
    total_cells = user_item_matrix.shape[0] * user_item_matrix.shape[1]
    non_zero_cells = (user_item_matrix > 0).sum().sum()
    sparsity = 1 - (non_zero_cells / total_cells)
    
    print(f"Matrix dimensions: {user_item_matrix.shape}")
    print(f"Total possible ratings: {total_cells:,}")
    print(f"Actual ratings: {non_zero_cells:,}")
    print(f"Sparsity: {sparsity:.4f} ({sparsity*100:.2f}%)")
    
    # Analyze distribution of ratings per user and item
    ratings_per_user = (user_item_matrix > 0).sum(axis=1)
    ratings_per_item = (user_item_matrix > 0).sum(axis=0)
    
    print(f"\nRatings per user - Mean: {ratings_per_user.mean():.2f}, Std: {ratings_per_user.std():.2f}")
    print(f"Ratings per item - Mean: {ratings_per_item.mean():.2f}, Std: {ratings_per_item.std():.2f}")
    
    return sparsity

def generate_insights(ratings):
    """Generate key insights from the data"""
    print("\n=== Key Insights ===")
    
    # Rating bias analysis
    rating_bias = ratings['rating'].mean() - 3.0  # Assuming 3 is neutral
    if rating_bias > 0:
        print(f"Users tend to rate positively (bias: +{rating_bias:.2f})")
    else:
        print(f"Users tend to rate negatively (bias: {rating_bias:.2f})")
    
    # Power users and items
    user_counts = ratings['user_id'].value_counts()
    item_counts = ratings['item_id'].value_counts()
    
    power_users = user_counts[user_counts > user_counts.quantile(0.95)]
    popular_items = item_counts[item_counts > item_counts.quantile(0.95)]
    
    print(f"Power users (top 5%): {len(power_users)} users")
    print(f"Popular items (top 5%): {len(popular_items)} items")
    
    # Rating variance analysis
    user_rating_std = ratings.groupby('user_id')['rating'].std().fillna(0)
    item_rating_std = ratings.groupby('item_id')['rating'].std().fillna(0)
    
    print(f"Average user rating variance: {user_rating_std.mean():.2f}")
    print(f"Average item rating variance: {item_rating_std.mean():.2f}")
    
    # Recommendation challenges
    single_rating_users = (user_counts == 1).sum()
    single_rating_items = (item_counts == 1).sum()
    
    print(f"\nChallenges for recommendation:")
    print(f"Users with only 1 rating: {single_rating_users}")
    print(f"Items with only 1 rating: {single_rating_items}")

# Load data and perform EDA
ratings, user_item_matrix = load_processed_data()

if ratings is not None and user_item_matrix is not None:
    print("Starting Exploratory Data Analysis...")
    
    # Perform all analyses
    rating_dist = analyze_rating_distribution(ratings)
    user_stats = analyze_user_behavior(ratings)
    item_stats = analyze_item_popularity(ratings)
    sparsity = analyze_sparsity(user_item_matrix)
    generate_insights(ratings)
    
    print("\nExploratory Data Analysis completed!")
    
    # Save summary statistics
    summary_stats = {
        'total_ratings': len(ratings),
        'total_users': ratings['user_id'].nunique(),
        'total_items': ratings['item_id'].nunique(),
        'avg_rating': ratings['rating'].mean(),
        'sparsity': sparsity,
        'avg_ratings_per_user': ratings['user_id'].value_counts().mean(),
        'avg_ratings_per_item': ratings['item_id'].value_counts().mean()
    }
    
    summary_df = pd.DataFrame([summary_stats])
    summary_df.to_csv('data/summary_stats.csv', index=False)
    print("Summary statistics saved to data/summary_stats.csv")
    
else:
    print("Please run data_collection.py and data_preprocessing.py first.")
