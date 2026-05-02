# NPS Intelligence Dashboard 💬 — AI-Powered Customer Loyalty Analysis

Go beyond the score. Understand *why* users are promoters or detractors, predict churn risk from NPS patterns, and get PM-ready action plans — all in one dashboard.

## 🚀 Product Overview

### The Problem
Net Promoter Score is one of the most widely tracked metrics in SaaS — and one of the most poorly used. Most teams report a single NPS number ("We're at 42!") without asking: *What are detractors saying? What makes promoters different? Which segments are at risk? What should we actually do?*

Raw NPS data without analysis is just a number. Without verbatim analysis, segment breakdown, and trend tracking, NPS is a vanity metric that leads to no action.

### The Solution
NPS Intelligence Dashboard ingests NPS survey responses (score + verbatim), applies NLP clustering to extract themes from each segment, uses ML to predict which passives are at churn risk, and generates PM-prioritized action plans — all visualized in an interactive Streamlit dashboard.

### The Impact
- 📊 **Segment breakdown** — Promoters, Passives, Detractors with trend visualization
- - 🧠 **NLP verbatim analysis** — Extract top themes from each segment automatically
  - - 🔮 **Churn risk prediction** — ML model identifies passives most likely to become detractors
    - - 🎯 **PM action plan** — Prioritized recommendations derived directly from user language
      - - 📈 **Trend tracking** — NPS movement over time with correlation to product events
       
        - ---

        ## 🎯 Why This Matters (Product Perspective)

        Every PM collects NPS. Almost none use it to its full potential. This dashboard demonstrates that NPS is not just a number — it's a rich qualitative dataset that, when properly analyzed, directly drives roadmap decisions.

        The verbatim analysis is where the real value is: when 34% of your detractors mention "slow load times" and 28% mention "missing export feature," those are P0 tickets, not nice-to-haves. This tool surfaces those signals automatically.

        **The key insight:** NPS analysis should drive product decisions, not just be reported in monthly business reviews.

        ---

        ## 🧠 AI/ML Explanation

        | Component | Technique | Why It Was Chosen |
        |---|---|---|
        | Verbatim Theme Extraction | TF-IDF + KMeans clustering | Groups similar verbatim responses into actionable themes without supervision |
        | Sentiment Scoring | TextBlob polarity analysis | Validates cluster sentiment (detractors should be negative, promoters positive) |
        | Churn Risk Prediction | Logistic Regression on Passives | Passives (score 7-8) are the highest-value segment — predicts which will churn vs. promote |
        | NPS Trend Detection | Rolling average + changepoint detection | Identifies when NPS meaningfully improved or degraded (not just noise) |
        | Key Quote Extraction | Sentence frequency scoring | Surfaces the most representative verbatim from each theme cluster |

        **Churn Risk Model for Passives:**
        Passives are scored 7 or 8. This model predicts which passives are at churn risk vs. upgrade risk using behavioral signals:
        - Number of days since last login
        - - Feature adoption depth
          - - Support ticket count
            - - Subscription tier
              - - Verbatim sentiment score
               
                - ---

                ## 🛠 Tech Stack

                | Layer | Technology |
                |---|---|
                | UI | Streamlit |
                | NLP | scikit-learn (TF-IDF, KMeans), TextBlob |
                | ML | scikit-learn (Logistic Regression) |
                | Data Processing | Pandas, NumPy |
                | Visualization | Plotly (gauges, trend charts, bar charts) |
                | Language | Python 3.8+ |

                ---

                ## 📊 Sample Output

                **Input:** 250 NPS responses from a SaaS tool (Q1 2026)

                **Score Distribution:**
                - Promoters (9-10): 38% — NPS = **+12**
                - - Passives (7-8): 32%
                  - - Detractors (0-6): 30%
                   
                    - **Detractor Theme Analysis (NLP clusters):**
                    - | Theme | % of Detractors | Avg Sentiment | Representative Quote |
                    - |---|---|---|---|
                    - | Performance & Load Times | 34% | -0.71 | "The app is painfully slow, especially on mobile" |
                    - | Missing Export Features | 28% | -0.58 | "I can't export my data to CSV — this is basic" |
                    - | Confusing Navigation | 22% | -0.44 | "I can never find what I'm looking for" |
                    - | Pricing Concerns | 16% | -0.52 | "The value doesn't justify the price increase" |
                   
                    - **Promoter Theme Analysis:**
                    - | Theme | % of Promoters | Avg Sentiment | Representative Quote |
                    - |---|---|---|---|
                    - | Customer Support Quality | 41% | +0.82 | "Support team is incredibly responsive — best I've experienced" |
                    - | Time Saved / Efficiency | 35% | +0.78 | "This tool saves my team 5 hours per week easily" |
                    - | Ease of Use | 24% | +0.69 | "So intuitive, my whole team onboarded in an afternoon" |
                   
                    - **PM Priority Action List (auto-generated):**
                    - 1. 🚨 **P0: Performance** — 34% of detractors cite load times. Engineering priority: mobile performance audit + CDN optimization.
                      2. 2. 🚨 **P0: Export feature** — 28% of detractors want CSV export. This is a 1-sprint feature with high churn-prevention value.
                         3. 3. ⚠️ **P1: Navigation redesign** — 22% of detractors confused by UX. Trigger IA audit + Hotjar session recording review.
                            4. 4. 📈 **Amplify: Support quality** — 41% of promoters cite support. Invest in support team, create case studies from this group.
                              
                               5. **Churn Risk (Passives):**
                               6. - 47 passives flagged as HIGH churn risk (score 7, negative verbatim, low recent activity)
                                  - - 33 passives flagged as UPGRADE potential (score 8, positive verbatim, high feature adoption)
                                   
                                    - ---

                                    ## 📸 Demo Instructions

                                    ```bash
                                    # 1. Clone the repo
                                    git clone https://github.com/Poojaahegde/nps-intelligence-dashboard.git
                                    cd nps-intelligence-dashboard

                                    # 2. Install dependencies
                                    pip install -r requirements.txt

                                    # 3. Launch the dashboard
                                    streamlit run app.py
                                    ```

                                    Open `http://localhost:8501` in your browser.

                                    The app auto-loads 250 synthetic NPS responses. You can also upload your own CSV with columns: `score` (0-10), `verbatim` (text comment), `user_id`, `date`, and optional: `plan_type`, `days_since_login`.

                                    ---

                                    ## 🎯 Product Thinking Layer

                                    ### 👥 Target Users
                                    - **Product Managers** who collect NPS quarterly and want to turn raw responses into roadmap input
                                    - - **Customer Success Managers** identifying which passives to proactively reach out to
                                      - - **Growth PMs** tracking NPS trend as a leading indicator of expansion/contraction revenue
                                       
                                        - ### 😣 Pain Points Solved
                                        - - **NPS is just a number** — without verbatim analysis, it's unactionable; this tool surfaces the "why"
                                          - - **Manual verbatim coding takes hours** — reading and categorizing 250 verbatims manually takes 3-4 hours; NLP does it in seconds
                                            - - **Passives are ignored** — most teams focus on detractors; passives are often the highest-leverage segment (close to promoting or churning)
                                              - - **No PM action output** — dashboards that show NPS without recommendations leave PMs to figure out "so what" themselves
                                               
                                                - ### 🧩 Key Product Decisions Made
                                               
                                                - **KMeans clustering over predefined categories:** NPS themes are product-specific and can't be predicted in advance. Unsupervised clustering lets the data define the themes rather than forcing user responses into predetermined buckets.
                                               
                                                - **Focusing churn prediction on passives (not detractors):** Detractors are largely lost. Passives are on the fence — the highest-value intervention target. A passive who churns is a lost revenue opportunity that was preventable.
                                               
                                                - **Action plan as the primary output:** Most dashboards stop at visualization. This tool translates NPS patterns into a PM-ready action list — the actual artifact that drives meetings and roadmap decisions.
                                               
                                                - **Trend tracking with changepoint detection:** A one-time NPS score is less valuable than the direction of movement. Changepoint detection surfaces when NPS materially changed and correlates it with product events.
                                               
                                                - ### 🗺 Future Roadmap
                                               
                                                - | Priority | Feature | Expected Impact |
                                                - |---|---|---|
                                                - | P0 | CSV upload for real NPS data | Transform demo into production tool |
                                                - | P0 | Typeform / SurveyMonkey API integration | Automatic NPS ingestion |
                                                - | P1 | Segment NPS by user cohort (plan, acquisition source) | Identify which segments drive NPS changes |
                                                - | P1 | Before/after NPS comparison (pre/post product release) | Measure whether product changes moved NPS |
                                                - | P2 | Proactive passive outreach list (export to CSV for CS) | Enable CS team to act on churn risk predictions |
                                                - | P2 | Competitor NPS benchmarking (Delighted API) | Contextualize your NPS vs. industry |
                                                - | P3 | Slack alert: "NPS dropped 5 points this week" | Proactive PM monitoring |
                                               
                                                - ---

                                                ## 📁 Project Structure

                                                ```
                                                nps-intelligence-dashboard/
                                                ├── app.py              # Main Streamlit dashboard
                                                ├── nps_analyzer.py     # NPS segmentation + verbatim NLP analysis
                                                ├── churn_predictor.py  # Logistic regression churn risk for passives
                                                ├── data_generator.py   # Synthetic NPS response generator
                                                ├── requirements.txt    # Python dependencies
                                                └── README.md           # This file
                                                ```

                                                ---

                                                ## 🔗 Related Projects in This Portfolio
                                                - [FeedbackSense](https://github.com/Poojaahegde/FeedbackSense-AI-Product-Feedback-Analyzer) — General user feedback clustering and sentiment
                                                - - [Churn Prediction Dashboard](https://github.com/Poojaahegde/churn-prediction-dashboard) — ML-powered churn prediction with explainable AI
                                                  - - [EmotionLoop](https://github.com/Poojaahegde/EmotionLoop) — 6-class emotion detection in user text
                                                   
                                                    - ---

                                                    *Built as part of an AI PM portfolio — demonstrating that NPS analysis requires NLP, ML, and product judgment to become actionable, not just reporting.*
