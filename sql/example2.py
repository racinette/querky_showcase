import typing

from querky_def import qrk
from querky import subquery, attr


@qrk.query('AccountInfo', shape='one')
def get_account(account_id):
    return f'''
        SELECT 
            first_name,
            last_name,
            username,
            phone_number
        FROM
            account
        WHERE
            id = {+account_id}
        '''


@qrk.query(shape='value', optional=False)
def insert_account(
        username,
        first_name,
        last_name: typing.Optional,
        phone_number: typing.Optional,
        balance,
        referred_by_account_id=None
):
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


@qrk.query(shape="value", optional=False)
def insert_post(poster_id, message):
    return f'''
        INSERT INTO
            post
            (
                poster_id,
                message
            )
        VALUES
            (
                {+poster_id},
                {+message}
            )
        RETURNING
            id
        '''


@qrk.query(shape="value", optional=False)
def insert_post_comment(post_id, commenter_id, message):
    return f'''
        INSERT INTO
            post_comment
            (
                post_id,
                commenter_id,
                message
            )
        VALUES
            (
                {+post_id},
                {+commenter_id},
                {+message}
            )
        RETURNING
            id
        '''


@qrk.query('AccountReferrer', shape='one', optional=True)
def get_account_referrer(account_id):
    return f'''
        SELECT
            referrer.id,
            referrer.username,
            referrer.first_name,
            referrer.last_name AS {attr.last_name(optional=True)},
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


@qrk.query(shape='value', optional=False)
def are_2d_matrices_equal(m):
    return f"SELECT {+m} = ARRAY[[1,2,3], [1,2,3]]::INTEGER[]"


@qrk.query(shape='value', optional=False)
def are_2d_matrices_equal2(m: 'list[list[int]]'):
    return f"SELECT {+m} = ARRAY[[1,2,3], [1,2,3], [1,2,3]]::INTEGER[]"


@qrk.query('SimpleRow', shape='one')
def get_row():
    return f'''
        SELECT
            ARRAY[[1,2,3], [1,2,3], [1,2,3]]::INTEGER[] AS {attr.matrix2d('list[list[int]]')},
            ARRAY[[[1,2,3],[1,2,3]], [[1,2,3],[1,2,3]], [[1,2,3],[1,2,3]]]::INTEGER[] AS {attr.matrix3d('list[list[list[int]]]')},
            'Looks like text' AS {attr.definitely_not_text('float')}
        '''



@qrk.query(shape='value', optional=False)
def add(a, b):
    return f"SELECT {+a}::INTEGER + {+b}"


@qrk.query(shape='value', optional=False)
def multiply(a, b):
    return f"SELECT {+a}::INTEGER * {+b}"


@qrk.query(shape='value', optional=False)
def divide(a, b):
    return f"SELECT {+a}::INTEGER / {+b}"


@qrk.query(shape='value', optional=False)
def operation(a, b):

    @subquery
    def add_ab():
        return add.query(a, b)

    @subquery
    def mult_ab():
        return multiply.query(a, b)

    return divide.query(add_ab, mult_ab)


@qrk.query(shape='one', optional=False)
def all_default_types():
    return f'''
        SELECT
            NULL::INTEGER[] AS _anyarray,
            NULL::TSRANGE AS _anyrange,
            NULL::NUMMULTIRANGE AS _anymultirange,
            NULL::RECORD AS _record,
            NULL::VARBIT AS _bitstring,
            NULL::BOOL AS _bool,
            NULL::BOX AS _box,
            NULL::BYTEA AS _bytes,
            NULL::TEXT AS _text,
            NULL::CIDR AS _cidr,
            NULL::INET AS _inet,
            NULL::MACADDR AS _macaddr,
            NULL::CIRCLE AS _circle,
            NULL::DATE AS _date,
            NULL::TIME AS _time,
            NULL::TIME WITH TIME ZONE AS _timetz,
            NULL::INTERVAL AS _interval,
            NULL::FLOAT AS _float,
            NULL::DOUBLE PRECISION AS _double_precision,
            NULL::SMALLINT AS _smallint,
            NULL::INTEGER AS _integer,
            NULL::BIGINT AS _bigint,
            NULL::NUMERIC AS _numeric,
            NULL::JSON AS _json,
            NULL::JSONB AS _jsonb,
            NULL::LINE AS _line,
            NULL::LSEG AS _lseg,
            NULL::MONEY AS _money,
            NULL::PATH AS _path,
            NULL::POINT AS _point,
            NULL::POLYGON AS _polygon,
            NULL::UUID AS _uuid,
            NULL::TID AS _tid
        '''
