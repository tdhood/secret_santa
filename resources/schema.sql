Drop Table users;
Drop Table events;
Drop Table invites;
Drop Table participants;
Drop Table wishlists;
Drop Table wishlist_items;
Drop Table secret_santas;



Create Table users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    username TEXT NOT NULL,
    first_name TEXT NOT NULL,
    password TEXT NOT NULL,
    phone_number TEXT NOT NULL
);

Create Table events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner INTEGER NOT NULL,
    title TEXT NOT NULL,
    deadline DATE NOT NULL,
    is_santa_picked BOOLEAN NOT NULL,
    is_event_live BOOLEAN NOT NULL,
    FOREIGN KEY (owner) REFERENCES users(id)
);

Create Table invites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    status BOOLEAN NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(id)
);

Create Table participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

Create Table wishlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id INTEGER NOT NULL,
    notes TEXT,
    FOREIGN KEY (participant_id) REFERENCES participants(id)
);

Create Table wishlist_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wishlist_id INTEGER NOT NULL,
    gift TEXT,
    url TEXT,
    image TEXT,
    notes TEXT,
    FOREIGN KEY (wishlist_id) REFERENCES wishlist(id)
);

Create Table secret_santas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    gifter INTEGER NOT NULL,
    giftee INTEGER NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(id)
);