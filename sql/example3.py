from querky_def import qrk

from sql.example2 import get_account


@qrk.query(get_account, shape='one')
def get_last_joined_account():
    return f'''
        SELECT 
            first_name,
            last_name,
            username,
            phone_number
        FROM
            account
        ORDER BY
            join_ts DESC
        LIMIT
            1
        '''
