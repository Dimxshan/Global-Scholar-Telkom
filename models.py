"""
models.py — OOP Class Architecture for Global Scholar Platform
==============================================================
Implements the UML Class Diagram from Skema_Arsitektur_Global_Scholar.md

Three OOP pillars applied:
  • Inheritance  — HousingListing / ItemListing extend Listing (base class)
  • Composition  — User owns MatchProfile; ChatGroup owns Message[]
  • Encapsulation — Private attrs via name-mangling (__password, __match_score)
"""

from datetime import datetime


# =====================================================================
#  CORE SYSTEM MODULE — Encapsulation & Composition
# =====================================================================

class User:
    """
    Base user account.
    Encapsulation: email, password, is_verified are private.
    Composition: owns one MatchProfile (destroyed if User is deleted).
    """

    def __init__(self, user_id: str, name: str, email: str, password: str,
                 avatar_seed: str = "", avatar_bg: str = "fecaca"):
        self.__user_id = user_id
        self.__email = email
        self.__password = password          # private — never exposed
        self.__is_verified = False           # must pass verification
        self.name = name
        self.avatar_seed = avatar_seed or name
        self.avatar_bg = avatar_bg

    # --- Getters (controlled access) ---
    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def email(self) -> str:
        return self.__email

    @property
    def is_verified(self) -> bool:
        return self.__is_verified

    # --- Verification logic (encapsulated) ---
    def verify_user(self, token: str) -> bool:
        """Only verifies if the token matches the campus validation."""
        if token == "VALID_CAMPUS_TOKEN":
            self.__is_verified = True
            return True
        return False

    @property
    def avatar_url(self) -> str:
        return (
            f"https://api.dicebear.com/9.x/avataaars/svg"
            f"?seed={self.avatar_seed}&backgroundColor={self.avatar_bg}"
        )

    def to_dict(self) -> dict:
        return {
            "user_id": self.__user_id,
            "name": self.name,
            "email": self.__email,
            "is_verified": self.__is_verified,
            "avatar_url": self.avatar_url,
        }


class Student(User):
    """
    Student extends User — adds university context.
    """

    def __init__(self, user_id, name, email, password,
                 origin_university="", target_university="",
                 major="", role="Exchange Student",
                 avatar_seed="", avatar_bg="fecaca"):
        super().__init__(user_id, name, email, password, avatar_seed, avatar_bg)
        self.origin_university = origin_university
        self.target_university = target_university
        self.major = major
        self.role = role

        # Composition: Student owns a MatchProfile
        self.match_profile = MatchProfile()

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "origin_university": self.origin_university,
            "target_university": self.target_university,
            "major": self.major,
            "role": self.role,
            "match_profile": self.match_profile.to_dict(),
        })
        return base


class MatchProfile:
    """
    Composition: exists only within a User/Student.
    Encapsulation: match_score is private — only calculated internally.
    """

    def __init__(self, sleep_schedule: str = "", study_habit: str = "",
                 cleanliness: str = "", tags: list = None):
        self.sleep_schedule = sleep_schedule
        self.study_habit = study_habit
        self.cleanliness = cleanliness
        self.tags = tags or []
        self.__match_score = 0  # private — encapsulated

    # --- Encapsulated getter ---
    @property
    def match_score(self) -> int:
        return self.__match_score

    # --- Encapsulated logic: internal score calculation ---
    def calculate_match_score(self, other: "MatchProfile") -> int:
        """
        Calculates compatibility score against another profile.
        Score is private and can only be set through this method.
        """
        score = 0
        if self.sleep_schedule == other.sleep_schedule:
            score += 40
        if self.study_habit == other.study_habit:
            score += 30
        if self.cleanliness == other.cleanliness:
            score += 30
        self.__match_score = score
        return score

    def set_score_directly(self, score: int):
        """Admin/system override for mock data."""
        self.__match_score = max(0, min(100, score))

    def to_dict(self) -> dict:
        return {
            "sleep_schedule": self.sleep_schedule,
            "study_habit": self.study_habit,
            "cleanliness": self.cleanliness,
            "tags": self.tags,
            "match_score": self.__match_score,
        }


# =====================================================================
#  COMMUNICATION MODULE — Composition
# =====================================================================

class Message:
    """
    Composition: owned by ChatGroup.
    If the group is deleted, all messages are destroyed.
    """

    def __init__(self, sender: User, content: str, timestamp: str = ""):
        self.sender = sender
        self.content = content
        self.timestamp = timestamp or datetime.now().strftime("%I:%M %p")

    def to_dict(self) -> dict:
        return {
            "sender": self.sender.to_dict(),
            "content": self.content,
            "timestamp": self.timestamp,
        }


class ChatGroup:
    """
    Composition: owns a list of Message objects.
    Deleting the group destroys all messages (strong ownership).
    """

    def __init__(self, group_id: str, group_name: str, initials: str = "",
                 gradient: str = "from-red-600 to-red-800",
                 members: list = None):
        self.group_id = group_id
        self.group_name = group_name
        self.initials = initials or group_name[:2].upper()
        self.gradient = gradient
        self.members = members or []

        # Composition: private chat history owned by this group
        self.__chat_history: list[Message] = []

    # --- Composition methods ---
    def send_message(self, sender: User, content: str) -> Message:
        msg = Message(sender, content)
        self.__chat_history.append(msg)
        return msg

    def get_chat_history(self) -> list[Message]:
        return list(self.__chat_history)

    @property
    def last_message(self) -> str:
        if self.__chat_history:
            last = self.__chat_history[-1]
            return f"{last.sender.name}: {last.content}"
        return "No messages yet"

    @property
    def last_time(self) -> str:
        if self.__chat_history:
            return self.__chat_history[-1].timestamp
        return ""

    @property
    def message_count(self) -> int:
        return len(self.__chat_history)

    def delete_group(self):
        """Composition: destroying group destroys all messages."""
        self.__chat_history.clear()

    def to_dict(self) -> dict:
        return {
            "group_id": self.group_id,
            "group_name": self.group_name,
            "initials": self.initials,
            "gradient": self.gradient,
            "members": [m.to_dict() for m in self.members],
            "last_message": self.last_message,
            "last_time": self.last_time,
            "message_count": self.message_count,
            "chat_history": [m.to_dict() for m in self.__chat_history],
        }


# =====================================================================
#  MARKETPLACE MODULE — Inheritance
# =====================================================================

class Listing:
    """
    Base class / Superclass for all marketplace listings.
    HousingListing and ItemListing inherit from this.
    """

    def __init__(self, listing_id: str, title: str, description: str,
                 owner: User, date_posted: str = ""):
        self.listing_id = listing_id
        self.title = title
        self.description = description
        self.owner = owner
        self.date_posted = date_posted or datetime.now().strftime("%b %d, %Y")
        self.tags: list[dict] = []

    def to_dict(self) -> dict:
        return {
            "listing_id": self.listing_id,
            "title": self.title,
            "description": self.description,
            "owner": self.owner.to_dict(),
            "date_posted": self.date_posted,
            "tags": self.tags,
            "listing_type": self.__class__.__name__,
        }


class HousingListing(Listing):
    """
    Subclass of Listing — for apartment/room sublets.
    Inherits: listing_id, title, description, owner, date_posted.
    Adds: rent_price, address, room_count, duration_months.
    """

    def __init__(self, listing_id, title, description, owner,
                 rent_price: float = 0, address: str = "",
                 room_count: int = 1, duration: str = "",
                 icon: str = "building-2", label: str = "Apartment",
                 gradient_bg: str = "from-red-100 via-red-50 to-orange-50",
                 icon_color: str = "text-red-300",
                 date_posted: str = ""):
        super().__init__(listing_id, title, description, owner, date_posted)
        self.rent_price = rent_price
        self.address = address
        self.room_count = room_count
        self.duration = duration
        self.icon = icon
        self.label = label
        self.gradient_bg = gradient_bg
        self.icon_color = icon_color

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "rent_price": self.rent_price,
            "address": self.address,
            "room_count": self.room_count,
            "duration": self.duration,
            "icon": self.icon,
            "label": self.label,
            "gradient_bg": self.gradient_bg,
            "icon_color": self.icon_color,
        })
        return base


class ItemListing(Listing):
    """
    Subclass of Listing — for textbooks, electronics, etc.
    Inherits: listing_id, title, description, owner, date_posted.
    Adds: item_price, item_condition, category.
    """

    def __init__(self, listing_id, title, description, owner,
                 item_price: float = 0, item_condition: str = "Used - Good",
                 category: str = "Other",
                 icon: str = "package", label: str = "Item",
                 badge: str = "ITEM", badge_color: str = "bg-gray-600",
                 gradient_bg: str = "from-gray-100 via-gray-50 to-slate-50",
                 icon_color: str = "text-gray-300",
                 date_posted: str = ""):
        super().__init__(listing_id, title, description, owner, date_posted)
        self.item_price = item_price
        self.item_condition = item_condition
        self.category = category
        self.icon = icon
        self.label = label
        self.badge = badge
        self.badge_color = badge_color
        self.gradient_bg = gradient_bg
        self.icon_color = icon_color

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "item_price": self.item_price,
            "item_condition": self.item_condition,
            "category": self.category,
            "icon": self.icon,
            "label": self.label,
            "badge": self.badge,
            "badge_color": self.badge_color,
            "gradient_bg": self.gradient_bg,
            "icon_color": self.icon_color,
        })
        return base
