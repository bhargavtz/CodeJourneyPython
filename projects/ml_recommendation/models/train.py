#!/usr/bin/env python3
"""
Model training pipeline for recommendation systems.

Trains and evaluates multiple recommendation models:
- Collaborative filtering (matrix factorization)
- Content-based filtering
- Hybrid approaches

Author: CodeJourney ML Project
License: MIT
"""

import logging
import joblib
from pathlib import Path
from typing import Dict, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestRegressor

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


class CollaborativeFiltering:
    """Collaborative filtering recommendation model."""

    def __init__(self, n_factors: int = 50, max_iter: int = 200):
        """
        Initialize collaborative filtering model.

        Args:
            n_factors: Number of latent factors
            max_iter: Maximum iterations for NMF
        """
        self.n_factors = n_factors
        self.model = NMF(n_components=n_factors, max_iter=max_iter, random_state=42)
        self.user_factors = None
        self.item_factors = None
        self.user_to_idx = {}
        self.item_to_idx = {}

    def fit(self, user_item_matrix: np.ndarray,
            user_ids: np.ndarray, item_ids: np.ndarray) -> None:
        """
        Fit collaborative filtering model.

        Args:
            user_item_matrix: User-item rating matrix
            user_ids: Unique user IDs
            item_ids: Unique item IDs
        """
        logger.info(f"Training collaborative filtering with {self.n_factors} factors")

        # Create index mappings
        self.user_to_idx = {uid: idx for idx, uid in enumerate(user_ids)}
        self.item_to_idx = {iid: idx for idx, iid in enumerate(item_ids)}

        # Fit NMF model
        self.user_factors = self.model.fit_transform(user_item_matrix)
        self.item_factors = self.model.components_.T

        logger.info(f"Trained on {len(user_ids)} users and {len(item_ids)} items")

    def predict(self, user_id: int, n_recommendations: int = 10) -> np.ndarray:
        """
        Get recommendations for user.

        Args:
            user_id: User ID
            n_recommendations: Number of recommendations

        Returns:
            Array of recommended item indices
        """
        if user_id not in self.user_to_idx:
            logger.warning(f"User {user_id} not in training data")
            return np.array([])

        user_idx = self.user_to_idx[user_id]
        user_factor = self.user_factors[user_idx:user_idx+1]

        # Compute scores for all items
        scores = user_factor @ self.item_factors.T
        scores = scores.ravel()

        # Get top-k items
        top_items = np.argsort(scores)[-n_recommendations:][::-1]
        return top_items

    def save(self, filepath: str) -> None:
        """Save model to file."""
        joblib.dump({
            'model': self.model,
            'user_factors': self.user_factors,
            'item_factors': self.item_factors,
            'user_to_idx': self.user_to_idx,
            'item_to_idx': self.item_to_idx,
        }, filepath)
        logger.info(f"Saved model to {filepath}")

    def load(self, filepath: str) -> None:
        """Load model from file."""
        data = joblib.load(filepath)
        self.model = data['model']
        self.user_factors = data['user_factors']
        self.item_factors = data['item_factors']
        self.user_to_idx = data['user_to_idx']
        self.item_to_idx = data['item_to_idx']
        logger.info(f"Loaded model from {filepath}")


class ContentBasedFiltering:
    """Content-based recommendation model using item features."""

    def __init__(self):
        """Initialize content-based model."""
        self.item_features = None
        self.item_similarity = None
        self.item_to_idx = {}

    def fit(self, item_features: np.ndarray, item_ids: np.ndarray) -> None:
        """
        Fit content-based model.

        Args:
            item_features: Item feature matrix
            item_ids: Unique item IDs
        """
        logger.info("Training content-based model")

        self.item_features = item_features
        self.item_to_idx = {iid: idx for idx, iid in enumerate(item_ids)}

        # Compute item similarity matrix
        self.item_similarity = cosine_similarity(item_features)

        logger.info(f"Computed similarity for {len(item_ids)} items")

    def predict(self, liked_item_id: int, n_recommendations: int = 10) -> np.ndarray:
        """
        Get recommendations based on liked item.

        Args:
            liked_item_id: Item ID that user liked
            n_recommendations: Number of recommendations

        Returns:
            Array of similar item indices
        """
        if liked_item_id not in self.item_to_idx:
            logger.warning(f"Item {liked_item_id} not in model")
            return np.array([])

        item_idx = self.item_to_idx[liked_item_id]
        similarities = self.item_similarity[item_idx]

        # Get top similar items (excluding the item itself)
        similar_items = np.argsort(similarities)[-n_recommendations-1:-1][::-1]
        return similar_items

    def save(self, filepath: str) -> None:
        """Save model to file."""
        joblib.dump({
            'item_features': self.item_features,
            'item_similarity': self.item_similarity,
            'item_to_idx': self.item_to_idx,
        }, filepath)
        logger.info(f"Saved model to {filepath}")


class HybridRecommender:
    """Hybrid recommendation model combining multiple approaches."""

    def __init__(self, cf_weight: float = 0.5, cb_weight: float = 0.5):
        """
        Initialize hybrid recommender.

        Args:
            cf_weight: Weight for collaborative filtering
            cb_weight: Weight for content-based
        """
        self.cf_weight = cf_weight
        self.cb_weight = cb_weight
        self.cf_model = CollaborativeFiltering()
        self.cb_model = ContentBasedFiltering()

    def fit(self, user_item_matrix: np.ndarray,
            item_features: np.ndarray,
            user_ids: np.ndarray,
            item_ids: np.ndarray) -> None:
        """
        Fit hybrid model.

        Args:
            user_item_matrix: User-item rating matrix
            item_features: Item feature matrix
            user_ids: Unique user IDs
            item_ids: Unique item IDs
        """
        logger.info("Training hybrid recommender")

        self.cf_model.fit(user_item_matrix, user_ids, item_ids)
        self.cb_model.fit(item_features, item_ids)

        logger.info(f"Hybrid model ready (CF:{self.cf_weight}, CB:{self.cb_weight})")

    def predict(self, user_id: int, liked_item_id: int,
                n_recommendations: int = 10) -> np.ndarray:
        """
        Get hybrid recommendations.

        Args:
            user_id: User ID
            liked_item_id: Item user liked
            n_recommendations: Number of recommendations

        Returns:
            Array of recommended item indices
        """
        # Get CF predictions
        cf_items = self.cf_model.predict(user_id, n_recommendations)

        # Get CB predictions
        cb_items = self.cb_model.predict(liked_item_id, n_recommendations)

        # Combine using weights
        combined_items = list(set(cf_items) | set(cb_items))
        combined_items = combined_items[:n_recommendations]

        return np.array(combined_items)

    def save(self, filepath: str) -> None:
        """Save model to file."""
        joblib.dump({
            'cf_model': self.cf_model,
            'cb_model': self.cb_model,
            'cf_weight': self.cf_weight,
            'cb_weight': self.cb_weight,
        }, filepath)
        logger.info(f"Saved hybrid model to {filepath}")


class ModelTrainer:
    """Orchestrates model training workflow."""

    def __init__(self, data_dir: str = "data"):
        """
        Initialize trainer.

        Args:
            data_dir: Directory for data files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def train_all_models(self) -> Dict:
        """
        Train all recommendation models.

        Returns:
            Dictionary with trained models and metrics
        """
        # Load or generate data
        df = self._load_or_generate_data()

        # Prepare data
        train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

        # Extract unique IDs and create matrices
        user_ids = df['user_id'].unique()
        item_ids = df['item_id'].unique()

        user_item_matrix = self._create_user_item_matrix(train_df, user_ids, item_ids)

        logger.info("=" * 60)
        logger.info("TRAINING MODELS")
        logger.info("=" * 60)

        # Train CF model
        cf_model = CollaborativeFiltering(n_factors=50)
        cf_model.fit(user_item_matrix, user_ids, item_ids)
        cf_model.save("models/collaborative_filtering.pkl")

        # Train CB model (using dummy features for demo)
        item_features = np.random.randn(len(item_ids), 20)
        cb_model = ContentBasedFiltering()
        cb_model.fit(item_features, item_ids)
        cb_model.save("models/content_based.pkl")

        # Train hybrid model
        hybrid_model = HybridRecommender()
        hybrid_model.fit(user_item_matrix, item_features, user_ids, item_ids)
        hybrid_model.save("models/hybrid_recommender.pkl")

        logger.info("All models trained and saved")

        return {
            'cf_model': cf_model,
            'cb_model': cb_model,
            'hybrid_model': hybrid_model,
            'user_ids': user_ids,
            'item_ids': item_ids,
        }

    def _load_or_generate_data(self) -> pd.DataFrame:
        """Load or generate sample data."""
        data_file = self.data_dir / "processed" / "ratings.csv"

        if data_file.exists():
            logger.info(f"Loading data from {data_file}")
            return pd.read_csv(data_file)

        logger.info("Generating sample data")
        np.random.seed(42)

        n_users = 100
        n_items = 50
        n_ratings = 1000

        data = {
            'user_id': np.random.randint(0, n_users, n_ratings),
            'item_id': np.random.randint(0, n_items, n_ratings),
            'rating': np.random.randint(1, 6, n_ratings),
        }

        df = pd.DataFrame(data).drop_duplicates(['user_id', 'item_id'])
        data_file.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(data_file, index=False)

        logger.info(f"Generated {len(df)} ratings from {n_users} users and {n_items} items")
        return df

    def _create_user_item_matrix(self, df: pd.DataFrame,
                                user_ids: np.ndarray,
                                item_ids: np.ndarray) -> np.ndarray:
        """Create user-item rating matrix."""
        user_to_idx = {uid: idx for idx, uid in enumerate(user_ids)}
        item_to_idx = {iid: idx for idx, iid in enumerate(item_ids)}

        matrix = np.zeros((len(user_ids), len(item_ids)))

        for _, row in df.iterrows():
            user_idx = user_to_idx.get(row['user_id'])
            item_idx = item_to_idx.get(row['item_id'])

            if user_idx is not None and item_idx is not None:
                matrix[user_idx, item_idx] = row['rating']

        logger.info(f"Created user-item matrix: {matrix.shape}")
        return matrix


def main():
    """Main training entry point."""
    trainer = ModelTrainer(data_dir="data")

    models = trainer.train_all_models()

    logger.info("=" * 60)
    logger.info("TRAINING COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Trained 3 models for {len(models['user_ids'])} users and {len(models['item_ids'])} items")

    # Example prediction
    user_id = 0
    recommendations = models['cf_model'].predict(user_id, n_recommendations=5)
    logger.info(f"Recommendations for user {user_id}: {recommendations}")


if __name__ == "__main__":
    main()
