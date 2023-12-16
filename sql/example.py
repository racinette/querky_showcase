from querky_def import qrk


# an UPDATE query: no value returned
@qrk.query  # or @qrk.query(shape='status')
def update_account_phone_number(account_id, new_phone_number):
    return f'''
        UPDATE
            account
        SET
            phone_number = {+new_phone_number}
        WHERE
            id = {+account_id}
        '''


# an INSERT query to always return a single value
@qrk.query(shape='value', optional=False)
def insert_account(username, first_name, last_name, phone_number, balance, referred_by_account_id):
    return f'''
        INSERT INTO
            account
            (
                username,
                first_name,
                last_name,
                phone_number,
                balance,
                referred_by_account_id
            )
        VALUES
            (
                {+username},
                {+first_name},
                {+last_name},
                {+phone_number},
                {+balance},
                {+referred_by_account_id}
            )
        RETURNING
            id
        '''


# a SELECT query to return an array of single values
@qrk.query(shape='column')
def select_top_largest_balances(limit):
    return f'''
        SELECT
            balance
        FROM
            account
        ORDER BY
            balance DESC
        LIMIT
            {+limit}
        '''


# now for the most interesting part: fetching rows
# a SELECT query to return a single (one) AccountReferrer row or None (optional)
@qrk.query('AccountReferrer', shape='one', optional=True)
def get_account_referrer(account_id):
    return f'''
        SELECT
            referrer.id,
            referrer.username,
            referrer.first_name,
            referrer.last_name,
            referrer.join_ts

        FROM 
            account

        INNER JOIN
            account AS referrer
        ON
            account.referred_by_account_id = referrer.id

        WHERE
            account.id = {+account_id}
        '''


# a SELECT query to return many (an array of) AccountPostComment rows
@qrk.query('AccountPostComment', shape='many')
def select_last_post_comments(post_id, limit):
    return f'''
        SELECT 
            account.first_name,
            account.last_name,
            post_comment.id,
            post_comment.message

        FROM
            post_comment

        INNER JOIN
            account
        ON
            post_comment.commenter_id = account.id

        WHERE
            post_comment.post_id = {+post_id}

        ORDER BY
            post_comment.ts DESC

        LIMIT
            {+limit}
        '''
