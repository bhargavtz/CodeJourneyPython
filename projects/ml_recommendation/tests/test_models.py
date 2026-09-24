"""
Tests for ML recommendation models.

Author: CodeJourney ML Project
License: MIT
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch
from models.train import CollaborativeFiltering, ContentBasedFiltering, HybridRecommender


class TestCollaborativeFiltering:
    """Test collaborative filtering model."""

    @pytest.fixture
    def sample_data(self):
        """Create sample user-item matrix."""
        np.random.seed(42)
        user_item_matrix = np.random.randint(0, 6, (10, 20)).astype(float)
        user_ids = np.arange(10)
        item_ids = np.arange(20)
        return user_item_matrix, user_ids, item_ids

    def test_model_initialization(self):
        """Test model initialization."""
        model = CollaborativeFiltering(n_factors=50)
        assert model.n_factors == 50
        assert model.user_factors is None

    def test_model_fit(self, sample_data):
        """Test model fitting."""
        matrix, user_ids, item_ids = sample_data
        model = CollaborativeFiltering(n_factors=10, max_iter=50)
        model.fit(matrix, user_ids, item_ids)

        assert model.user_factors is not None
        assert model.item_factors is not None
        assert model.user_factors.shape[0] == len(user_ids)

    def test_model_predict(self, sample_data):
        """Test prediction."""
        matrix, user_ids, item_ids = sample_data
        model = CollaborativeFiltering(n_factors=5, max_iter=50)
        model.fit(matrix, user_ids, item_ids)

        recommendations = model.predict(user_id=0, n_recommendations=5)
        assert len(recommendations) <= 5
        assert all(0 <= item < len(item_ids) for item in recommendations)

    def test_model_unknown_user(self, sample_data):
        """Test prediction for unknown user."""
        matrix, user_ids, item_ids = sample_data
        model = CollaborativeFiltering(n_factors=5, max_iter=50)
        model.fit(matrix, user_ids, item_ids)

        recommendations = model.predict(user_id=999, n_recommendations=5)
        assert len(recommendations) == 0


class TestContentBasedFiltering:
    """Test content-based filtering model."""

    @pytest.fixture
    def sample_data(self):
        """Create sample item features."""
        np.random.seed(42)
        item_features = np.random.randn(20, 15)
        item_ids = np.arange(20)
        return item_features, item_ids

    def test_model_fit(self, sample_data):
        """Test model fitting."""
        features, item_ids = sample_data
        model = ContentBasedFiltering()
        model.fit(features, item_ids)

        assert model.item_similarity is not None
        assert model.item_similarity.shape == (len(item_ids), len(item_ids))

    def test_model_predict(self, sample_data):
        """Test content-based prediction."""
        features, item_ids = sample_data
        model = ContentBasedFiltering()
        model.fit(features, item_ids)

        recommendations = model.predict(liked_item_id=0, n_recommendations=5)
        assert len(recommendations) <= 5


class TestHybridRecommender:
    """Test hybrid recommendation model."""

    @pytest.fixture
    def sample_data(self):
        """Create sample data."""
        np.random.seed(42)
        matrix = np.random.randint(0, 6, (10, 20)).astype(float)
        features = np.random.randn(20, 15)
        user_ids = np.arange(10)
        item_ids = np.arange(20)
        return matrix, features, user_ids, item_ids

    def test_hybrid_model_creation(self):
        """Test hybrid model initialization."""
        model = HybridRecommender(cf_weight=0.6, cb_weight=0.4)
        assert model.cf_weight == 0.6
        assert model.cb_weight == 0.4

    def test_hybrid_model_fit(self, sample_data):
        """Test hybrid model fitting."""
        matrix, features, user_ids, item_ids = sample_data
        model = HybridRecommender()
        model.fit(matrix, features, user_ids, item_ids)

        assert model.cf_model.user_factors is not None
        assert model.cb_model.item_similarity is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
