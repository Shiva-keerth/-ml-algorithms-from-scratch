import streamlit as st

st.set_page_config(page_title="AI Travel Finder", layout="wide")
st.title("AI Travel Finder")
st.write("Tell me your mood: **Adventure, Peace, Beach, Hills, Historical**")

# Data dictionary for recommendations
places = {
    "adventure": {
        "place": "Manali",
        "desc": "Perfect for trekking, paragliding and snow adventure in the Himalayas",
        "images": [
            "https://loremflickr.com/800/500/manali,himalayas",
            "https://loremflickr.com/800/500/solang,valley,snow"
        ],
        "video_search": "Manali travel guide"
    },
    "peace": {
        "place": "Rishikesh",
        "desc": "Calm place for yoga, meditation and riverside relaxation",
        "images": [
            "https://loremflickr.com/800/500/rishikesh,ganga",
            "https://loremflickr.com/800/500/laxman,jhula,rishikesh"
        ],
        "video_search": "Rishikesh travel guide"
    },
    "beach": {
        "place": "Goa",
        "desc": "Enjoy beaches, nightlife, water sports and casinos",
        "images": [
            "https://loremflickr.com/800/500/goa,beach,india",
            "https://loremflickr.com/800/500/baga,beach"
        ],
        "video_search": "Goa Travel Guide"
    },
    "hills": {
        "place": "Ladakh",
        "desc": "Bike riding with the beautiful straight roads surrounded by mountains",
        "images": [
            "https://loremflickr.com/800/500/ladakh",
            "https://loremflickr.com/800/500/leh,ladakh"
        ],
        "video_search": "Ladakh Travel guide"
    },
    "historical": {
        "place": "Jaipur",
        "desc": "Forts, palaces and royal Pink City heritage",
        "images": [
            "https://loremflickr.com/800/500/hawa,mahal,jaipur",
            "https://loremflickr.com/800/500/amber,fort,rajasthan"
        ],
        "video_search": "Jaipur travel guide"
    }
}

query = st.chat_input("Where do you want to go?")

if query:
    q = query.lower()
    found = False
    for mood in places:
        if mood in q:
            data = places[mood]
            st.subheader(f"Recommended Place: {data['place']}")
            st.info(data["desc"])

            st.subheader("Photos")
            cols = st.columns(2)
            for i, img_url in enumerate(data["images"]):
                cols[i % 2].image(img_url, use_container_width=True)

            st.subheader("Travel Video")
            yt_url = f"https://www.youtube.com/results?search_query={data['video_search'].replace(' ', '+')}"
            st.link_button(f"Watch {data['place']} Travel videos on YouTube", yt_url)

            st.subheader("Location")
            st.components.v1.iframe(f"https://maps.google.com/maps?q={data['place']}&output=embed", height=400)
            found = True
            break

    if not found:
        st.warning("Try typing: adventure, beach, hills, peace, historical")