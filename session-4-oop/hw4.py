from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Optional


# =========================
# 1) LibraryItem (ABC)
# =========================
class LibraryItem(ABC):
    _id_counter: int = 1

    def __init__(self, title: str, creator: str, copies: int):
        if copies < 0:
            raise ValueError("copies must be >= 0")
        self.id: int = LibraryItem._id_counter
        LibraryItem._id_counter += 1

        self.title: str = title
        self.creator: str = creator
        self.total_copies: int = copies
        self.available_copies: int = copies

    def is_available(self) -> bool:
        return self.available_copies > 0

    def borrow(self) -> bool:
        if self.available_copies > 0:
            self.available_copies -= 1
            return True
        return False

    def return_item(self) -> bool:
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            return True
        return False

    @abstractmethod
    def get_item_info(self) -> str:
        ...

    @abstractmethod
    def get_item_type(self) -> str:
        ...

    def __str__(self) -> str:
        return f"{self.title} by {self.creator} (ID: {self.id})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LibraryItem):
            return False
        return self.id == other.id


# =========================
# 2) Book
# =========================
class Book(LibraryItem):
    def __init__(self, title: str, author: str, copies: int, isbn: str, num_pages: int):
        super().__init__(title, author, copies)
        self.author: str = author
        self.isbn: str = isbn
        self.num_pages: int = num_pages

    def get_item_type(self) -> str:
        return "Book"

    def get_item_info(self) -> str:
        return (
            f"Title: {self.title}\n"
            f"Author: {self.author}\n"
            f"ISBN: {self.isbn}\n"
            f"Pages: {self.num_pages}\n"
            f"Type: {self.get_item_type()}"
        )


# =========================
# 3) DVD
# =========================
class DVD(LibraryItem):
    def __init__(self, title: str, director: str, copies: int, duration_minutes: int, genre: str):
        super().__init__(title, director, copies)
        self.director: str = director
        self.duration_minutes: int = duration_minutes
        self.genre: str = genre

    def get_item_type(self) -> str:
        return "DVD"

    def get_item_info(self) -> str:
        return (
            f"Title: {self.title}\n"
            f"Director: {self.director}\n"
            f"Duration: {self.duration_minutes} minutes\n"
            f"Genre: {self.genre}\n"
            f"Type: {self.get_item_type()}"
        )


# =========================
# 4) Member (Observer base)
# =========================
class Member(ABC):
    _id_counter: int = 1

    def __init__(self, name: str, email: str):
        self.member_id: int = Member._id_counter
        Member._id_counter += 1

        self.name: str = name
        self.email: str = email
        self.borrowed_items: List[int] = []
        self.notifications: List[str] = []

    def can_borrow(self) -> bool:
        return self.get_borrowed_count() < self.get_max_borrow_limit()

    def borrow_item(self, item_id: int) -> bool:
        if item_id not in self.borrowed_items:
            self.borrowed_items.append(item_id)
            return True
        return False

    def return_item(self, item_id: int) -> bool:
        if item_id in self.borrowed_items:
            self.borrowed_items.remove(item_id)
            return True
        return False

    def get_borrowed_count(self) -> int:
        return len(self.borrowed_items)

    @abstractmethod
    def get_max_borrow_limit(self) -> int:
        ...

    # Observer hook
    def update(self, message: str) -> None:
        self.notifications.append(message)

    def get_notifications(self) -> List[str]:
        return list(self.notifications)

    def clear_notifications(self) -> None:
        self.notifications.clear()

    def __str__(self) -> str:
        return f"{self.name} ({self.member_id})"


# =========================
# 5) RegularMember
# =========================
class RegularMember(Member):
    MAX_BORROW_LIMIT: int = 3

    def __init__(self, name: str, email: str):
        super().__init__(name, email)

    def get_max_borrow_limit(self) -> int:
        return RegularMember.MAX_BORROW_LIMIT


# =========================
# 6) PremiumMember
# =========================
class PremiumMember(Member):
    MAX_BORROW_LIMIT: int = 5

    def __init__(self, name: str, email: str, membership_expiry: Optional[str] = None):
        super().__init__(name, email)
        self.membership_expiry: Optional[str] = membership_expiry

    def get_max_borrow_limit(self) -> int:
        return PremiumMember.MAX_BORROW_LIMIT


# =========================
# 7) Library (Singleton + Subject)
# =========================
class Library:
    _instance: Optional["Library"] = None

    def __new__(cls) -> "Library":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # initialize once
            cls._instance.items = {}
            cls._instance.members = {}
            cls._instance.waiting_list = {}
        return cls._instance

    # --- Items ---
    def add_item(self, item: LibraryItem) -> bool:
        if item.id in self.items:
            return False
        self.items[item.id] = item
        return True

    def remove_item(self, item_id: int) -> bool:
        if item_id in self.items:
            del self.items[item_id]
            self.waiting_list.pop(item_id, None)
            # Note: Any members holding this item will still have the ID listed;
            # a more robust system would enforce returns before deletion.
            return True
        return False

    def display_all_items(self) -> None:
        if not self.items:
            print("[No items]")
            return
        for it in self.items.values():
            print(f"{it} | Available: {it.available_copies}/{it.total_copies} | Type: {it.get_item_type()}")

    def search_items(self, query: str) -> List[LibraryItem]:
        q = query.lower()
        return [it for it in self.items.values() if q in it.title.lower() or q in it.creator.lower()]

    # --- Members ---
    def add_member(self, member: Member) -> bool:
        if member.member_id in self.members:
            return False
        self.members[member.member_id] = member
        return True

    def remove_member(self, member_id: int) -> bool:
        if member_id in self.members:
            # also remove member from any waiting list
            for wl in self.waiting_list.values():
                wl[:] = [m for m in wl if m.member_id != member_id]
            del self.members[member_id]
            return True
        return False

    def display_all_members(self) -> None:
        if not self.members:
            print("[No members]")
            return
        for m in self.members.values():
            print(f"{m} - Borrowed: {m.get_borrowed_count()}/{m.get_max_borrow_limit()}")

    # --- Borrow / Return ---
    def borrow_item(self, member_id: int, item_id: int) -> bool:
        member = self.members.get(member_id)
        item = self.items.get(item_id)
        if member is None or item is None:
            return False
        if not member.can_borrow():
            return False
        if not item.is_available():
            return False

        if item.borrow():
            member.borrow_item(item_id)
            return True
        return False

    def return_item(self, member_id: int, item_id: int) -> bool:
        member = self.members.get(member_id)
        item = self.items.get(item_id)
        if member is None or item is None:
            return False

        if member.return_item(item_id) and item.return_item():
            # Item became available; notify waiting members
            self.notify_waiting_members(item_id)
            return True
        return False

    # --- Waiting List (Observer pattern) ---
    def join_waiting_list(self, member_id: int, item_id: int) -> bool:
        member = self.members.get(member_id)
        item = self.items.get(item_id)
        if member is None or item is None:
            return False
        wl = self.waiting_list.setdefault(item_id, [])
        if member not in wl:
            wl.append(member)
            return True
        return False

    def leave_waiting_list(self, member_id: int, item_id: int) -> bool:
        member = self.members.get(member_id)
        wl = self.waiting_list.get(item_id, [])
        before = len(wl)
        self.waiting_list[item_id] = [m for m in wl if m.member_id != member_id]
        return len(self.waiting_list[item_id]) < before

    def get_waiting_list(self, item_id: int) -> List[Member]:
        return list(self.waiting_list.get(item_id, []))

    def notify_waiting_members(self, item_id: int) -> None:
        item = self.items.get(item_id)
        if not item:
            return
        wl = self.waiting_list.get(item_id, [])
        if not wl:
            return
        message = f"'{item.title}' is now available!"
        for m in wl:
            m.update(message)
        # keep list (spec says notify all; not necessarily auto-borrow or clear)
        # If you want to auto-clear after notify, uncomment next line:
        # self.waiting_list[item_id].clear()

    # --- Magic ---
    def __len__(self) -> int:
        return len(self.items)


# =========================
# Demo / Sample Usage
# =========================
def main():
    print("=" * 70)
    print("LIBRARY MANAGEMENT SYSTEM - DEMO")
    print("=" * 70)

    # Singleton library
    library = Library()

    # Add items
    book1 = Book("Python Crash Course", "Eric Matthes", 2, "978-1593279288", 544)
    book2 = Book("Clean Code", "Robert Martin", 2, "978-0132350884", 464)
    dvd1 = DVD("The Matrix", "Wachowski Brothers", 2, 136, "Sci-Fi")
    dvd2 = DVD("Inception", "Christopher Nolan", 1, 148, "Thriller")

    library.add_item(book1)
    library.add_item(book2)
    library.add_item(dvd1)
    library.add_item(dvd2)

    print(f"\n--- Added Items ---")
    print(f"Book: {book1} (ID: {book1.id})")
    print(f"DVD: {dvd1} (ID: {dvd1.id})")
    print(f"Total items: {len(library)}")

    # Polymorphism
    print(f"\n--- Polymorphism Demo: get_item_info() ---")
    print(book1.get_item_info())
    print(f"\n{dvd1.get_item_info()}")

    # Add members
    alice = RegularMember("Alice", "alice@email.com")
    bob = PremiumMember("Bob", "bob@email.com")
    charlie = RegularMember("Charlie", "charlie@email.com")

    library.add_member(alice)
    library.add_member(bob)
    library.add_member(charlie)

    print(f"\n--- Added Members ---")
    print(f"{alice} - Max: {alice.get_max_borrow_limit()} items")
    print(f"{bob} - Max: {bob.get_max_borrow_limit()} items")

    # Regular member borrows (max 3)
    print(f"\n--- Regular Member Borrowing (Max 3) ---")
    library.borrow_item(alice.member_id, book1.id)
    library.borrow_item(alice.member_id, dvd1.id)
    library.borrow_item(alice.member_id, book2.id)
    print(f"Alice borrowed: {alice.get_borrowed_count()}/{alice.get_max_borrow_limit()} items")

    # Try to exceed limit
    success = library.borrow_item(alice.member_id, dvd2.id)
    print(f"Alice trying 4th item: {success} (exceeded limit)")

    # Premium member borrows (max 5)
    print(f"\n--- Premium Member Borrowing (Max 5) ---")
    library.borrow_item(bob.member_id, dvd2.id)
    print(f"Bob borrowed: {bob.get_borrowed_count()}/{bob.get_max_borrow_limit()} items")
    print(f"'{dvd2.title}' available: {dvd2.available_copies}")

    # Waiting list & Observer
    print(f"\n--- Waiting List & Observer Pattern ---")
    success = library.borrow_item(charlie.member_id, dvd2.id)
    print(f"Charlie trying to borrow '{dvd2.title}': {success} (unavailable)")

    library.join_waiting_list(charlie.member_id, dvd2.id)
    print(f"Charlie joined waiting list")
    print(f"Waiting list size: {len(library.get_waiting_list(dvd2.id))}")

    # Return triggers notification
    print(f"\nBob returns '{dvd2.title}'...")
    library.return_item(bob.member_id, dvd2.id)
    print(f"Charlie's notifications: {charlie.get_notifications()}")

    # Search
    print(f"\n--- Search Items ---")
    results = library.search_items("Python")
    print(f"Search 'Python': {len(results)} result(s)")

    results = library.search_items("Matrix")
    print(f"Search 'Matrix': {len(results)} result(s)")

    # Display final state
    print(f"\n--- Final State ---")
    print(f"Total items: {len(library)}")
    library.display_all_items()

    print("\n" + "=" * 70)
    print("DEMO COMPLETED!")
    print("=" * 70)


if __name__ == "__main__":
    main()
