"""
NPSAnalyzer: NLP-based verbatim theme extraction and passive churn risk prediction.
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from textblob import TextBlob


class NPSAnalyzer:
      def __init__(self, n_clusters: int = 3):
                self.n_clusters = n_clusters

      def extract_themes(self, verbatims: list) -> list:
                """
                        Extract NLP themes from a list of verbatim responses.
                                Returns list of theme dicts with label, pct, avg_sentiment, key_quote, top_words.
                                        """
                if len(verbatims) < self.n_clusters:
                              return []

                n_clusters = min(self.n_clusters, len(verbatims))
                vectorizer = TfidfVectorizer(stop_words="english", max_features=100, ngram_range=(1, 2))

          try:
                        tfidf = vectorizer.fit_transform(verbatims)
except Exception:
            return []

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(tfidf)
        feature_names = vectorizer.get_feature_names_out()

        themes = []
        for cluster_id in range(n_clusters):
                      cluster_indices = [i for i, l in enumerate(labels) if l == cluster_id]
                      cluster_verbatims = [verbatims[i] for i in cluster_indices]

            if not cluster_verbatims:
                              continue

            # Get top words for this cluster
            center = kmeans.cluster_centers_[cluster_id]
            top_word_indices = center.argsort()[-5:][::-1]
            top_words = [feature_names[i] for i in top_word_indices]

            # Avg sentiment
            sentiments = [TextBlob(v).sentiment.polarity for v in cluster_verbatims]
            avg_sentiment = np.mean(sentiments)

            # Key quote: most representative verbatim (closest to cluster center)
            cluster_vecs = tfidf[cluster_indices]
            center_vec = kmeans.cluster_centers_[cluster_id].reshape(1, -1)
            from sklearn.metrics.pairwise import cosine_similarity
            sims = cosine_similarity(cluster_vecs, center_vec).flatten()
            best_idx = cluster_indices[sims.argmax()]
            key_quote = verbatims[best_idx][:120]

            # Label from top words
            label = " / ".join(top_words[:2]).title()

            themes.append({
                              "cluster_id": cluster_id,
                              "label": label,
                              "pct": len(cluster_indices) / len(verbatims) * 100,
                              "count": len(cluster_indices),
                              "avg_sentiment": round(avg_sentiment, 3),
                              "key_quote": key_quote,
                              "top_words": top_words,
            })

        themes.sort(key=lambda x: x["count"], reverse=True)
        return themes

    def predict_passive_churn_risk(self, passives_df: pd.DataFrame) -> np.ndarray:
              """
                      Predict churn risk score (0-1) for passive NPS respondents.
                              Uses heuristic scoring based on available behavioral signals.
                                      """
              scores = []
              for _, row in passives_df.iterrows():
                            risk = 0.5  # Base risk for passives

            # NPS score: 7 = higher churn risk, 8 = lower
                  if row.get("score", 7) == 7:
                                    risk += 0.15
else:
                risk -= 0.1

            # Verbatim sentiment
              sentiment = TextBlob(str(row.get("verbatim", ""))).sentiment.polarity
            risk -= sentiment * 0.2  # Negative sentiment increases risk

            # Days since login
            days_since_login = row.get("days_since_login", 10)
            if days_since_login > 14:
                              risk += 0.2
elif days_since_login > 7:
                risk += 0.1
elif days_since_login < 2:
                risk -= 0.15

            # Feature adoption
            features_used = row.get("features_used", 3)
            if features_used < 2:
                              risk += 0.15
elif features_used > 5:
                risk -= 0.15

            scores.append(min(1.0, max(0.0, risk + np.random.normal(0, 0.05))))

        return np.array(scores)
