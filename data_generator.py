"""
Synthetic NPS data generator with realistic verbatim responses per segment.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Realistic verbatim templates for each NPS segment
PROMOTER_VERBATIMS = [
      "Absolutely love this product — it's transformed how our team collaborates. Would recommend to anyone.",
      "The customer support team is outstanding. Any time I have an issue, it's resolved within hours.",
      "This tool saves me at least 5 hours per week. The ROI is undeniable.",
      "So intuitive and easy to use. My entire team was onboarded in a single afternoon.",
      "The reporting features are best in class. My manager loves the dashboards I can generate.",
      "Best investment we've made this year. The platform keeps improving with every update.",
      "Incredible product. The integrations with Slack and GitHub work flawlessly.",
      "The mobile app is great — I can manage everything on the go without any friction.",
      "Customer success team proactively reached out when they saw we weren't using a key feature. Loved that.",
      "We switched from a competitor 6 months ago and haven't looked back. Night and day difference.",
      "The speed of the app is impressive — everything loads instantly even with large datasets.",
      "Love the new AI features. The summarization tool alone is worth the subscription.",
      "Excellent value for money. We've tried 4 other tools and this one wins on every dimension.",
      "The team collaboration features are exactly what we needed. Reduced our meetings by 30%.",
      "Product keeps getting better. The team clearly listens to user feedback.",
]

PASSIVE_VERBATIMS = [
      "Good product overall but the mobile experience could be improved — sometimes crashes on iOS.",
      "Works well for basic use cases. Wish there were more advanced filtering options.",
      "Solid tool, though the onboarding could be smoother. Took us a few days to get fully set up.",
      "Generally happy but the search functionality doesn't always find what I'm looking for.",
      "The core features are great. The reporting is a bit limited compared to what I need.",
      "Pretty good product. Would love better Jira integration — the current sync has some gaps.",
      "Decent experience. The UI is a little dated but functionality is solid.",
      "Works for our needs. Response time from support could be faster.",
      "Good but not great. Missing a few features that would make it perfect for our workflow.",
      "Useful tool. The pricing tiers could be more flexible for smaller teams.",
      "Mostly positive experience. Occasional performance issues during peak hours.",
      "Good product with room to grow. Would love to see more automation options.",
      "Works well day-to-day. Wish the data export options were more flexible.",
      "The tool does what it promises. Would rate higher if the API documentation were clearer.",
      "Reasonable experience. Could use better notification controls — I get too many emails.",
]

DETRACTOR_VERBATIMS = [
      "The app is painfully slow, especially when working with large projects. Unacceptable performance.",
      "I've been trying to export my data for weeks. There's no CSV export option — this is a basic feature.",
      "Support takes 3-4 days to respond and the answers are copy-pasted from documentation. Not helpful.",
      "The interface is confusing and unintuitive. I can never find what I'm looking for.",
      "The price increased 40% at renewal with barely any notice. Lost trust in the company.",
      "Critical bugs that have been reported for months are still not fixed. Priorities seem wrong.",
      "The mobile app is essentially unusable. Crashes constantly and loses my work.",
      "We've had 3 outages in the past month. Reliability is unacceptable for a paid service.",
      "The search is broken. It returns irrelevant results and misses exact matches.",
      "Data migration from our old system was a nightmare. No support during the process.",
      "Way too complicated for what it does. Competitors offer the same functionality with a much better UX.",
      "Billing support is non-existent. Have been trying to resolve a billing error for 6 weeks.",
      "The product roadmap is unclear and features promised months ago still haven't shipped.",
      "Terrible onboarding. I was left completely on my own with no guided setup.",
      "Not worth the price. We're actively looking for alternatives.",
]


def generate_nps_data(n: int = 250, seed: int = 42) -> pd.DataFrame:
      """Generate synthetic NPS survey responses with verbatims and behavioral signals."""
      np.random.seed(seed)
      responses = []
      base_date = datetime(2026, 1, 1)

    for i in range(n):
              # Score distribution: realistic SaaS NPS (promoters ~35%, passives ~35%, detractors ~30%)
              rand = np.random.random()
              if rand < 0.35:
                            score = np.random.choice([9, 10], p=[0.4, 0.6])
                            segment = "promoter"
                            verbatim = np.random.choice(PROMOTER_VERBATIMS)
                            days_since_login = np.random.randint(0, 5)
                            features_used = np.random.randint(4, 10)
elif rand < 0.70:
            score = np.random.choice([7, 8], p=[0.45, 0.55])
            segment = "passive"
            verbatim = np.random.choice(PASSIVE_VERBATIMS)
            days_since_login = np.random.randint(2, 20)
            features_used = np.random.randint(2, 7)
else:
            score = np.random.choice([0, 1, 2, 3, 4, 5, 6], p=[0.05, 0.05, 0.05, 0.10, 0.15, 0.25, 0.35])
              segment = "detractor"
            verbatim = np.random.choice(DETRACTOR_VERBATIMS)
            days_since_login = np.random.randint(5, 45)
            features_used = np.random.randint(1, 4)

        # Random date within last 90 days
        date = base_date + timedelta(days=np.random.randint(0, 90))

        responses.append({
                      "user_id": f"user_{i:04d}",
                      "score": score,
                      "segment": segment,
                      "verbatim": verbatim,
                      "date": date.date(),
                      "days_since_login": days_since_login,
                      "features_used": features_used,
                      "plan_type": np.random.choice(["free", "starter", "pro", "enterprise"], p=[0.30, 0.35, 0.25, 0.10]),
        })

    return pd.DataFrame(responses)
