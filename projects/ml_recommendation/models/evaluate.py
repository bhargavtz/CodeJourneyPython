"""
Model evaluation for recommendation systems.

Calculates various metrics for evaluating recommendation quality.

Author: CodeJourney ML Project
License: MIT
"""

import logging
import numpy as np
from typing import Tuple

logger = logging.getLogger(__name__)


class RecommendationMetrics:
    """Calculate recommendation system metrics."""

    @staticmethod
    def precision_at_k(true_items: set, recommended_items: np.ndarray,
                       k: int = 10) -> float:
        """
        Calculate precision@k metric.

        Args:
            true_items: Set of relevant items
            recommended_items: Array of recommended item indices
            k: Number of recommendations to consider

        Returns:
            Precision@k score (0-1)
        """
        recommended_k = set(recommended_items[:k])
        if len(recommended_k) == 0:
            return 0.0

        correct = len(true_items & recommended_k)
        return correct / k

    @staticmethod
    def recall_at_k(true_items: set, recommended_items: np.ndarray,
                    k: int = 10) -> float:
        """
        Calculate recall@k metric.

        Args:
            true_items: Set of relevant items
            recommended_items: Array of recommended item indices
            k: Number of recommendations to consider

        Returns:
            Recall@k score (0-1)
        """
        if len(true_items) == 0:
            return 0.0

        recommended_k = set(recommended_items[:k])
        correct = len(true_items & recommended_k)
        return correct / len(true_items)

    @staticmethod
    def ndcg_at_k(true_items: set, recommended_items: np.ndarray,
                  k: int = 10) -> float:
        """
        Calculate NDCG@k (Normalized Discounted Cumulative Gain).

        Args:
            true_items: Set of relevant items
            recommended_items: Array of recommended item indices
            k: Number of recommendations to consider

        Returns:
            NDCG@k score (0-1)
        """
        # DCG
        dcg = 0.0
        for i, item in enumerate(recommended_items[:k]):
            if item in true_items:
                dcg += 1.0 / np.log2(i + 2)  # i+2 because positions are 1-indexed

        # IDCG (ideal DCG)
        idcg = 0.0
        for i in range(min(k, len(true_items))):
            idcg += 1.0 / np.log2(i + 2)

        if idcg == 0:
            return 0.0

        return dcg / idcg

    @staticmethod
    def mrr(true_items: set, recommended_items: np.ndarray) -> float:
        """
        Calculate Mean Reciprocal Rank.

        Args:
            true_items: Set of relevant items
            recommended_items: Array of recommended item indices

        Returns:
            MRR score (0-1)
        """
        for i, item in enumerate(recommended_items):
            if item in true_items:
                return 1.0 / (i + 1)
        return 0.0

    @staticmethod
    def map_score(true_items: set, recommended_items: np.ndarray,
                  k: int = 10) -> float:
        """
        Calculate Mean Average Precision.

        Args:
            true_items: Set of relevant items
            recommended_items: Array of recommended item indices
            k: Number of recommendations to consider

        Returns:
            MAP score (0-1)
        """
        precisions = []
        found_items = 0

        for i, item in enumerate(recommended_items[:k]):
            if item in true_items:
                found_items += 1
                precisions.append(found_items / (i + 1))

        if len(precisions) == 0:
            return 0.0

        return sum(precisions) / len(true_items)

    @staticmethod
    def coverage(recommended_items: np.ndarray, total_items: int) -> float:
        """
        Calculate catalog coverage.

        Args:
            recommended_items: Recommended item indices
            total_items: Total number of items in catalog

        Returns:
            Coverage score (0-1)
        """
        unique_items = len(set(recommended_items))
        return unique_items / total_items if total_items > 0 else 0.0

    @staticmethod
    def diversity(item_similarities: np.ndarray,
                  recommended_items: np.ndarray) -> float:
        """
        Calculate recommendation diversity.

        Args:
            item_similarities: Item similarity matrix
            recommended_items: Recommended item indices

        Returns:
            Diversity score (0-1, where 0=identical, 1=completely different)
        """
        if len(recommended_items) < 2:
            return 1.0

        recommended_items = recommended_items[:10]  # Limit to top 10
        similarities = []

        for i, item1 in enumerate(recommended_items):
            for j, item2 in enumerate(recommended_items):
                if i < j:
                    sim = item_similarities[item1, item2]
                    similarities.append(sim)

        if len(similarities) == 0:
            return 1.0

        mean_similarity = np.mean(similarities)
        return 1.0 - mean_similarity  # Higher similarity = lower diversity


class ModelEvaluator:
    """Evaluate recommendation models on test set."""

    @staticmethod
    def evaluate(model, test_df, user_ids, item_ids,
                 k: int = 10) -> dict:
        """
        Evaluate model on test set.

        Args:
            model: Trained recommendation model
            test_df: Test dataframe with user-item-rating tuples
            user_ids: Array of user IDs
            item_ids: Array of item IDs
            k: Number of recommendations for ranking metrics

        Returns:
            Dictionary with evaluation metrics
        """
        metrics = {
            'precision_at_10': [],
            'recall_at_10': [],
            'ndcg_at_10': [],
            'mrr': [],
            'map': [],
        }

        # Group test ratings by user
        user_test_items = test_df.groupby('user_id')['item_id'].apply(set).to_dict()

        # Evaluate for each user
        evaluated_users = 0
        for user_id, true_items in user_test_items.items():
            if user_id not in user_ids:
                continue

            recommendations = model.predict(user_id, n_recommendations=k)

            if len(recommendations) == 0:
                continue

            metrics['precision_at_10'].append(
                RecommendationMetrics.precision_at_k(true_items, recommendations, k)
            )
            metrics['recall_at_10'].append(
                RecommendationMetrics.recall_at_k(true_items, recommendations, k)
            )
            metrics['ndcg_at_10'].append(
                RecommendationMetrics.ndcg_at_k(true_items, recommendations, k)
            )
            metrics['mrr'].append(
                RecommendationMetrics.mrr(true_items, recommendations)
            )
            metrics['map'].append(
                RecommendationMetrics.map_score(true_items, recommendations, k)
            )

            evaluated_users += 1

        # Calculate averages
        results = {}
        for metric, scores in metrics.items():
            if len(scores) > 0:
                results[metric] = np.mean(scores)
            else:
                results[metric] = 0.0

        results['evaluated_users'] = evaluated_users

        return results

    @staticmethod
    def print_results(results: dict) -> None:
        """Print evaluation results."""
        logger.info("=" * 60)
        logger.info("EVALUATION RESULTS")
        logger.info("=" * 60)

        for metric, score in results.items():
            if metric != 'evaluated_users':
                logger.info(f"{metric:20} : {score:.4f}")

        logger.info(f"Evaluated on {results['evaluated_users']} users")
        logger.info("=" * 60)
