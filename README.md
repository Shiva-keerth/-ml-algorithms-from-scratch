# 🧠 Machine Learning & AI Algorithms from Scratch

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Vectorization-013243?style=for-the-badge&logo=numpy&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Deep_Learning-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Interactive_UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A comprehensive, first-principles implementation of core **Machine Learning, Deep Learning, Natural Language Processing (NLP), and Computer Vision** algorithms built entirely from scratch in Python.

Instead of relying solely on black-box abstractions like `scikit-learn`, this repository reconstructs the underlying mathematical foundations—vectorized linear algebra, differential calculus, gradient optimization, loss functions, and probabilistic metrics—from the ground up.

---

## ⚡ Mathematical & Algorithmic Matrix

| Category | Algorithm / Model | Core Mathematics & Mechanics | Complexity (Time / Space) | Implementation |
| :--- | :--- | :--- | :--- | :--- |
| **Supervised** | **Linear & Multiple Regression** | Gradient Descent, Ordinary Least Squares (OLS), MSE Loss | $O(N \cdot P)$ / $O(P)$ | `Linear Regression/` |
| **Supervised** | **Decision Trees** | Gini Impurity, Information Gain, Recursive Node Splitting | $O(N \cdot P \log N)$ / $O(D)$ | `Desicion Tree/` |
| **Supervised** | **Random Forests** | Bootstrap Aggregating (Bagging), Feature Subsampling | $O(T \cdot N \cdot P \log N)$ / $O(T \cdot D)$ | `Random forest/` |
| **Supervised** | **K-Nearest Neighbors (KNN)** | Euclidean / Manhattan Distance Vectorization | $O(N \cdot P)$ / $O(N \cdot P)$ | `knn/` |
| **Unsupervised** | **K-Means Clustering** | WCSS Minimization, Lloyd's Centroid Iteration | $O(K \cdot N \cdot P \cdot I)$ / $O(K \cdot P)$ | `k-means/` |
| **NLP** | **TF-IDF & Cosine Similarity** | Vector Space Model, Angle Dot Product Normalization | $O(V \cdot D)$ / $O(V)$ | `cosine_similarity/` |
| **NLP** | **Sentiment Analysis Engine** | Bag-of-Words (BoW), N-Gram Frequency, VADER Lexicons | $O(N)$ / $O(V)$ | `sentiment_analysis/` |
| **Deep Learning**| **Multi-Layer Perceptron (MLP)**| Forward/Backpropagation, Cross-Entropy Loss, ReLU | $O(L \cdot N \cdot W)$ / $O(W)$ | `deep_learning/` |
| **Vision** | **AI Gesture Tracking** | MediaPipe Hand Landmark Topology, Real-time Pipeline | Real-time ($30+$ FPS) | `AI_doddle.py` |
| **Suite** | **Unified ML Suite Engine** | Dynamic algorithm switching, interactive Streamlit UI | Interactive | `improved_MI_algorithms_suite.py` |

---

## 🚀 Key Feature Highlights

### 1️⃣ Unified ML Algorithms Suite (`improved_MI_algorithms_suite.py`)
An interactive, full-stack Streamlit dashboard that lets users upload custom datasets (or use built-in benchmarks like `mall_customers.csv` or `improved_moviedataset.csv`), select algorithms dynamically, adjust hyperparameters (learning rates, tree depth, $K$ clusters), and inspect real-time performance curves and decision boundaries.

### 2️⃣ NLP & Recommender Engine (`cosine_similarity/` & `sentiment_analysis/`)
*   **Vector Recommendation System:** Implements cosine similarity on text embeddings to compute pairwise semantic matching without external vector databases.
*   **Custom Sentiment Pipeline:** Demonstrates textual preprocessing (stemming, lemmatization, stop-word removal) coupled with Bag-of-Words and TF-IDF representations.

### 3️⃣ Interactive Computer Vision (`AI_doddle.py`)
Combines OpenCV with MediaPipe landmark tracking to build an AI-powered digital canvas, enabling real-time gesture-based drawing and hand tracking in Python.

### 4️⃣ Deep Learning & LLM Integrations (`deep_learning/` & `LLM/`)
Includes custom neural network components alongside modern API wrappers (Groq & Gemini) to bridge fundamental ML theory with modern Large Language Model workflows.

---

## 📂 Repository Architecture

```
├── Linear Regression/           # OLS & Gradient Descent implementations
├── Desicion Tree/               # Custom tree node splitting & Gini entropy logic
├── Random forest/               # Ensemble forest bagging logic
├── knn/                         # K-Nearest Neighbors classifier
├── k-means/                     # Unsupervised centroid clustering
├── cosine_similarity/           # Vector space matching & recommendations
├── sentiment_analysis/          # BoW, N-Gram, and VADER sentiment models
├── deep_learning/               # Neural network backprop & activation experiments
├── NLP/                         # Natural language parsing & text vectorization
├── LLM/                         # Groq / Gemini API endpoints & prompt chains
├── AI_doddle.py                 # MediaPipe real-time interactive canvas
├── MI_algorithms_suite.py       # Core ML algorithms engine
├── improved_MI_algorithms_suite.py # Advanced Streamlit interactive ML Suite
├── mall_customers.csv           # Benchmark dataset for clustering
└── improved_moviedataset.csv    # Benchmark dataset for NLP & recommendations
```

---

## 🛠️ Tech Stack & Dependencies

*   **Core Logic:** Python 3.12, NumPy, Pandas, SciPy
*   **Machine Learning & Neural Nets:** TensorFlow, Keras, Scikit-Learn (comparison baseline)
*   **Computer Vision & Media:** OpenCV, MediaPipe
*   **NLP Tools:** NLTK, VADER Sentiment
*   **Interactive UI:** Streamlit

---

## 💻 Quick Start & Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Shiva-keerth/-ml-algorithms-from-scratch.git
   cd -ml-algorithms-from-scratch
   ```

2. **Install dependencies:**
   ```bash
   pip install numpy pandas tensorflow opencv-python mediapipe streamlit nltk
   ```

3. **Run the Interactive ML Suite:**
   ```bash
   streamlit run improved_MI_algorithms_suite.py
   ```

---

## 🤝 Connect With Me
*   **GitHub:** [Shiva-keerth](https://github.com/Shiva-keerth)
*   **Focus:** Generative AI, RAG Systems, Agentic AI, and Machine Learning.
