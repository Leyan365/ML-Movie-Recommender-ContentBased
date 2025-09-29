<img width="1824" height="923" alt="m2" src="https://github.com/user-attachments/assets/1b6af8a6-2b4f-45c0-9a54-3f87b592c1b3" /># 🎬 ML-Movie-Recommender-ContentBased

An End-to-End Movie Recommender System built using **Content-Based Filtering**, **TF-IDF Vectorization**, and deployed with **Streamlit**. The system recommends movies by analyzing metadata such as keywords, genres, cast, crew (director), and plot overview.

---

## 🔑 Features

- 🎯 Recommends top 5 similar movies using content-based filtering
- 🧠 Uses TF-IDF and cosine similarity for similarity scoring
- 🖼️ Fetches real-time movie posters via TMDB API
- ⚙️ Built using pandas, scikit-learn, nltk, Streamlit, and requests
- 🚀 Clean Streamlit UI with a responsive layout and loading spinner

---

## 🚀 How to Run the Project Locally

> ⚠️ This project does **not** include large datasets or `.pkl` files in the repository. You must generate them before running the app.

### 1. 📦 Setup Environment

Ensure you have **Python 3.x** and install required dependencies:

```bash
pip install pandas numpy scikit-learn streamlit requests nltk
```

---

### 2. 📁 Obtain Datasets

Download the **TMDB 5000 Movie Dataset**:

- [`tmdb_5000_movies.csv`](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- [`tmdb_5000_credits.csv`](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

📌 Place both CSV files in your project root directory.

---

### 3. ⚙️ Generate Model Artifacts

Open and run all cells in `notebook.ipynb` to:

- Clean and preprocess data
- Perform TF-IDF vectorization
- Compute cosine similarity matrix

This will generate two key files:

- `movies.pkl` – cleaned movie metadata with tags
- `similarity.pkl` – cosine similarity matrix (5000x5000)

---

### 4. 🔐 Configure TMDB API Key

The app fetches movie posters using the TMDB API.

- Create a free TMDB account → [https://www.themoviedb.org/](https://www.themoviedb.org/)
- Navigate to [API section](https://www.themoviedb.org/settings/api) and generate a **v3 API key**
- Replace the placeholder in `app.py`:

```python
url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY_HERE&language=en-US"
```

> ✅ Don’t commit your real API key to GitHub. Use a placeholder when pushing!

---

### 5. 🚀 Run the App

Launch the Streamlit web app using:

```bash
streamlit run app.py
```

---

## 🧠 Technical Deep Dive

### Machine Learning Pipeline (`notebook.ipynb`)

| Step | Description | Libraries |
|------|-------------|-----------|
| **Data Cleaning** | Merged movies and credits data, handled nulls, parsed genres/keywords/cast/crew | `pandas`, `ast` |
| **Feature Engineering** | Extracted top 3 cast, director, keywords, etc. into a `tags` field | `lambda`, `apply` |
| **Text Normalization** | Used stemming to reduce words to root form | `nltk.PorterStemmer` |
| **Vectorization** | TF-IDF vectorizer on `tags` column (max_features=5000) | `TfidfVectorizer` |
| **Similarity Calculation** | Cosine similarity on vectorized tags | `cosine_similarity` |
| **Artifact Saving** | Saved `movies.pkl` and `similarity.pkl` | `pickle` |

---

### Streamlit App (`app.py`)

- Loads the `.pkl` artifacts
- Accepts user movie input via dropdown
- Finds top 5 similar movies using cosine similarity
- Fetches posters using TMDB API
- Displays results in a horizontal layout with images and captions
- Uses a loading spinner to improve UX

---

## 📸 Application Preview

<img width="1825" height="951" alt="m1" src="https://github.com/user-attachments/assets/40ae912d-ade6-4c65-a83b-30a6ae501b05" />
<img width="1824" height="923" alt="m2" src="https://github.com/user-attachments/assets/e4d56ca2-0c1a-45b8-8e48-2172f8efe689" />


---

## ⚠️ Notes

- Exclude `.pkl`, `.csv`, and `API keys` from your GitHub repo
- Add these to your `.gitignore`:

```
*.pkl
*.csv
apikey.txt
```

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## 🙏 Acknowledgements

- [TMDB API](https://www.themoviedb.org/documentation/api)
- [Kaggle TMDB 5000 Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- [Streamlit](https://streamlit.io/)
- YouTube inspiration: *Project-Based ML Recommender*

---
