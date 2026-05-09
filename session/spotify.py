import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Spotify Analytics", layout="wide")

df = pd.read_csv("spotify.csv")

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Dataset", "Overview", "Music Analytics","Data Assistance"],
        icons=["table", "bar-chart", "music-note","robot"],
        menu_icon="play-circle",
        default_index=0
    )

#------Dataset Overview_____
if selected == "Dataset":

    st.title("Dataset Explorer")

    st.divider()

    col1,col2,col3=st.columns(3)

    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isna().sum().sum())

    st.divider()

# column selection
    selected_columns=st.multiselect("Select the columns to display",df.columns,default=df.columns)

    filtered_columns=df[selected_columns]

    # search dataset

    st.subheader("Searching in the dataset")

    search=st.text_input("Search any value")

    if search:
        filtered_columns = filtered_columns[
            filtered_columns.astype(str).apply(
                lambda row: row.str.contains(search, case=False).any(),
                axis=1
            )
        ]
    # column filter
    st.subheader("Column Filter")

    col1, col2 = st.columns(2)

    with col1:
        filter_column = st.selectbox("Select Column", filtered_columns.columns)

    with col2:
        filter_value = st.selectbox(
            "Select Value",
            filtered_columns[filter_column].dropna().unique()
        )

    if st.button("Apply Filter"):
        filtered_columns = filtered_columns[filtered_columns[filter_column] == filter_value]

    st.divider()

    # row display
    st.subheader("Row display")

    rows = st.slider(
        "Number of row display",
        min_value=10,
        max_value=len(filtered_columns),
        value=100
    )

    # dataset table
    st.subheader("Dataset Table")
    st.dataframe(filtered_columns.head(rows), use_container_width=True)

    # show full dataset
    if st.checkbox("Show all dataset"):
        st.dataframe(df, use_container_width=True)

    st.divider()

    # columns statistics
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    if len(numeric_cols) > 0:
        selected_col = st.selectbox("Select Numeric Column", numeric_cols)
        st.write(filtered_columns[selected_col].describe())

    st.divider()

    # download dataset
    st.subheader("Download dataset")

    csv = filtered_columns.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Dataset",
        csv,
        file_name="dataset.csv",
        mime="text/csv"
    )

# ---------------- OVERVIEW PAGE ---------------- #
# 1. Load Data
# df = pd.read_csv("spotify.csv")

if selected == "Overview":
    st.title("🎵 Spotify Insights: Strategic Catalog Overview")

    # --- Calculations ---
    total_tracks = len(df)
    total_streams = df["stream"].sum()

    # Defining "Hits" as tracks with popularity > 75
    hits_df = df[df["popularity"] > 75]
    hit_rate = (len(hits_df) / total_tracks * 100) if total_tracks > 0 else 0

    avg_popularity = df["popularity"].mean()
    avg_duration = df["duration"].mean()

    # --- KPI Row ---
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        label="Total Streams",
        value=f"{total_streams / 1e6:.1f}M",
        delta="Global Reach"
    )

    kpi2.metric(
        label="Hit Ratio",
        value=f"{hit_rate:.1f}%",
        delta="Pop > 75",
        delta_color="normal"
    )

    kpi3.metric(
        label="Avg Track Length",
        value=f"{avg_duration:.0f}s" if not pd.isna(avg_duration) else "N/A"
    )

    kpi4.metric(
        label="Avg Popularity",
        value=f"{avg_popularity:.1f}/100"
    )

    st.divider()

    # --- Genre Performance Matrix ---
    st.subheader("Genre Performance Matrix")

    genre_metrics = df.groupby("genre").agg(
        Total_Tracks=("song_id", "count"),
        Total_Streams=("stream", "sum"),
        Avg_Popularity=("popularity", "mean"),
        Avg_Duration=("duration", "mean")
    )

    genre_metrics["Stream Share %"] = (
        genre_metrics["Total_Streams"] / total_streams * 100
        if total_streams > 0 else 0
    )

    st.dataframe(
        genre_metrics.style.format({
            "Total_Streams": "{:,.0f}",
            "Avg_Popularity": "{:.1f}",
            "Avg_Duration": "{:.0f}s",
            "Stream Share %": "{:.2f}%"
        }).background_gradient(
            subset=["Total_Streams", "Stream Share %"],
            cmap="Greens"
        ),
        use_container_width=True
    )

    st.divider()

    # --- Content & Label Audit ---
    col_label, col_expl = st.columns(2)

    with col_label:
        st.subheader("Label Efficiency")
        st.write("Avg Popularity by Record Label")

        label_df = df.groupby("label")[["popularity", "stream"]].mean()

        st.dataframe(
            label_df.style
            .highlight_max(axis=0, color="#1DB954")
            .highlight_min(axis=0, color="#ff4b4b")
            .format("{:.1f}"),
            use_container_width=True
        )

    with col_expl:
        st.subheader("Content Audit")
        st.write("Explicit vs. Clean Split")

        explicit_count = df["explicit_content"].value_counts().to_frame(name="count")
        explicit_count["Share %"] = (explicit_count["count"] / total_tracks * 100)

        st.dataframe(
            explicit_count.style.format({"Share %": "{:.1f}%"}),
            use_container_width=True
        )

    # --- Financial/Stream Deep Dive ---
    st.subheader("Deep Dive: Artist & Language Trends")

    lang_col, artist_col = st.columns([4, 6])

    with lang_col:
        st.markdown("**Top Languages by Stream**")
        lang_summary = (
            df.groupby("language")["stream"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )
        st.dataframe(lang_summary.rename("Total Streams"), use_container_width=True)

    with artist_col:
        st.markdown("**Top Performing Artists**")
        top_artists = (
            df.groupby("artist")["stream"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )
        st.bar_chart(top_artists, color="#1DB954")

    # --- Data Quality Audit ---
    with st.expander("Catalog Integrity & Audit"):
        audit1, audit2 = st.columns(2)

        audit1.write(f"**Duplicate Songs:** {df.duplicated(subset=['song_id']).sum()}")
        audit2.write(f"**Missing Durations:** {df['duration'].isna().sum()}")

        st.info("Missing durations are usually metadata errors from the aggregator.")
        st.success("Executive Music Catalog Overview Generated")

if selected == "Music Analytics":
    tab1, tab2 = st.tabs(["Basic Charts", "Advanced Charts"])

    with tab1:
        st.title("📊 Basic Music Insights")

        # 1. Existing Genre Pie
        st.subheader("The Most Streamed Musical Styles")
        genre_count = df["genre"].value_counts().reset_index()
        fig_pie = px.pie(genre_count, names="genre", values="count", hole=0.5,
                         color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig_pie, use_container_width=True)

        # 2. NEW: Language Distribution (Crucial for Global Data)
        st.subheader("Global Language Presence")
        lang_data = df["language"].value_counts().head(10)
        fig_lang = px.bar(lang_data, x=lang_data.index, y=lang_data.values,
                          labels={'x': 'Language', 'y': 'Track Count'}, color=lang_data.values,
                          color_continuous_scale='Viridis')
        st.plotly_chart(fig_lang, use_container_width=True)

        # 3. NEW: Tracks Released per Year (Time Series)
        st.subheader("Release Momentum Over Years")
        df['release_year'] = pd.to_datetime(df['release_date']).dt.year
        year_counts = df['release_year'].value_counts().sort_index()
        fig_year = px.line(x=year_counts.index, y=year_counts.values, markers=True, title="Catalog Growth Over Time")
        st.plotly_chart(fig_year, use_container_width=True)

        # 4. Label Analysis
        st.subheader("Top 5 Dominant Record Labels")
        data2 = df["label"].value_counts().head(5)
        fig_labels = px.bar(x=data2.index, y=data2.values, color=data2.index)
        st.plotly_chart(fig_labels, use_container_width=True)

        # 5. Top 10 Producers (New) ---
        st.subheader("🎬 Top 10 Most Prolific Producers")
        producer_counts = df["producer"].value_counts().head(10)
        fig_prod = px.bar(
            producer_counts,
            orientation='h',
            color=producer_counts.values,
            labels={'value': 'Tracks Produced', 'index': 'Producer'},
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_prod, use_container_width=True)

        # --- 2. Stream Distribution (New) ---
        st.subheader("📈 Streaming Reach Distribution")
        # A histogram helps visualize if most songs are "niche" or "hits"
        fig_hist = px.histogram(
            df, x="stream",
            nbins=50,
            title="Frequency of Stream Counts",
            color_discrete_sequence=['#1DB954']
        )
        st.plotly_chart(fig_hist, use_container_width=True)

        # --- 3. Explicit Content Popularity (New) ---
        st.subheader("🔞 Popularity: Explicit vs. Clean")
        explicit_pop = df.groupby("explicit_content")["popularity"].mean().reset_index()
        fig_expl = px.bar(
            explicit_pop, x="explicit_content", y="popularity",
            color="explicit_content",
            color_discrete_map={'Yes': '#ff4b4b', 'No': '#1DB954'}
        )
        st.plotly_chart(fig_expl, use_container_width=True)

        st.divider()

    with tab2:
        st.title("🧪 Advanced Statistical Discovery")

        scatter_data = df.dropna(subset=["duration", "popularity"])

        fig_scatter = px.scatter(
            scatter_data, x="duration", y="popularity",
            color="genre",
            hover_data=["song_title", "artist"],
            trendline="ols",
            opacity=0.5
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        # 2. NEW: Popularity Spread (Box Plot)
        # Excellent for showing the "range" of success in each genre
        st.subheader("📦 Genre Popularity Variance")
        fig_box = px.box(df, x="genre", y="popularity", color="genre", title="Popularity Distribution per Genre")
        st.plotly_chart(fig_box, use_container_width=True)

        # 3. NEW: Explicit vs. Non-Explicit Streaming Impact
        st.subheader("🔞 Explicit Content vs. Streaming Performance")
        fig_strip = px.box(df, x="explicit_content", y="stream", color="explicit_content", notched=True)
        st.plotly_chart(fig_strip, use_container_width=True)

        # 4. NEW: Top 10 Artists by Total Engagement (Bubble Chart)
        st.subheader("👨‍🎤 Top 10 Artists: Total Streams vs Avg Popularity")
        artist_stats = df.groupby("artist").agg({
            "stream": "sum",
            "popularity": "mean",
            "song_id": "count"
        }).sort_values(by="stream", ascending=False).head(10).reset_index()

        fig_bubble = px.scatter(
            artist_stats, x="popularity", y="stream",
            size="song_id", color="artist",
            text="artist", log_y=True  # Log scale helps if streams vary wildly
        )
        st.plotly_chart(fig_bubble, use_container_width=True)

if selected == "Data Assistance":
    st.title("🤖 Sonic Data Assistant")
    st.divider()

    st.write("Ask questions about your music catalog (e.g., Streams, Genre, Popularity, Labels)")
    user_question = st.text_input("Enter your question here:")

    # New Feature: Toggle for Visuals
    show_visuals = st.radio("Display supporting analytics/graphs?", ("Yes", "No"), index=0, horizontal=True)

    if user_question:
        q = user_question.lower()

        # 1. Total Catalog/Track Questions
        if "total" in q or "track" in q or "catalog" in q:
            total = len(df)
            st.success(f"Total Tracks in Dataset: {total:,}")

            if show_visuals == "Yes":
                genre_dist = df["genre"].value_counts()
                fig = px.pie(names=genre_dist.index, values=genre_dist.values,
                             title="Catalog Composition by Genre", hole=0.4)
                st.plotly_chart(fig, use_container_width=True)

        # 2. Streaming Questions
        elif "stream" in q or "reach" in q:
            total_streams = df["stream"].sum()
            st.success(f"Total Global Streams: {total_streams:,}")

            if show_visuals == "Yes":
                # Streams by Genre
                stream_genre = df.groupby("genre")["stream"].sum().sort_values(ascending=False)
                fig = px.bar(x=stream_genre.index, y=stream_genre.values,
                             labels={"x": "Genre", "y": "Total Streams"},
                             title="Streaming Volume per Genre", color=stream_genre.values)
                st.plotly_chart(fig, use_container_width=True)

        # 3. Genre Questions
        elif "genre" in q or "type" in q:
            top_genre = df["genre"].value_counts().idxmax()
            st.success(f"The most dominant genre in this dataset is: **{top_genre}**")

            if show_visuals == "Yes":
                genre_counts = df["genre"].value_counts()
                fig = px.bar(x=genre_counts.index, y=genre_counts.values,
                             title="Genre Popularity (Count)", color=genre_counts.index)
                st.plotly_chart(fig, use_container_width=True)

        # 4. Popularity/Hit Questions
        elif "popular" in q or "hit" in q:
            avg_pop = df["popularity"].mean()
            st.success(f"The average popularity score across the catalog is: {avg_pop:.2f}/100")

            if show_visuals == "Yes":
                fig = px.histogram(df, x="popularity", nbins=20,
                                   title="Popularity Score Distribution", color_discrete_sequence=['#1DB954'])
                st.plotly_chart(fig, use_container_width=True)

        # 5. Record Label Questions
        elif "label" in q or "company" in q:
            top_label = df["label"].value_counts().idxmax()
            st.success(f"The label with the most releases is: **{top_label}**")

            if show_visuals == "Yes":
                label_data = df["label"].value_counts().head(10)
                fig = px.pie(names=label_data.index, values=label_data.values, title="Top 10 Labels by Market Share")
                st.plotly_chart(fig, use_container_width=True)

        # 6. Explicit Content Questions
        elif "explicit" in q or "adult" in q:
            explicit_perc = (df["explicit_content"].value_counts(normalize=True) * 100).get("Yes", 0)
            st.success(f"Percentage of Explicit Content: {explicit_perc:.1f}%")

            if show_visuals == "Yes":
                expl_count = df["explicit_content"].value_counts()
                fig = px.pie(names=expl_count.index, values=expl_count.values,
                             title="Content Rating Distribution", color=expl_count.index,
                             color_discrete_map={'Yes': '#ff4b4b', 'No': '#1DB954'})
                st.plotly_chart(fig, use_container_width=True)

        # 7. Duration Questions
        elif "long" in q or "duration" in q or "time" in q:
            avg_dur = df["duration"].mean()
            st.success(f"Average Track Duration: {avg_dur:.2f} seconds")

            if show_visuals == "Yes":
                fig = px.scatter(df, x="duration", y="popularity", color="genre",
                                 title="Track Duration vs. Popularity")
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning(
                "I didn't quite catch that. Try asking about Streams, Genres, Popularity, Labels, or Content Rating.")

    st.divider()
    st.info("Tip: You can ask 'What is the total stream count?' or 'Which label is most popular?'")