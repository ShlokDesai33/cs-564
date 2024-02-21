drop table if exists User;

CREATE TABLE User (
    user_id TEXT PRIMARY KEY,
    rating INTEGER,
    country TEXT,
    location TEXT
);

drop table if exists Item;

CREATE TABLE Item (
    item_id INTEGER PRIMARY KEY,
    user_id TEXT,
    name TEXT,
    currently DOUBLE,
    buy_price DOUBLE,
    first_bid DOUBLE,
    number_of_bids INTEGER,
    started DATETIME,
    ends DATETIME,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

drop table if exists Bid;

CREATE TABLE Bid (
    item_id INTEGER,
    user_id TEXT,
    time DATETIME,
    amount DOUBLE,
    PRIMARY KEY (time, item_id, user_id, amount),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (item_id) REFERENCES Item(item_id)
);

drop table if exists ItemCategory;

CREATE TABLE ItemCategory (
    item_id INTEGER,
    category TEXT,
    PRIMARY KEY (item_id, category),
    FOREIGN KEY (item_id) REFERENCES Item(item_id)
);
