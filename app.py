
import streamlit as st
import json
import html
import uuid
from pathlib import Path


# --------------------------------------------------
# YARN IT: CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Yarn It",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = Path(__file__).with_name("yarn_it_data.json")
UPLOAD_DIR = Path(__file__).with_name("yarn_it_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# COLOUR THEME AND STYLING
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
    --green: #285B43;
    --green-dark: #193D2D;
    --pink: #F8E6EC;
    --pink-dark: #EAC3D1;
    --gold: #C5A253;
    --cream: #FFFAF8;
    --text: #26392F;
    --muted: #78847B;
}

.stApp {
    background: var(--cream);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: var(--green) !important;
}

[data-testid="stSidebar"] {
    background: var(--pink);
    border-right: 1px solid var(--pink-dark);
}

[data-testid="stSidebar"] h1 {
    font-size: 2.2rem;
}

.stButton > button,
.stFormSubmitButton > button {
    background: var(--green);
    color: white;
    border: 1px solid var(--gold);
    border-radius: 9px;
    min-height: 42px;
    font-weight: 600;
    transition: background 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: var(--green-dark);
    color: white;
    border-color: var(--gold);
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 8px;
}

[data-testid="stMetric"] {
    background: var(--pink);
    border: 1px solid var(--pink-dark);
    border-radius: 12px;
    padding: 18px;
}

[data-testid="stMetricLabel"] {
    color: var(--green);
}

[data-testid="stMetricValue"] {
    color: var(--green-dark);
}

.yarn-eyebrow {
    color: #927638;
    font-size: 0.76rem;
    letter-spacing: 2px;
    font-weight: 700;
    text-transform: uppercase;
}

.yarn-banner {
    background: linear-gradient(120deg, #285B43, #193D2D);
    color: #FFFAF8;
    padding: 36px;
    border-radius: 18px;
    border-bottom: 4px solid var(--gold);
    margin: 12px 0 26px 0;
}

.yarn-banner h2 {
    color: white !important;
    font-size: 2.25rem;
    margin-bottom: 10px;
}

.yarn-banner p {
    color: #F8E6EC;
    font-size: 1rem;
    line-height: 1.7;
}

.yarn-card {
    background: white;
    border: 1px solid #E9D9D9;
    border-radius: 14px;
    padding: 22px;
    min-height: 150px;
    margin-bottom: 12px;
}

.yarn-card h3 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.08rem;
    margin-bottom: 10px;
}

.yarn-card p {
    color: #65736A;
    font-size: 0.93rem;
    line-height: 1.65;
}

.yarn-tag {
    color: var(--green);
    background: var(--pink);
    border-radius: 20px;
    padding: 5px 10px;
    font-size: 0.77rem;
    display: inline-block;
}

hr {
    border-color: #E9D9D9;
}

#MainMenu, footer {
    visibility: hidden;
}

@media (max-width: 768px) {
    .yarn-banner {
        padding: 24px;
    }
    .yarn-banner h2 {
        font-size: 1.8rem;
    }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SAVE AND LOAD PROJECT DATA
# --------------------------------------------------

def load_data():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, dict) and isinstance(
                    data.get("projects", []), list
                ):
                    data.setdefault("projects", [])
                    data.setdefault("uploads", [])
                    return data
        except (json.JSONDecodeError, OSError):
            pass

    return {"projects": [], "uploads": []}


def save_data(data):
    temporary_file = DATA_FILE.with_suffix(".tmp")
    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    temporary_file.replace(DATA_FILE)


if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data
data.setdefault("projects", [])
data.setdefault("uploads", [])


def save_current_data():
    save_data(st.session_state.data)


def find_project(project_name):
    for project in st.session_state.data["projects"]:
        if project["name"] == project_name:
            return project
    return None


def navigate_to(destination):
    """Change the sidebar page before Streamlit renders the next run."""
    st.session_state["section_nav"] = destination


# --------------------------------------------------
# CROCHET LEARNING CONTENT
# --------------------------------------------------

lessons = {
    "Slip Knot": {
        "level": "Beginner",
        "purpose": "Creates the starting loop for most crochet projects.",
        "steps": [
            "Make a loop with your yarn, leaving a short tail.",
            "Pull a section of the working yarn through the loop.",
            "Place the new loop on your crochet hook.",
            "Pull gently on the working yarn to adjust the loop around the hook."
        ]
    },
    "Chain Stitch": {
        "level": "Beginner",
        "purpose": "Creates a foundation chain and spaces within many patterns.",
        "steps": [
            "Start with a slip knot on your hook.",
            "Wrap the working yarn over the hook.",
            "Pull the yarn through the loop already on your hook.",
            "Repeat to make the required number of chain stitches."
        ]
    },
    "Single Crochet": {
        "level": "Beginner",
        "purpose": "Creates a compact fabric useful for bags, toys and other projects.",
        "steps": [
            "Insert your hook into the indicated stitch.",
            "Wrap the yarn over your hook and pull up a loop.",
            "You should have two loops on the hook.",
            "Wrap the yarn over again and pull through both loops."
        ]
    },
    "Double Crochet": {
        "level": "Beginner",
        "purpose": "Creates a taller stitch used in garments, blankets and granny squares.",
        "steps": [
            "Wrap the yarn over your hook.",
            "Insert your hook into the indicated stitch.",
            "Wrap the yarn over and pull up a loop.",
            "Wrap the yarn over and pull through the first two loops.",
            "Wrap the yarn over once more and pull through the remaining two loops."
        ]
    },
    "Slip Stitch": {
        "level": "Beginner",
        "purpose": "Joins stitches or rounds and moves across stitches without adding much height.",
        "steps": [
            "Insert your hook into the indicated stitch.",
            "Wrap the yarn over your hook.",
            "Pull the yarn through the stitch and the loop on your hook."
        ]
    }
}


# --------------------------------------------------
# PATTERN LIBRARY
# --------------------------------------------------

patterns = {
    "Crochet Bookmark": {
        "difficulty": "Beginner",
        "category": "Accessories",
        "materials": [
            "Cotton yarn",
            "Suitable crochet hook",
            "Scissors",
            "Yarn needle"
        ],
        "description": "A simple rectangular bookmark for everyday use.",
        "instructions": [
            "Chain 9.",
            "Starting in the second chain from the hook, single crochet across. You should have 8 stitches.",
            "Chain 1 and turn. Single crochet in each stitch across.",
            "Repeat the previous row until the bookmark reaches your preferred length.",
            "Fasten off and weave in the loose ends."
        ],
        "rows": 20
    },
    "Basic Scarf": {
        "difficulty": "Beginner",
        "category": "Clothing",
        "materials": [
            "Soft yarn",
            "Matching crochet hook",
            "Scissors",
            "Yarn needle"
        ],
        "description": "A straightforward scarf made with single crochet stitches.",
        "instructions": [
            "Chain 21.",
            "Starting in the second chain from the hook, single crochet across. You should have 20 stitches.",
            "Chain 1 and turn.",
            "Single crochet in each stitch across.",
            "Repeat until the scarf reaches your preferred length.",
            "Fasten off and weave in the loose ends."
        ],
        "rows": 30
    },
    "Granny Square": {
        "difficulty": "Beginner to intermediate",
        "category": "Home and accessories",
        "materials": [
            "Yarn in one or more colours",
            "Matching crochet hook",
            "Scissors",
            "Yarn needle"
        ],
        "description": "A traditional square that can be joined to make blankets, bags and cardigans.",
        "instructions": [
            "Make a slip knot and chain 4. Join with a slip stitch to form a ring.",
            "Chain 3, then work double crochet stitches and chain spaces into the ring to begin the first round.",
            "For a typical granny-square structure, work groups of 3 double crochet stitches into spaces. Use chain spaces to form corners.",
            "Continue adding rounds, keeping the corner spaces consistent so the square can grow.",
            "Fasten off, weave in the ends, and block the square if desired."
        ],
        "rows": 4
    },
    "Simple Dishcloth": {
        "difficulty": "Beginner",
        "category": "Home",
        "materials": [
            "Cotton yarn",
            "Matching crochet hook",
            "Scissors",
            "Yarn needle"
        ],
        "description": "A practical square cloth made with an easy stitch pattern.",
        "instructions": [
            "Chain 26.",
            "Starting in the second chain from the hook, single crochet across. You should have 25 stitches.",
            "Chain 1 and turn.",
            "Single crochet across every row, keeping the stitch count consistent.",
            "Continue until the cloth is approximately square.",
            "Fasten off and weave in the loose ends."
        ],
        "rows": 25
    }
}


# --------------------------------------------------
# PROJECT IDEAS
# --------------------------------------------------

ideas = [
    {
        "name": "Oversized Cardigan",
        "category": "Clothing",
        "level": "Intermediate",
        "description": "A relaxed cardigan with long sleeves and a comfortable fit.",
        "materials": "Yarn, hook, measuring tape, stitch markers"
    },
    {
        "name": "Everyday Tote Bag",
        "category": "Bags",
        "level": "Beginner to intermediate",
        "description": "A reusable bag with a sturdy base and comfortable handles.",
        "materials": "Durable yarn, hook, yarn needle"
    },
    {
        "name": "Crochet Flowers",
        "category": "Accessories",
        "level": "Beginner",
        "description": "Small flowers for accessories, gifts and decorative arrangements.",
        "materials": "Small amounts of yarn in your chosen colours"
    },
    {
        "name": "Granny Square Sweater",
        "category": "Clothing",
        "level": "Intermediate",
        "description": "A colourful garment assembled from individual crochet squares.",
        "materials": "Several yarn colours, hook, measuring tape"
    },
    {
        "name": "Bucket Hat",
        "category": "Accessories",
        "level": "Beginner to intermediate",
        "description": "A practical hat with a brim that can be adjusted to your style.",
        "materials": "Yarn, hook, stitch markers"
    },
    {
        "name": "Soft Plush Toy",
        "category": "Toys",
        "level": "Intermediate",
        "description": "A handmade stuffed toy using amigurumi techniques.",
        "materials": "Yarn, hook, stuffing, yarn needle"
    },
    {
        "name": "Decorative Cushion",
        "category": "Home",
        "level": "Beginner to intermediate",
        "description": "A textured cushion cover that adds a handmade touch to a room.",
        "materials": "Yarn, hook, cushion insert"
    },
    {
        "name": "Crochet Shoulder Bag",
        "category": "Bags",
        "level": "Intermediate",
        "description": "A compact bag with a strap for carrying everyday essentials.",
        "materials": "Yarn, hook, strap material if desired"
    }
]


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

valid_sections = [
    "Home", "Learn", "Patterns", "Ideas Gallery",
    "Upload Ideas", "Colour Inspiration", "My Projects"
]
if st.session_state.get("section_nav") not in valid_sections:
    st.session_state["section_nav"] = "Home"

with st.sidebar:
    st.markdown(
        '<p class="yarn-eyebrow">YOUR CREATIVE WORKSPACE</p>',
        unsafe_allow_html=True
    )
    st.title("Yarn It")
    st.caption("Make something by hand.")

    st.divider()

    section = st.radio(
        "NAVIGATION",
        [
            "Home",
            "Learn",
            "Patterns",
            "Ideas Gallery",
            "Upload Ideas",
            "Colour Inspiration",
            "My Projects"
        ],
        label_visibility="visible",
        key="section_nav"
    )

    st.divider()


# --------------------------------------------------
# HOME
# --------------------------------------------------

if section == "Home":
    st.markdown(
        '<p class="yarn-eyebrow">A SPACE FOR YOUR NEXT CREATION</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="yarn-banner">
        <h2>Make time for making.</h2>
        <p>
            Learn new stitches, browse crochet inspiration, explore
            colour combinations and collect ideas for your next project.
        </p>
    </div>
    """, unsafe_allow_html=True)

    total_projects = len(data["projects"])
    a, b = st.columns(2)
    a.metric("Your projects", total_projects)
    b.metric("Saved inspiration pictures", len(data.get("uploads", [])))

    st.divider()
    st.subheader("Explore Yarn It")
    st.write("Choose where you want to begin.")

    left, right = st.columns(2)

    with left:
        st.markdown("""
        <div class="yarn-card">
            <span class="yarn-tag">LEARN</span>
            <h3>Build your skills</h3>
            <p>Explore crochet stitches with clear, step-by-step lessons.</p>
        </div>
        """, unsafe_allow_html=True)

        st.button("Explore lessons", use_container_width=True, on_click=navigate_to, args=("Learn",))

        st.markdown("""
        <div class="yarn-card">
            <span class="yarn-tag">COLOUR</span>
            <h3>Find colours that work together</h3>
            <p>Explore colour palettes for your next crochet project.</p>
        </div>
        """, unsafe_allow_html=True)

        st.button("Explore colour inspiration", use_container_width=True, on_click=navigate_to, args=("Colour Inspiration",))

    with right:
        st.markdown("""
        <div class="yarn-card">
            <span class="yarn-tag">CREATE</span>
            <h3>Find your next pattern</h3>
            <p>Explore written instructions for beginner-friendly projects.</p>
        </div>
        """, unsafe_allow_html=True)

        st.button("Browse patterns", use_container_width=True, on_click=navigate_to, args=("Patterns",))

        st.markdown("""
        <div class="yarn-card">
            <span class="yarn-tag">DISCOVER</span>
            <h3>Get inspired</h3>
            <p>Browse project ideas, from garments to bags and home decor.</p>
        </div>
        """, unsafe_allow_html=True)

        st.button("View project ideas", use_container_width=True, on_click=navigate_to, args=("Ideas Gallery",))

    st.button("Upload inspiration", use_container_width=True, on_click=navigate_to, args=("Upload Ideas",))


# --------------------------------------------------
# LEARN
# --------------------------------------------------

elif section == "Learn":
    st.markdown(
        '<p class="yarn-eyebrow">LEARN AT YOUR OWN PACE</p>',
        unsafe_allow_html=True
    )
    st.title("Crochet lessons")
    st.write(
        "Start with the basics and work through each technique "
        "at your own pace."
    )

    selected_lesson = st.selectbox(
        "Choose a stitch or technique",
        list(lessons.keys())
    )

    lesson = lessons[selected_lesson]

    st.markdown('<div class="yarn-card">', unsafe_allow_html=True)
    st.markdown(f"### {selected_lesson}")
    st.markdown(
        f'<span class="yarn-tag">{lesson["level"]}</span>',
        unsafe_allow_html=True
    )
    st.write(lesson["purpose"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("Follow these steps")

    for index, step in enumerate(lesson["steps"], start=1):
        st.markdown(f"**Step {index}**")
        st.write(step)

    st.info(
        "Crochet terminology and stitch height can vary between "
        "US and UK patterns. Check which terminology a pattern uses."
    )


# --------------------------------------------------
# BROWSE PATTERNS: SEARCH UPLOADED IMAGES
# --------------------------------------------------

elif section == "Patterns":
    st.markdown('<p class="yarn-eyebrow">SEARCH AND EXPLORE</p>', unsafe_allow_html=True)
    st.title("Browse crochet inspiration")
    st.write("Search pictures that people have uploaded to this Yarn It library. A picture is for inspiration; instructions appear only when the uploader has provided a pattern.")

    pattern_search = st.text_input("What would you like to see?", placeholder="Try bag, scarf, flowers or cardigan", key="pattern_search")
    uploaded_items = data.get("uploads", [])
    matching_images = [
        item for item in uploaded_items
        if pattern_search.casefold() in " ".join([
            item.get("name", ""), item.get("category", ""),
            item.get("description", ""), item.get("tags", "")
        ]).casefold()
    ]

    if not matching_images:
        st.info("No pictures match this search yet. Upload a crochet picture in Upload Ideas, then search for its name or category here.")
        st.button("Upload a picture", on_click=navigate_to, args=("Upload Ideas",))
    else:
        image_columns = st.columns(3)
        for index, item in enumerate(matching_images):
            with image_columns[index % 3]:
                image_path = Path(__file__).parent / item.get("image", "")
                if image_path.exists():
                    st.image(str(image_path), use_container_width=True)
                st.markdown(f"### {html.escape(item.get('name', 'Untitled idea'))}")
                st.caption(item.get("category", "Other"))
                if item.get("description"):
                    st.write(item["description"])
                if item.get("pattern_text", "").strip():
                    with st.expander("View uploaded pattern"):
                        st.write(item["pattern_text"])
                else:
                    st.caption("No pattern available for this picture.")
                if st.button("Save picture to My Projects", key=f"pattern_save_image_{item.get('id', index)}", use_container_width=True):
                    project_name = item.get("name", "Crochet idea")
                    if find_project(project_name):
                        st.info("This idea is already in My Projects.")
                    else:
                        data["projects"].append({
                            "name": project_name, "pattern": item.get("pattern_text", ""),
                            "notes": item.get("description", ""),
                            "difficulty": item.get("level", "Not specified"),
                            "image": item.get("image", "")
                        })
                        save_current_data()
                        st.success("Picture saved to My Projects.")


# --------------------------------------------------
# IDEAS GALLERY
# --------------------------------------------------

elif section == "Ideas Gallery":
    st.markdown('<p class="yarn-eyebrow">YOUR NEXT PROJECT STARTS HERE</p>', unsafe_allow_html=True)
    st.title("Crochet ideas")
    st.write("Search ideas you've saved to Yarn It, or add new inspiration in the Upload Ideas.")

    saved_uploads = data.get("uploads", [])
    search_query = st.text_input("Search crochet ideas", placeholder="Try bag, flowers, cardigan or blanket", key="idea_search")
    categories = ["All"] + sorted({item.get("category", "Other") for item in saved_uploads})
    selected_category = st.selectbox("Filter by category", categories, key="idea_category")
    matching_uploads = []
    for item in saved_uploads:
        searchable = " ".join([item.get("name", ""), item.get("category", ""), item.get("description", ""), item.get("tags", "")]).casefold()
        if search_query.casefold() in searchable and (selected_category == "All" or item.get("category", "Other") == selected_category):
            matching_uploads.append(item)

    if matching_uploads:
        st.caption(f"Showing {len(matching_uploads)} saved image(s). Search only includes images uploaded to this Yarn It app.")
        columns = st.columns(3)
        for index, item in enumerate(matching_uploads):
            with columns[index % 3]:
                image_path = Path(__file__).parent / item.get("image", "")
                if image_path.exists():
                    st.image(str(image_path), use_container_width=True)
                st.markdown(f"### {html.escape(item.get('name', 'Untitled idea'))}")
                st.caption(f"{item.get('category', 'Other')} · {item.get('level', 'Not specified')}")
                st.write(item.get("description", "No notes added."))
                if st.button("Save to My Projects", key=f"save_upload_{item.get('id', index)}", use_container_width=True):
                    project_name = item.get("name", "Crochet idea")
                    existing = find_project(project_name)
                    if existing:
                        st.info("This idea is already in My Projects.")
                    else:
                        data["projects"].append({"name": project_name, "pattern": "", "row": 0, "stitches": 0, "notes": item.get("description", "") + "\nCategory: " + item.get("category", "Other"), "difficulty": item.get("level", "Not specified"), "image": item.get("image", "")})
                        save_current_data()
                        st.success("Idea saved to My Projects.")
    else:
        st.info("No matching uploaded pictures yet. Open Upload Ideas to upload crochet photos. After you upload them, search by name or category here.")
        st.button("Open Upload Ideas", use_container_width=True, on_click=navigate_to, args=("Upload Ideas",))


# --------------------------------------------------
# INSPIRATION LIBRARY AND IMAGE UPLOADS
# --------------------------------------------------

elif section == "Upload Ideas":
    st.markdown('<p class="yarn-eyebrow">COLLECT IDEAS YOU LOVE</p>', unsafe_allow_html=True)
    st.title("Upload Ideas")
    st.write("Upload crochet pictures from your computer, give each one a name, and search your saved collection later.")
    st.info("Yarn It searches the images you upload into this app. It does not automatically search the whole internet.")

    with st.expander("Upload a crochet picture", expanded=not data.get("uploads")):
        with st.form("upload_inspiration_form", clear_on_submit=True):
            upload_name = st.text_input("Name", placeholder="For example, crochet shoulder bag")
            upload_category = st.selectbox("Category", ["Bags", "Clothing", "Accessories", "Home", "Toys", "Flowers", "Blankets", "Other"])
            upload_level = st.selectbox("Difficulty", ["Beginner", "Beginner to intermediate", "Intermediate", "Advanced", "Inspiration only"] )
            upload_description = st.text_area("Notes or project details", placeholder="Add materials or details about this design.")
            upload_tags = st.text_input("Search tags (optional)", placeholder="e.g. tote, granny square, pink")
            upload_pattern_text = st.text_area("Pattern instructions (optional)", placeholder="Paste the instructions here if you have them. Leave blank if this is only an inspiration picture.")
            uploaded_pattern_file = st.file_uploader("Or upload pattern instructions as a .txt file (optional)", type=["txt"], key="uploaded_pattern_file")
            uploaded_image = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg", "webp"], help="Use a crochet photo you own or have permission to use.")
            submit_upload = st.form_submit_button("Save to Upload Ideas", use_container_width=True)
            if submit_upload:
                clean_name = upload_name.strip()
                if not clean_name:
                    st.error("Please enter a name for this image.")
                elif uploaded_image is None:
                    st.error("Please choose an image to upload.")
                else:
                    suffix = Path(uploaded_image.name).suffix.lower()
                    if suffix not in {".png", ".jpg", ".jpeg", ".webp"}:
                        suffix = ".jpg"
                    image_filename = f"yarn_it_uploads/{uuid.uuid4().hex}{suffix}"
                    image_path = Path(__file__).parent / image_filename
                    image_path.parent.mkdir(exist_ok=True)
                    image_path.write_bytes(uploaded_image.getvalue())
                    pattern_text = upload_pattern_text.strip()
                    if uploaded_pattern_file is not None:
                        file_text = uploaded_pattern_file.getvalue().decode("utf-8", errors="replace").strip()
                        if file_text:
                            pattern_text = file_text
                    data.setdefault("uploads", []).append({"id": uuid.uuid4().hex, "name": clean_name, "category": upload_category, "level": upload_level, "description": upload_description.strip(), "tags": upload_tags.strip(), "pattern_text": pattern_text, "image": image_filename})
                    save_current_data()
                    st.success("Picture saved. Search its name or category in Browse Patterns. If you added instructions, they will appear with the picture.")
                    st.rerun()

    st.divider()
    st.subheader("Your uploaded pictures")
    uploads = data.get("uploads", [])
    if not uploads:
        st.write("Your library is empty. Upload your first crochet image above to get started.")
    else:
        library_search = st.text_input("Search your library", placeholder="Search by name, category or tag", key="library_search")
        visible_uploads = [item for item in uploads if library_search.casefold() in " ".join([item.get("name", ""), item.get("category", ""), item.get("description", ""), item.get("tags", "")]).casefold()]
        cols = st.columns(3)
        for index, item in enumerate(visible_uploads):
            with cols[index % 3]:
                image_path = Path(__file__).parent / item.get("image", "")
                if image_path.exists():
                    st.image(str(image_path), use_container_width=True)
                st.markdown(f"### {html.escape(item.get('name', 'Untitled idea'))}")
                st.caption(f"{item.get('category', 'Other')} · {item.get('level', 'Not specified')}")
                if item.get("description"):
                    st.write(item["description"])
                if st.button("Delete image", key=f"delete_upload_{item.get('id', index)}"):
                    if image_path.exists():
                        image_path.unlink()
                    data["uploads"] = [saved for saved in data["uploads"] if saved.get("id") != item.get("id")]
                    save_current_data()
                    st.rerun()


# --------------------------------------------------
# COLOUR INSPIRATION
# --------------------------------------------------

elif section == "Colour Inspiration":
    st.markdown('<p class="yarn-eyebrow">PLAN YOUR COLOUR STORY</p>', unsafe_allow_html=True)
    st.title("Colour inspiration")
    st.write("Explore yarn colour combinations for your next crochet idea. Choose a palette to see the colours and their hex codes.")

    palettes = {
        "Garden Morning": [("Sage green", "#A3B18A"), ("Forest green", "#285B43"), ("Cream", "#FFFAF0"), ("Soft pink", "#F2C6D2")],
        "Blush and Gold": [("Baby pink", "#F8E6EC"), ("Rose", "#D98FA3"), ("Warm gold", "#C5A253"), ("Ivory", "#FFF8E7")],
        "Ocean Calm": [("Dusty blue", "#8FAFC0"), ("Deep teal", "#2F6F68"), ("Sand", "#DCC7A1"), ("White", "#FFFFFF")],
        "Autumn Market": [("Rust", "#B65F3C"), ("Mustard", "#D6A63D"), ("Olive", "#737C48"), ("Cream", "#F6EBDD")],
        "Soft Neutrals": [("Oatmeal", "#D8C8B4"), ("Taupe", "#A28B78"), ("Chocolate", "#5D4037"), ("Off-white", "#F8F4EC")],
        "Berry Mix": [("Berry", "#8F3D61"), ("Pink", "#E7A5B7"), ("Lilac", "#B9A0CC"), ("Cream", "#FFF5E8")],
    }
    selected_palette = st.selectbox("Choose a palette", list(palettes.keys()))
    swatches = palettes[selected_palette]
    swatch_columns = st.columns(len(swatches))
    for column, (colour_name, colour_hex) in zip(swatch_columns, swatches):
        with column:
            st.markdown(f'<div style="background:{colour_hex};height:110px;border-radius:12px;border:1px solid #ddd;"></div>', unsafe_allow_html=True)
            st.markdown(f"**{colour_name}**")
            st.code(colour_hex, language=None)

    st.divider()
    st.subheader("Make your own palette")
    custom_colours = st.columns(4)
    custom_palette = []
    for index, column in enumerate(custom_colours, start=1):
        with column:
            custom_palette.append(st.color_picker(f"Colour {index}", ["#285B43", "#F8E6EC", "#C5A253", "#FFFAF8"][index - 1], key=f"custom_palette_{index}"))
    preview_columns = st.columns(4)
    for column, colour in zip(preview_columns, custom_palette):
        with column:
            st.markdown(f'<div style="height:70px;background:{colour};border:1px solid #ddd;border-radius:10px;"></div>', unsafe_allow_html=True)
            st.code(colour, language=None)
    st.caption("Colour previews are digital references. Yarn shades can look different in person and under different lighting.")


# --------------------------------------------------
# MY PROJECTS
# --------------------------------------------------

elif section == "My Projects":
    st.markdown(
        '<p class="yarn-eyebrow">YOUR PERSONAL WORKSPACE</p>',
        unsafe_allow_html=True
    )
    st.title("My projects")
    st.write(
        "Save crochet pictures and ideas, and keep notes about the projects you want to make."
    )

    with st.expander("Create a new project", expanded=not data["projects"]):
        with st.form("create_project_form"):
            new_name = st.text_input(
                "Project name",
                placeholder="For example, my first cardigan"
            )

            new_type = st.selectbox(
                "Project type",
                [
                    "Original project",
                    "Clothing",
                    "Bag",
                    "Accessory",
                    "Home decor",
                    "Toy",
                    "Other"
                ]
            )

            new_notes = st.text_area(
                "Notes",
                placeholder="Materials, colours, size or other details"
            )

            submitted = st.form_submit_button("Save project")

            if submitted:
                clean_name = new_name.strip()

                if not clean_name:
                    st.error("Please enter a project name.")
                elif find_project(clean_name):
                    st.error("A project with this name already exists.")
                else:
                    data["projects"].append({
                        "name": clean_name,
                        "pattern": "",
                        "row": 0,
                        "stitches": 0,
                        "notes": (
                            "Type: " + new_type + "\n" + new_notes
                        ).strip(),
                        "difficulty": "Not specified"
                    })
                    save_current_data()
                    st.success("Your project has been saved.")
                    st.rerun()

    st.divider()
    st.subheader("Saved projects")

    if not data["projects"]:
        st.write(
            "Your project list is empty. Create a project above or save an idea from Browse Patterns."
        )
    else:
        names = [
            project["name"] for project in data["projects"]
        ]

        chosen_name = st.selectbox(
            "Choose a project to manage",
            names,
            key="manage_project"
        )

        project = find_project(chosen_name)

        st.markdown(f"### {project['name']}")

        updated_notes = st.text_area(
            "Project notes",
            value=project.get("notes", ""),
            key=f"notes_{chosen_name}"
        )

        if st.button("Save notes"):
            project["notes"] = updated_notes
            save_current_data()
            st.success("Notes saved.")

        with st.expander("Remove this project"):
            st.warning(
                "Removing a project also removes its saved details and notes from this app."
            )

            confirm_delete = st.checkbox(
                "I want to remove this project",
                key=f"confirm_{chosen_name}"
            )

            if st.button("Delete project"):
                if confirm_delete:
                    data["projects"] = [
                        item for item in data["projects"]
                        if item["name"] != chosen_name
                    ]
                    save_current_data()
                    st.success("Project removed.")
                    st.rerun()
                else:
                    st.error("Confirm the removal first.")

    st.divider()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()
st.caption("Yarn It | A crochet inspiration and project library")