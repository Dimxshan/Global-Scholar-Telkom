"""
app.py — Flask Application Router for Global Scholar Platform
==============================================================
Serves the multi-page dashboard with mock data instantiated
from the OOP models (models.py).
"""

from flask import Flask, render_template
from models import (
    Student, MatchProfile, ChatGroup, Message,
    HousingListing, ItemListing,
)

app = Flask(__name__)

# =====================================================================
#  MOCK DATA — Instantiated from OOP Models
# =====================================================================

# --- Students (User subclass, each owns a MatchProfile via Composition) ---

aisya = Student(
    user_id="U001", name="Aisya Putri",
    email="aisya@student.telkomuniversity.ac.id", password="secureHash001",
    origin_university="Telkom University",
    target_university="Yonsei University, Seoul",
    major="Informatics", role="Exchange Student",
    avatar_seed="Aisya", avatar_bg="fecaca",
)
aisya.verify_user("VALID_CAMPUS_TOKEN")
aisya.match_profile = MatchProfile(
    sleep_schedule="Night Owl", study_habit="Library Lover",
    cleanliness="Tidy",
    tags=[
        {"emoji": "🌙", "label": "Night Owl", "color": "bg-indigo-50 text-indigo-600 border-indigo-100"},
        {"emoji": "📚", "label": "Library Lover", "color": "bg-amber-50 text-amber-600 border-amber-100"},
        {"emoji": "🧹", "label": "Tidy", "color": "bg-emerald-50 text-emerald-600 border-emerald-100"},
    ],
)
aisya.match_profile.set_score_directly(100)

minjun = Student(
    user_id="U002", name="Kim Minjun",
    email="minjun@yonsei.ac.kr", password="secureHash002",
    origin_university="Yonsei University",
    target_university="Yonsei University, Seoul",
    major="Korean Studies", role="Local Buddy",
    avatar_seed="Minjun", avatar_bg="c0aede",
)
minjun.verify_user("VALID_CAMPUS_TOKEN")
minjun.match_profile = MatchProfile(
    sleep_schedule="Night Owl", study_habit="Library Lover",
    cleanliness="Tidy",
    tags=[
        {"emoji": "🌙", "label": "Night Owl", "color": "bg-indigo-50 text-indigo-600 border-indigo-100"},
        {"emoji": "📚", "label": "Library Lover", "color": "bg-amber-50 text-amber-600 border-amber-100"},
        {"emoji": "🧹", "label": "Tidy", "color": "bg-emerald-50 text-emerald-600 border-emerald-100"},
    ],
)
minjun.match_profile.set_score_directly(90)

yui = Student(
    user_id="U003", name="Tanaka Yui",
    email="yui@waseda.jp", password="secureHash003",
    origin_university="Waseda University",
    target_university="Waseda University, Tokyo",
    major="Literature", role="Exchange Student",
    avatar_seed="Yui", avatar_bg="ffdfbf",
)
yui.verify_user("VALID_CAMPUS_TOKEN")
yui.match_profile = MatchProfile(
    sleep_schedule="Early Bird", study_habit="Café Studier",
    cleanliness="Moderate",
    tags=[
        {"emoji": "☀️", "label": "Early Bird", "color": "bg-sky-50 text-sky-600 border-sky-100"},
        {"emoji": "🎵", "label": "Music Lover", "color": "bg-rose-50 text-rose-600 border-rose-100"},
        {"emoji": "📖", "label": "Café Studier", "color": "bg-violet-50 text-violet-600 border-violet-100"},
    ],
)
yui.match_profile.set_score_directly(70)

alex = Student(
    user_id="U004", name="Alex Rivera",
    email="alex@koreau.ac.kr", password="secureHash004",
    origin_university="UC Berkeley",
    target_university="Korea University, Seoul",
    major="Engineering", role="Exchange Student",
    avatar_seed="Alex", avatar_bg="d1d4f9",
)
alex.verify_user("VALID_CAMPUS_TOKEN")
alex.match_profile = MatchProfile(
    sleep_schedule="Night Owl", study_habit="Group Study",
    cleanliness="Moderate",
    tags=[
        {"emoji": "🌙", "label": "Night Owl", "color": "bg-indigo-50 text-indigo-600 border-indigo-100"},
        {"emoji": "🏃", "label": "Active", "color": "bg-teal-50 text-teal-600 border-teal-100"},
        {"emoji": "🍳", "label": "Home Cook", "color": "bg-orange-50 text-orange-600 border-orange-100"},
    ],
)
alex.match_profile.set_score_directly(80)

priya = Student(
    user_id="U005", name="Priya Sharma",
    email="priya@yonsei.ac.kr", password="secureHash005",
    origin_university="IIT Delhi",
    target_university="Yonsei University, Seoul",
    major="Business", role="Exchange Student",
    avatar_seed="Priya", avatar_bg="ffd5dc",
)
priya.verify_user("VALID_CAMPUS_TOKEN")
priya.match_profile = MatchProfile(
    sleep_schedule="Early Bird", study_habit="Library Lover",
    cleanliness="Tidy",
    tags=[
        {"emoji": "☀️", "label": "Early Bird", "color": "bg-sky-50 text-sky-600 border-sky-100"},
        {"emoji": "📚", "label": "Library Lover", "color": "bg-amber-50 text-amber-600 border-amber-100"},
        {"emoji": "🌿", "label": "Vegan", "color": "bg-lime-50 text-lime-600 border-lime-100"},
    ],
)
priya.match_profile.set_score_directly(60)

ALL_STUDENTS = [minjun, yui, alex, priya]  # excludes current user (aisya)
CURRENT_USER = aisya

# --- Chat Groups (Composition: each Group owns its Message list) ---

group_seoul = ChatGroup("G001", "Seoul Fall 24", "SF", "from-red-600 to-red-800",
                        members=[aisya, minjun, alex, priya])
group_seoul.send_message(minjun, "Hey everyone! 👋 I found a great place near Sinchon station. ₩650,000/month each.")
group_seoul.send_message(alex, "That sounds awesome! 🙌 Is it close to Yonsei campus?")
group_seoul.send_message(minjun, "Yes! Only 10-min walk 🚶‍♂️ I'll post it on the marketplace.")
group_seoul.send_message(aisya, "That's perfect! I'm definitely interested 🎉 Can we schedule a visit?")
group_seoul.send_message(priya, "Count me in too! 🙋‍♀️ Let's do Saturday?")

group_tokyo = ChatGroup("G002", "Tokyo Spring 25", "TS", "from-rose-400 to-rose-600",
                        members=[aisya, yui])
group_tokyo.send_message(yui, "Has anyone checked the Waseda dorms?")

group_ku = ChatGroup("G003", "KU Housing Search", "KU", "from-emerald-500 to-emerald-700",
                     members=[aisya, alex])
group_ku.send_message(alex, "The Anam area is affordable 👍")

group_yonsei = ChatGroup("G004", "Yonsei Buddy Club", "YB", "from-purple-500 to-purple-700",
                         members=[aisya, minjun, priya])
group_yonsei.send_message(priya, "Welcome all new exchange students! 🎉")

group_market = ChatGroup("G005", "Marketplace Deals", "MD", "from-amber-500 to-amber-600",
                         members=[aisya, minjun, yui])
group_market.send_message(minjun, "Selling Korean textbooks cheap!")

ALL_GROUPS = [group_seoul, group_tokyo, group_ku, group_yonsei, group_market]

# --- Marketplace: HousingListing (extends Listing) ---

h1 = HousingListing(
    listing_id="H001", title="Cozy Room near Sinchon Station",
    description="Bright furnished room in shared 3BR apartment. 10-min walk to Yonsei campus. WiFi, washing machine, AC.",
    owner=minjun, rent_price=650000, address="12-8 Sinchon-dong, Seodaemun-gu, Seoul",
    room_count=3, duration="Sep 2024 – Feb 2025 (6 months)",
    icon="building-2", label="Sinchon Apartment",
    gradient_bg="from-red-100 via-red-50 to-orange-50", icon_color="text-red-300",
)
h1.tags = [
    {"label": "Near Campus", "color": "bg-red-50 text-red-600 border-red-100"},
    {"label": "Furnished", "color": "bg-emerald-50 text-emerald-600 border-emerald-100"},
    {"label": "WiFi", "color": "bg-violet-50 text-violet-600 border-violet-100"},
]

h2 = HousingListing(
    listing_id="H002", title="Studio Apartment in Anam",
    description="Private studio with kitchenette near Korea University. Quiet neighborhood. Utilities included.",
    owner=alex, rent_price=480000, address="45 Anam-ro, Seongbuk-gu, Seoul",
    room_count=1, duration="Mar 2025 – Aug 2025 (6 months)",
    icon="building", label="Anam Studio",
    gradient_bg="from-emerald-100 via-emerald-50 to-amber-50", icon_color="text-emerald-300",
)
h2.tags = [
    {"label": "Utilities Incl.", "color": "bg-emerald-50 text-emerald-600 border-emerald-100"},
    {"label": "Quiet Area", "color": "bg-amber-50 text-amber-600 border-amber-100"},
    {"label": "Private", "color": "bg-sky-50 text-sky-600 border-sky-100"},
]

h3 = HousingListing(
    listing_id="H003", title="Hongdae Share House — Lively Area",
    description="Vibrant share house in Hongdae. Common lounge, rooftop access, and weekly community events.",
    owner=priya, rent_price=550000, address="78 Wausan-ro, Mapo-gu, Seoul",
    room_count=1, duration="Sep 2024 – Feb 2025 (6 months)",
    icon="home", label="Hongdae Share House",
    gradient_bg="from-purple-100 via-purple-50 to-pink-50", icon_color="text-purple-300",
)
h3.tags = [
    {"label": "Rooftop", "color": "bg-purple-50 text-purple-600 border-purple-100"},
    {"label": "Community", "color": "bg-pink-50 text-pink-600 border-pink-100"},
    {"label": "Events", "color": "bg-orange-50 text-orange-600 border-orange-100"},
]

ALL_HOUSING = [h1, h2, h3]

# --- Marketplace: ItemListing (extends Listing) ---

i1 = ItemListing(
    listing_id="I001", title="Korean Grammar in Use (Intermediate)",
    description="Essential grammar textbook for TOPIK Level 3-4. Some highlighting, all pages intact. Practice CD included.",
    owner=minjun, item_price=25000, item_condition="Like New", category="Language Learning",
    icon="book-open", label="Textbook", badge="TEXTBOOK", badge_color="bg-orange-500",
    gradient_bg="from-orange-100 via-orange-50 to-amber-50", icon_color="text-orange-300",
)
i1.tags = [
    {"label": "TOPIK Prep", "color": "bg-orange-50 text-orange-600 border-orange-100"},
    {"label": "Korean", "color": "bg-red-50 text-red-600 border-red-100"},
    {"label": "With CD", "color": "bg-emerald-50 text-emerald-600 border-emerald-100"},
]

i2 = ItemListing(
    listing_id="I002", title="Samsung Galaxy Tab S6 Lite (2022)",
    description="Great for note-taking. Comes with S Pen and protective case. Minor scratch on back, screen perfect.",
    owner=yui, item_price=180000, item_condition="Used - Good", category="Electronics",
    icon="laptop", label="Electronics", badge="ELECTRONICS", badge_color="bg-sky-600",
    gradient_bg="from-sky-100 via-sky-50 to-indigo-50", icon_color="text-sky-300",
)
i2.tags = [
    {"label": "With S Pen", "color": "bg-sky-50 text-sky-600 border-sky-100"},
    {"label": "Note-taking", "color": "bg-indigo-50 text-indigo-600 border-indigo-100"},
    {"label": "Case Incl.", "color": "bg-amber-50 text-amber-600 border-amber-100"},
]

i3 = ItemListing(
    listing_id="I003", title="Intro to Business Economics (3rd Ed.)",
    description="Required reading for BUS101 at Yonsei. Some wear on covers, content readable. Budget-friendly.",
    owner=priya, item_price=15000, item_condition="Used - Acceptable", category="Business & Economics",
    icon="book-marked", label="Textbook", badge="TEXTBOOK", badge_color="bg-rose-500",
    gradient_bg="from-rose-100 via-rose-50 to-amber-50", icon_color="text-rose-300",
)
i3.tags = [
    {"label": "BUS101", "color": "bg-rose-50 text-rose-600 border-rose-100"},
    {"label": "Budget Pick", "color": "bg-amber-50 text-amber-600 border-amber-100"},
    {"label": "Yonsei", "color": "bg-violet-50 text-violet-600 border-violet-100"},
]

ALL_ITEMS = [i1, i2, i3]


# =====================================================================
#  FLASK ROUTES
# =====================================================================

@app.route("/")
def index():
    """Buddy Finder — renders student profile cards with match scores."""
    return render_template(
        "index.html",
        page="buddy",
        current_user=CURRENT_USER,
        buddies=ALL_STUDENTS,
    )


@app.route("/messages")
def messages():
    """Secure Messaging — group chats with message composition."""
    return render_template(
        "messages.html",
        page="messages",
        current_user=CURRENT_USER,
        groups=ALL_GROUPS,
        active_group=ALL_GROUPS[0],
    )


@app.route("/marketplace")
def marketplace():
    """Student Marketplace — housing sublets + items/textbooks."""
    return render_template(
        "marketplace.html",
        page="marketplace",
        current_user=CURRENT_USER,
        housing_listings=ALL_HOUSING,
        item_listings=ALL_ITEMS,
    )


@app.route("/profile")
def profile():
    """User profile page — detailed info and active listings."""
    user_housing = [h for h in ALL_HOUSING if h.owner.user_id == CURRENT_USER.user_id]
    user_items = [it for it in ALL_ITEMS if it.owner.user_id == CURRENT_USER.user_id]
    return render_template(
        "profile.html",
        page="profile",
        current_user=CURRENT_USER,
        user_housing=user_housing,
        user_items=user_items,
        all_groups=[g for g in ALL_GROUPS if CURRENT_USER in g.members],
    )


# =====================================================================
#  RUN
# =====================================================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)
