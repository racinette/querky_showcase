CREATE TABLE account (
    id BIGSERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT,
    phone_number TEXT,
    balance BIGINT NOT NULL DEFAULT 0,
    join_ts TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    referred_by_account_id BIGINT REFERENCES account (id)
);

CREATE TABLE post (
    id BIGSERIAL PRIMARY KEY,
    poster_id BIGINT NOT NULL REFERENCES account (id),
    message TEXT NOT NULL,
    ts TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE post_comment (
    id BIGSERIAL PRIMARY KEY,
    post_id BIGINT NOT NULL REFERENCES post (id),
    commenter_id BIGINT NOT NULL REFERENCES account (id),
    message TEXT NOT NULL,
    ts TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
