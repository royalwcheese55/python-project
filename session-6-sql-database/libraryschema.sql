-- Drop tables if they exist (for dev/demo)
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS waiting_list;
DROP TABLE IF EXISTS borrowed_items;
DROP TABLE IF EXISTS memberships;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS dvds;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS library_items;

-- 1. library_items
CREATE TABLE library_items (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(255) NOT NULL,
    creator         VARCHAR(255) NOT NULL,
    item_type       VARCHAR(20)  NOT NULL CHECK (item_type IN ('book', 'dvd')),
    total_copies    INTEGER      NOT NULL DEFAULT 1 CHECK (total_copies >= 0),
    available_copies INTEGER     NOT NULL DEFAULT 1 CHECK (available_copies >= 0),
    created_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- 2. books
CREATE TABLE books (
    id         INTEGER PRIMARY KEY REFERENCES library_items(id) ON DELETE CASCADE,
    isbn       VARCHAR(20) NOT NULL UNIQUE,
    num_pages  INTEGER     NOT NULL CHECK (num_pages > 0)
);

-- 3. dvds
CREATE TABLE dvds (
    id               INTEGER PRIMARY KEY REFERENCES library_items(id) ON DELETE CASCADE,
    duration_minutes INTEGER     NOT NULL CHECK (duration_minutes > 0),
    genre            VARCHAR(50) NOT NULL
);

-- 4. members
CREATE TABLE members (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(255) NOT NULL,
    email         VARCHAR(255) NOT NULL UNIQUE,
    membership_id INTEGER, -- will link to memberships.id (1-1)
    created_at    TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);

-- 5. memberships
CREATE TABLE memberships (
    id               SERIAL PRIMARY KEY,
    member_id        INTEGER NOT NULL UNIQUE REFERENCES members(id) ON DELETE CASCADE,
    membership_type  VARCHAR(20) NOT NULL CHECK (membership_type IN ('regular', 'premium')),
    borrow_limit     INTEGER     NOT NULL CHECK (borrow_limit > 0),
    expiry_date      DATE,
    created_at       TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);

-- Now that memberships exists, add FK from members.membership_id → memberships.id
ALTER TABLE members
    ADD CONSTRAINT fk_members_membership
    FOREIGN KEY (membership_id)
    REFERENCES memberships(id);

-- 6. borrowed_items
CREATE TABLE borrowed_items (
    id           SERIAL PRIMARY KEY,
    member_id    INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    item_id      INTEGER NOT NULL REFERENCES library_items(id) ON DELETE CASCADE,
    borrow_date  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_date  TIMESTAMP,
    status       VARCHAR(20) NOT NULL DEFAULT 'borrowed'
        CHECK (status IN ('borrowed', 'returned'))
);

-- 7. waiting_list
CREATE TABLE waiting_list (
    id         SERIAL PRIMARY KEY,
    member_id  INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    item_id    INTEGER NOT NULL REFERENCES library_items(id) ON DELETE CASCADE,
    joined_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_waiting_member_item UNIQUE (member_id, item_id)
);

-- 8. notifications
CREATE TABLE notifications (
    id         SERIAL PRIMARY KEY,
    member_id  INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    message    TEXT    NOT NULL,
    is_read    BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
