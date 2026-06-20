"""
models.py — OOP Class Architecture for Global Scholar Platform
==============================================================
Implements the UML Class Diagram from Skema_Arsitektur_Global_Scholar.md

Four OOP pillars applied:
  • Abstraction   — User and Listing are abstract base classes
  • Inheritance   — HousingListing / ItemListing extend Listing (base class)
  • Composition   — User owns MatchProfile; ChatGroup owns Message[]
  • Encapsulation — Private attrs via name-mangling (__password, __match_score)
  • Polymorphism  — Searchable interface realized by Student and Listing
"""

from datetime import datetime
from abc import ABC, abstractmethod


# =====================================================================
#  SEARCHABLE INTERFACE — Polymorphism
#  Realized by: Student, HousingListing, ItemListing
# =====================================================================

class Searchable(ABC):
    """
    Interface (abstract base class) for all searchable entities.
    Polymorphism: the global search bar processes any Searchable object
    without needing to know the underlying type (Student vs Listing).
    """

    @abstractmethod
    def get_search_keywords(self) -> list[str]:
        """Returns a list of keywords this object can be found by."""
        pass

    @abstractmethod
    def get_match_score(self, query: str) -> float:
        """
        Returns a relevance score (0.0 - 1.0) for a given search query.
        Polymorphic: each class calculates this differently.
        """
        pass


# =====================================================================
#  CORE SYSTEM MODULE — Abstraction, Encapsulation & Composition
# =====================================================================

class User(ABC):
    """
    Abstract base class for all users.
    Cannot be instantiated directly — must use Student subclass.
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

    @abstractmethod
    def login(self, email: str, password: str) -> bool:
        """Abstract: each user type may have different login logic."""
        pass

    def update_profile(self, name: str = None, avatar_seed: str = None):
        """Updates public profile fields."""
        if name:
            self.name = name
        if avatar_seed:
            self.avatar_seed = avatar_seed

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


class Student(User, Searchable):
    """
    Student extends User — adds university context.
    Realizes Searchable — can be found via global search.
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
        self.__preferred_roommate_id = None  # encapsulated

        # Composition: Student owns a MatchProfile
        self.match_profile = MatchProfile()

    # --- User abstract method implementation ---
    def login(self, email: str, password: str) -> bool:
        """Basic credential check (in real app: hash comparison)."""
        return self.email == email

    def set_roommate_preference(self, friend_id: str) -> None:
        """Encapsulated setter for preferred roommate."""
        self.__preferred_roommate_id = friend_id

    def get_roommate_preference(self) -> str:
        return self.__preferred_roommate_id

    def apply_for_housing(self, housing_listing) -> str:
        """
        Student applies for a housing listing.
        Returns a confirmation message.
        """
        if not housing_listing.is_active:
            return f"Cannot apply: '{housing_listing.title}' is no longer active."
        return (
            f"Application submitted for '{housing_listing.title}' "
            f"by {self.name}."
        )

    # --- Searchable interface implementation ---
    def get_search_keywords(self) -> list[str]:
        """Polymorphism: Student returns name, university, major as keywords."""
        return [
            self.name.lower(),
            self.origin_university.lower(),
            self.target_university.lower(),
            self.major.lower(),
            self.role.lower(),
        ]

    def get_match_score(self, query: str) -> float:
        """
        Polymorphism: calculates how relevant this Student is to a search query.
        Returns a score between 0.0 and 1.0.
        """
        query = query.lower()
        keywords = self.get_search_keywords()
        matches = sum(1 for kw in keywords if query in kw)
        return round(matches / len(keywords), 2) if keywords else 0.0

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "origin_university": self.origin_university,
            "target_university": self.target_university,
            "major": self.major,
            "role": self.role,
            "preferred_roommate_id": self.__preferred_roommate_id,
            "match_profile": self.match_profile.to_dict(),
        })
        return base


class MatchProfile:
    """
    Composition: exists only within a Student.
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
        """For seeding mock data only — not for production use."""
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

    def add_member(self, student: Student) -> None:
        """Adds a student to the group if not already a member."""
        if student not in self.members:
            self.members.append(student)

    def broadcast_message(self, message: Message) -> None:
        """Broadcasts a pre-built Message object to the chat history."""
        self.__chat_history.append(message)

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
#  MARKETPLACE MODULE — Abstraction & Inheritance
# =====================================================================

class Listing(Searchable):
    """
    Abstract base class for all marketplace listings.
    Cannot be instantiated directly.
    HousingListing and ItemListing inherit from this.
    Realizes Searchable — both subclasses are globally searchable.
    """

    def __init__(self, listing_id: str, title: str, description: str,
                 owner: User, date_posted: str = ""):
        self.listing_id = listing_id
        self.title = title
        self.description = description
        self.owner = owner
        self.date_posted = date_posted or datetime.now().strftime("%b %d, %Y")
        self.tags: list[dict] = []
        self.__is_active = True  # encapsulated — use activate()/deactivate()

    @property
    def is_active(self) -> bool:
        return self.__is_active

    def activate(self) -> None:
        """Makes this listing visible/available."""
        self.__is_active = True

    def deactivate(self) -> None:
        """Hides this listing from the marketplace."""
        self.__is_active = False

    # --- Searchable interface implementation (shared by all listings) ---
    def get_search_keywords(self) -> list[str]:
        """Polymorphism: Listing returns title, description, owner name."""
        return [
            self.title.lower(),
            self.description.lower(),
            self.owner.name.lower(),
        ]

    def get_match_score(self, query: str) -> float:
        """
        Polymorphism: calculates relevance score for a listing.
        Title match is weighted higher than description.
        """
        query = query.lower()
        score = 0.0
        if query in self.title.lower():
            score += 0.6
        if query in self.description.lower():
            score += 0.3
        if query in self.owner.name.lower():
            score += 0.1
        return round(min(score, 1.0), 2)

    def to_dict(self) -> dict:
        return {
            "listing_id": self.listing_id,
            "title": self.title,
            "description": self.description,
            "owner": self.owner.to_dict(),
            "date_posted": self.date_posted,
            "tags": self.tags,
            "is_active": self.__is_active,
            "listing_type": self.__class__.__name__,
        }


class HousingListing(Listing):
    """
    Subclass of Listing — for apartment/room sublets.
    Inherits: listing_id, title, description, owner, date_posted, is_active.
    Adds: rent_price, address, room_count, duration.
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

    def book_viewing(self, student: Student) -> str:
        """
        Student books a viewing for this housing listing.
        Returns a confirmation string.
        """
        if not self.is_active:
            return f"'{self.title}' is no longer available for viewing."
        return (
            f"Viewing booked for '{self.title}' by {student.name}. "
            f"Contact {self.owner.name} to confirm the schedule."
        )

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
    Inherits: listing_id, title, description, owner, date_posted, is_active.
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
        self.__is_sold = False  # encapsulated

    @property
    def is_sold(self) -> bool:
        return self.__is_sold

    def mark_as_sold(self) -> None:
        """
        Marks this item as sold and automatically deactivates the listing.
        Encapsulation: __is_sold can only be changed through this method.
        """
        self.__is_sold = True
        self.deactivate()  # sold items are hidden from marketplace

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
            "is_sold": self.__is_sold,
        })
        return base


# =====================================================================
#  GLOBAL SEARCH UTILITY — Demonstrates Polymorphism
# =====================================================================

def global_search(query: str, searchables: list[Searchable]) -> list[dict]:
    """
    Polymorphic search: accepts any list of Searchable objects
    (Students, HousingListings, ItemListings) without knowing their type.
    This is polymorphism in action — same function, different behaviors.
    """
    results = []
    for obj in searchables:
        score = obj.get_match_score(query)
        if score > 0:
            results.append({
                "object": obj,
                "score": score,
                "type": obj.__class__.__name__,
            })
    # Sort by relevance score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results