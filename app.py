import streamlit as st
from content_based_filtering import content_recommendation
from scipy.sparse import load_npz
import pandas as pd
from numpy import load
from hybrid_recommendations import HybridRecommenderSystem

# Load files
songs_data = pd.read_csv("data/cleaned_data.csv")
transformed_data = load_npz("data/transformed_data.npz")
track_ids = load("data/track_ids.npy", allow_pickle=True)
filtered_data = pd.read_csv("data/collab_filtered_data.csv")
interaction_matrix = load_npz("data/interaction_matrix.npz")
transformed_hybrid_data = load_npz("data/transformed_hybrid_data.npz")

# Title
st.title('🎵 Spotify Song Recommender')

# Input
st.write('### Enter a song and artist to get personalized music recommendations.')
song_name = st.text_input('Enter a song name:').lower()
artist_name = st.text_input('Enter the artist name:').lower()
k = st.selectbox('How many recommendations do you want?', [5, 10, 15, 20], index=1)

# Check for hybrid vs content-based
if ((filtered_data["name"] == song_name) & (filtered_data["artist"] == artist_name)).any():
    filtering_type = "Hybrid Recommender System"
    diversity = st.slider("Diversity in Recommendations", 1, 9, value=5)
    content_based_weight = 1 - (diversity / 10)

    chart_data = pd.DataFrame({
        "type": ["Personalized", "Diverse"],
        "ratio": [10 - diversity, diversity]
    })
    st.bar_chart(chart_data, x="type", y="ratio")
else:
    filtering_type = "Content-Based Filtering"

# Recommendation Logic
if st.button("Get Recommendations"):
    if filtering_type == "Content-Based Filtering":
        if ((songs_data["name"] == song_name) & (songs_data['artist'] == artist_name)).any():
            st.write(f"Recommendations for **{song_name}** by **{artist_name}**")
            recommendations = content_recommendation(song_name, artist_name, songs_data, transformed_data, k)
        else:
            st.error(f"Sorry, we couldn't find **{song_name}** by **{artist_name}**.")
            recommendations = pd.DataFrame()
    else:
        st.write(f"Recommendations for **{song_name}** by **{artist_name}**")
        recommender = HybridRecommenderSystem(k, content_based_weight)
        recommendations = recommender.give_recommendations(
            song_name, artist_name, filtered_data,
            transformed_hybrid_data, track_ids, interaction_matrix
        )

    # Display recommendations
    if not recommendations.empty:
        for ind, recommendation in recommendations.iterrows():
            rec_song = recommendation['name'].title()
            rec_artist = recommendation['artist'].title()
            preview = recommendation['spotify_preview_url']

            if ind == 0:
                st.markdown("## 🎶 Currently Playing")
            elif ind == 1:
                st.markdown("### 🎧 Next Up")
            else:
                st.markdown(f"#### {ind}. **{rec_song}** by **{rec_artist}**")

            st.markdown(f"**{rec_song}** by **{rec_artist}**")

            # ✅ FIX: only play preview if link is valid
            if isinstance(preview, str) and preview.strip() != "":
                st.audio(preview)
            else:
                st.write("⚠️ No audio preview available.")

            st.write("---")
