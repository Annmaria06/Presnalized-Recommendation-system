import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error, mean_absolute_error
from scipy.sparse import csr_matrix
import pickle

class UserBasedCollaborativeFiltering:
    def __init__(self, n_neighbors=50):
        self.n_neighbors = n_neighbors
        self.user_similarity = None
        self.user_item_matrix = None
        self.user_means = None
        
    def fit(self, user_item_matrix, user_means=None):
        """Fit the user-based collaborative filtering model"""
        print("Training User-Based Collaborative Filtering...")
        
        self.user_item_matrix = user_item_matrix
        
        # Load or calculate user means
        if user_means is not None:
            self.user_means = user_means.set_index('user_id')['mean_rating']
        else:
            # Calculate user means for non-zero ratings
            user_means_dict = {}
            for user_id in user_item_matrix.index:
                user_ratings = user_item_matrix.loc[user_id]
                non_zero_ratings = user_ratings[user_ratings > 0]
                user_means_dict[user_id] = non_zero_ratings.mean() if len(non_zero_ratings) > 0 else 0
            self.user_means = pd.Series(user_means_dict)
        
        # Calculate user similarity matrix
        # Use only users who have rated items
        active_users_mask = (user_item_matrix > 0).sum(axis=1) > 0
        active_users = user_item_matrix[active_users_mask]
        
        print(f"Calculating similarity for {len(active_users)} active users...")
        
        # Calculate cosine similarity
        self.user_similarity = cosine_similarity(active_users)
        self.user_similarity = pd.DataFrame(
            self.user_similarity, 
            index=active_users.index, 
            columns=active_users.index
        )
        
        print("User-Based CF model trained successfully!")
        
    def predict(self, user_id, item_id):
        """Predict rating for a user-item pair"""
        if user_id not in self.user_item_matrix.index:
            return self.user_means.mean()  # Global average for new users
            
        if item_id not in self.user_item_matrix.columns:
            return self.user_means[user_id]  # User average for new items
        
        # Get similar users
        if user_id not in self.user_similarity.index:
            return self.user_means[user_id]
            
        user_similarities = self.user_similarity.loc[user_id]
        
        # Find users who have rated this item
        item_raters = self.user_item_matrix[self.user_item_matrix[item_id] > 0].index
        
        # Get similarities for users who rated this item
        relevant_similarities = user_similarities[user_similarities.index.isin(item_raters)]
        relevant_similarities = relevant_similarities[relevant_similarities.index != user_id]
        
        if len(relevant_similarities) == 0:
            return self.user_means[user_id]
        
        # Get top N similar users
        top_similar_users = relevant_similarities.nlargest(self.n_neighbors)
        
        if len(top_similar_users) == 0 or top_similar_users.sum() == 0:
            return self.user_means[user_id]
        
        # Calculate weighted average
        numerator = 0
        denominator = 0
        
        for similar_user_id, similarity in top_similar_users.items():
            if similarity > 0:
                similar_user_rating = self.user_item_matrix.loc[similar_user_id, item_id]
                similar_user_mean = self.user_means[similar_user_id]
                
                numerator += similarity * (similar_user_rating - similar_user_mean)
                denominator += abs(similarity)
        
        if denominator == 0:
            return self.user_means[user_id]
        
        predicted_rating = self.user_means[user_id] + (numerator / denominator)
        
        # Ensure rating is within valid range
        return max(1, min(5, predicted_rating))
    
    def recommend(self, user_id, n_recommendations=10):
        """Recommend items for a user"""
        if user_id not in self.user_item_matrix.index:
            return []
        
        user_ratings = self.user_item_matrix.loc[user_id]
        unrated_items = user_ratings[user_ratings == 0].index
        
        predictions = []
        for item_id in unrated_items:
            pred_rating = self.predict(user_id, item_id)
            predictions.append((item_id, pred_rating))
        
        # Sort by predicted rating and return top N
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:n_recommendations]

class ItemBasedCollaborativeFiltering:
    def __init__(self, n_neighbors=50):
        self.n_neighbors = n_neighbors
        self.item_similarity = None
        self.user_item_matrix = None
        
    def fit(self, user_item_matrix):
        """Fit the item-based collaborative filtering model"""
        print("Training Item-Based Collaborative Filtering...")
        
        self.user_item_matrix = user_item_matrix
        
        # Transpose matrix to get item-user matrix
        item_user_matrix = user_item_matrix.T
        
        # Use only items that have been rated
        active_items_mask = (item_user_matrix > 0).sum(axis=1) > 0
        active_items = item_user_matrix[active_items_mask]
        
        print(f"Calculating similarity for {len(active_items)} active items...")
        
        # Calculate cosine similarity
        self.item_similarity = cosine_similarity(active_items)
        self.item_similarity = pd.DataFrame(
            self.item_similarity,
            index=active_items.index,
            columns=active_items.index
        )
        
        print("Item-Based CF model trained successfully!")
        
    def predict(self, user_id, item_id):
        """Predict rating for a user-item pair"""
        if user_id not in self.user_item_matrix.index:
            # Return global average for new users
            all_ratings = self.user_item_matrix[self.user_item_matrix > 0]
            return all_ratings.mean().mean()
            
        if item_id not in self.user_item_matrix.columns:
            # Return user average for new items
            user_ratings = self.user_item_matrix.loc[user_id]
            user_ratings = user_ratings[user_ratings > 0]
            return user_ratings.mean() if len(user_ratings) > 0 else 3.0
        
        # Get similar items
        if item_id not in self.item_similarity.index:
            user_ratings = self.user_item_matrix.loc[user_id]
            user_ratings = user_ratings[user_ratings > 0]
            return user_ratings.mean() if len(user_ratings) > 0 else 3.0
            
        item_similarities = self.item_similarity.loc[item_id]
        
        # Find items that this user has rated
        user_ratings = self.user_item_matrix.loc[user_id]
        rated_items = user_ratings[user_ratings > 0].index
        
        # Get similarities for items the user has rated
        relevant_similarities = item_similarities[item_similarities.index.isin(rated_items)]
        relevant_similarities = relevant_similarities[relevant_similarities.index != item_id]
        
        if len(relevant_similarities) == 0:
            user_ratings_nonzero = user_ratings[user_ratings > 0]
            return user_ratings_nonzero.mean() if len(user_ratings_nonzero) > 0 else 3.0
        
        # Get top N similar items
        top_similar_items = relevant_similarities.nlargest(self.n_neighbors)
        
        if len(top_similar_items) == 0 or top_similar_items.sum() == 0:
            user_ratings_nonzero = user_ratings[user_ratings > 0]
            return user_ratings_nonzero.mean() if len(user_ratings_nonzero) > 0 else 3.0
        
        # Calculate weighted average
        numerator = 0
        denominator = 0
        
        for similar_item_id, similarity in top_similar_items.items():
            if similarity > 0:
                user_rating_for_similar_item = self.user_item_matrix.loc[user_id, similar_item_id]
                numerator += similarity * user_rating_for_similar_item
                denominator += abs(similarity)
        
        if denominator == 0:
            user_ratings_nonzero = user_ratings[user_ratings > 0]
            return user_ratings_nonzero.mean() if len(user_ratings_nonzero) > 0 else 3.0
        
        predicted_rating = numerator / denominator
        
        # Ensure rating is within valid range
        return max(1, min(5, predicted_rating))
    
    def recommend(self, user_id, n_recommendations=10):
        """Recommend items for a user"""
        if user_id not in self.user_item_matrix.index:
            return []
        
        user_ratings = self.user_item_matrix.loc[user_id]
        unrated_items = user_ratings[user_ratings == 0].index
        
        predictions = []
        for item_id in unrated_items:
            pred_rating = self.predict(user_id, item_id)
            predictions.append((item_id, pred_rating))
        
        # Sort by predicted rating and return top N
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:n_recommendations]

def evaluate_model(model, test_data):
    """Evaluate model performance"""
    print("Evaluating model performance...")
    
    predictions = []
    actuals = []
    
    for _, row in test_data.iterrows():
        user_id = row['user_id']
        item_id = row['item_id']
        actual_rating = row['rating']
        
        predicted_rating = model.predict(user_id, item_id)
        
        predictions.append(predicted_rating)
        actuals.append(actual_rating)
    
    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(actuals, predictions))
    mae = mean_absolute_error(actuals, predictions)
    
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")
    
    return rmse, mae

def train_and_evaluate_models():
    """Train and evaluate both collaborative filtering models"""
    
    # Load data
    try:
        user_item_matrix = pd.read_csv('data/user_item_matrix.csv', index_col=0)
        ratings = pd.read_csv('data/ratings_processed.csv')
        
        try:
            user_means = pd.read_csv('data/user_means.csv')
        except FileNotFoundError:
            user_means = None
            
    except FileNotFoundError:
        print("Required data files not found. Please run previous scripts first.")
        return
    
    # Split data for evaluation (80-20 split)
    np.random.seed(42)
    train_indices = np.random.choice(len(ratings), size=int(0.8 * len(ratings)), replace=False)
    test_indices = np.setdiff1d(np.arange(len(ratings)), train_indices)
    
    train_data = ratings.iloc[train_indices]
    test_data = ratings.iloc[test_indices]
    
    print(f"Training data: {len(train_data)} ratings")
    print(f"Test data: {len(test_data)} ratings")
    
    # Create training matrix
    train_matrix = train_data.pivot_table(
        index='user_id', 
        columns='item_id', 
        values='rating'
    ).fillna(0)
    
    # Ensure same dimensions as original matrix
    train_matrix = train_matrix.reindex(
        index=user_item_matrix.index, 
        columns=user_item_matrix.columns, 
        fill_value=0
    )
    
    # Train User-Based CF
    print("\n" + "="*50)
    user_cf = UserBasedCollaborativeFiltering(n_neighbors=30)
    user_cf.fit(train_matrix, user_means)
    
    print("Evaluating User-Based CF:")
    user_rmse, user_mae = evaluate_model(user_cf, test_data.head(1000))  # Evaluate on subset for speed
    
    # Train Item-Based CF
    print("\n" + "="*50)
    item_cf = ItemBasedCollaborativeFiltering(n_neighbors=30)
    item_cf.fit(train_matrix)
    
    print("Evaluating Item-Based CF:")
    item_rmse, item_mae = evaluate_model(item_cf, test_data.head(1000))  # Evaluate on subset for speed
    
    # Save models
    with open('data/user_cf_model.pkl', 'wb') as f:
        pickle.dump(user_cf, f)
    
    with open('data/item_cf_model.pkl', 'wb') as f:
        pickle.dump(item_cf, f)
    
    # Save evaluation results
    results = pd.DataFrame({
        'Model': ['User-Based CF', 'Item-Based CF'],
        'RMSE': [user_rmse, item_rmse],
        'MAE': [user_mae, item_mae]
    })
    results.to_csv('data/model_evaluation.csv', index=False)
    
    print("\n" + "="*50)
    print("Model Comparison:")
    print(results)
    
    # Generate sample recommendations
    print("\n" + "="*50)
    print("Sample Recommendations:")
    
    # Get a random user for demonstration
    sample_user = np.random.choice(user_item_matrix.index)
    
    print(f"\nRecommendations for User {sample_user}:")
    
    user_recs = user_cf.recommend(sample_user, 5)
    print("User-Based CF:")
    for item_id, pred_rating in user_recs:
        print(f"  Item {item_id}: {pred_rating:.2f}")
    
    item_recs = item_cf.recommend(sample_user, 5)
    print("Item-Based CF:")
    for item_id, pred_rating in item_recs:
        print(f"  Item {item_id}: {pred_rating:.2f}")
    
    print("\nModels saved successfully!")

# Run training and evaluation
train_and_evaluate_models()
