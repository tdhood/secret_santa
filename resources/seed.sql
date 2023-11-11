INSERT into users 
(email, username, first_name, password, phone_number) 
VALUES 
("user1@email.com", "user1", "one", "$2b$12$.DB4q/p07WIkr.Pzq59gU.ulYADUXpghBFX2I6pami4CnkFmSmkgC", "111-111-1111");

INSERT into users 
(email, username, first_name, password, phone_number) 
VALUES 
("user2@email.com", "user2", "two", "$2b$12$v0vILkL55i7FUvTLUS/iTebcuztQr8b0eBniJkEIMez03YaWmKyGq", "222-222-2222");

INSERT into users 
(email, username, first_name, password, phone_number) 
VALUES 
("user3@email.com", "user3", "three", "$2b$12$/OwV1RlU2XVnDGo3grNvqe97TJcD.korkJehmP2.lawcx2nfrHKOS", "333-333-3333");

INSERT into events 
(owner, title, deadline, is_event_live, is_santa_picked)
VALUES
(1, "christmas", "2023-12-01", TRUE, FALSE);

INSERT into events 
(owner, title, deadline, is_event_live, is_santa_picked)
VALUES
(1, "xmas", "2023-12-01", TRUE, TRUE);

INSERT into events 
(owner, title, deadline, is_event_live, is_santa_picked)
VALUES
(2, "easter", "2024-03-01", TRUE, FALSE);

INSERT into invites
(event_id, name, phone_number, status)
VALUES
(1, "two", "222-222-2222", TRUE);

INSERT into invites
(event_id, name, phone_number, status)
VALUES
(1, "three", "333-333-3333", FALSE);

INSERT into invites
(event_id, name, phone_number, status)
VALUES
(2, "three", "333-333-3333", TRUE);

INSERT into invites
(event_id, name, phone_number, status)
VALUES
(2, "one", "111-111-1111", TRUE);

INSERT into invites
(event_id, name, phone_number, status)
VALUES
(3, "one", "111-111-1111", TRUE);

INSERT into participants
(event_id, user_id)
VALUES
(1, 1);

INSERT into participants
(event_id, user_id)
VALUES
(1, 2);

INSERT into participants
(event_id, user_id)
VALUES
(2, 2);

INSERT into participants
(event_id, user_id)
VALUES
(2, 1);

INSERT into participants
(event_id, user_id)
VALUES
(2, 3);

INSERT into participants
(event_id, user_id)
VALUES
(3, 1);

INSERT into participants
(event_id, user_id)
VALUES
(3, 2);

INSERT into wishlists
(participant_id, notes)
VALUES
(1, "one's winter clothes");

INSERT into wishlists
(participant_id, notes)
VALUES
(2, "two's large sportsballs");

INSERT into wishlists
(participant_id, notes)
VALUES
(3, "two's small sportsballs");

INSERT into wishlists
(participant_id, notes)
VALUES
(4, "one's summer wear");

INSERT into wishlists
(participant_id, notes)
VALUES
(5, "three's food");

INSERT into wishlist_items
(wishlist_id, gift, url, notes)
VALUES
(1, "hat", "hats.com", "large");

INSERT into wishlist_items
(wishlist_id, gift, url, notes)
VALUES
(1, "red gloves", "gloves-r-us.com", "medium");

INSERT into wishlist_items
(wishlist_id, gift, url, notes)
VALUES
(2, "soccer ball", "sports-shop.com", "size 5");

INSERT into wishlist_items
(wishlist_id, gift, url)
VALUES
(2, "basketball", "hoops.com");

INSERT into wishlist_items
(wishlist_id, gift, url)
VALUES
(2, "bowling ball", "sports.com");

INSERT into wishlist_items
(wishlist_id, gift, url)
VALUES
(3, "golf ball", "sports.com");

INSERT into wishlist_items
(wishlist_id, gift, url)
VALUES
(4, "blue skirt", "summer.com");

INSERT into wishlist_items
(wishlist_id, gift, url)
VALUES
(5, "chocolate", "food.com");

INSERT into wishlist_items
(wishlist_id, gift, url)
VALUES
(5, "candy", "food.com");

INSERT into wishlist_items
(wishlist_id, gift, url)
VALUES
(5, "mango", "food.com");