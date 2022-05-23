# Postgres driver
import psycopg2
import uuid
import sys
import ast


def connect_db():
    # establishing the connection
    return psycopg2.connect(database="foo", user='foouser',
                            password='foopass', host='localhost', port='5434')


def insert_uid_data():
    print('Call Insert uid Data')
    # get connection instance
    conn = connect_db()
    # Setting auto commit false
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    with open('new-uid.txt') as f:
        uid_list = f.read().splitlines()

    allocation_group_id = select_uid_allocation_group()
    idx = allocation_group_id

    for uid in uid_list:
        result = ''.join([i for i in uid if not i.isdigit()])
        if result == "instructor":
            continue

        # Preparing SQL queries to INSERT a record into the database.
        cursor.execute(
            "insert into resources.allocation (uid, group_id, image_id, target_id, sequence, requested_date) values (%s,%s,10010,100010,0,CURRENT_TIMESTAMP)",
            (uid, idx))
        idx += 1

    # Commit your changes in the database
    conn.commit()
    print("Records inserted........")

    # Closing the connection
    conn.close()


def insert_group_data():
    # get connection instance
    conn = connect_db()
    # Setting auto commit false
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    with open('new-uid.txt') as f:
        uid_list = f.read().splitlines()

    idx = 100
    for uid in uid_list:
        result = ''.join([i for i in uid if not i.isdigit()])
        if result == "instructor":
            continue

        # Preparing SQL queries to INSERT a record into the database.
        cursor.execute(
            "insert into resources.allocation_group (uid,search_key,target_hash,image_hash, image_count, requested_date, provisioned_date) values (%s,%s,'593ddf76ff865889e897700d6162259f','3871be408f254705d934291111051405', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
            (uid, '20211012170808_' + str(idx)))
        idx += 1

    # Commit your changes in the database
    conn.commit()
    print("Records inserted........")

    # Closing the connection
    conn.close()


def insert_setting_data():
    print('Call Insert setting Data')
    # get connection instance
    conn = connect_db()
    # Setting auto commit false
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    with open('new-uid.txt') as f:
        uid_list = f.read().splitlines()

    allocation_id = select_uid_allocation()
    idx = allocation_id

    for uid in uid_list:
        result = ''.join([i for i in uid if not i.isdigit()])
        if result == "instructor":
            continue

        # Preparing SQL queries to INSERT a record into the database.
        cursor.execute(
            "insert into resources.allocation_setting (allocation_id, type_id, source_id, key_name, value) values (%s,'T','S','REGION_NAME','us-gov-west-1')",
            (idx,))

        cursor.execute(
            "insert into resources.allocation_setting (allocation_id, type_id, source_id, key_name, value) values (%s,'T','S','ACCESS_KEY','AKIAQFI4PRVSHNKGVTEG')",
            (idx,))

        cursor.execute(
            "insert into resources.allocation_setting (allocation_id, type_id, source_id, key_name, value) values (%s,'T','S','SECRET_KEY','mwPO394wc21IKg4Q89RnJuSp9tJXfytWhak6Y9yl')",
            (idx,))

        cursor.execute(
            "insert into resources.allocation_setting (allocation_id, type_id, source_id, key_name, value) values (%s,'T','S','SUBNET_ID','subnet-0ed9352c369698a18')",
            (idx,))

        cursor.execute(
            "insert into resources.allocation_setting (allocation_id, type_id, source_id, key_name, value) values (%s,'T','S','VPC_ID','vpc-076db852b5b932959')",
            (idx,))

        cursor.execute(
            "insert into resources.allocation_setting (allocation_id, type_id, source_id, key_name, value) values (%s,'T','S','ROLE_ARN','arn:aws-us-gov:iam::403709541943:role/CVLE_Administrator')",
            (idx,))

        cursor.execute(
            "insert into resources.allocation_setting (allocation_id, type_id, source_id, key_name, value) values (%s,'T','S','ROLE_SESSION_NAME','terraform')",
            (idx,))
        idx += 1

    # Commit your changes in the database
    conn.commit()
    print("Records inserted........")

    # Closing the connection
    conn.close()


def delete_setting_table():
    print('Truncate setting table')
    # get connection instance
    conn = connect_db()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a query
    cur.execute("DELETE FROM resources.allocation_setting")
    conn.commit()
    # Closing the connection
    conn.close()


def delete_group_table():
    print('Truncate group table')
    # get connection instance
    conn = connect_db()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a query
    cur.execute("DELETE FROM resources.allocation_group")
    conn.commit()
    # Closing the connection
    conn.close()


def delete_allocation_table():
    print('Truncate allocation table')
    # get connection instance
    conn = connect_db()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a query
    cur.execute("DELETE FROM resources.allocation")
    conn.commit()
    # Closing the connection
    conn.close()


def gen_uid():
    print('Generate uid Data')
    my_file = open('new-uid.txt', 'w')
    i = 1
    while i <= int(uuid_idx):
        result = uuid.uuid4()
        # print(result.hex.upper())
        my_file.write("%s\n" % result.hex.upper())
        i += 1

    i = 1
    while i <= int(instructor_ids):
        result = uuid.uuid4()
        # print(result.hex.upper())
        my_file.write("instructor" + str(i) + "\n")
        i += 1

    my_file.close()


def delete_cdm_resources():
    delete_setting_table()
    delete_allocation_table()
    delete_group_table()


def provision_cdm_resources():
    # do this first
    insert_group_data()
    # do this second but take starting ID from the above insert, now automated
    insert_uid_data()
    # do this third but copy starting ID from above insert, now automated
    insert_setting_data()


def select_uid_allocation_group():
    print('Call select_uid_allocation_group')
    # get connection instance
    conn = connect_db()

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM resources.allocation_group order by id")
    result = cursor.fetchone()

    return result[0]


def select_uid_allocation():
    print('Call select_uid_allocation')
    # get connection instance
    conn = connect_db()

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM resources.allocation order by id")
    result = cursor.fetchone()

    return result[0]


def generate_uid():
    print("gen_uid")
    gen_uid()


def provision_all():
    print("provision_all")
    gen_uid()
    delete_cdm_resources()
    provision_cdm_resources()


# Press the green arrow to run the script.
if __name__ == '__main__':
    # python3 crms-cdm-allocation.py '{"uuid_idx" : 5, "instructor_ids" : 2, "run" : "provision_all"}'
    arguments = ast.literal_eval(sys.argv[1])
    uuid_idx = arguments['uuid_idx']
    instructor_ids = arguments['instructor_ids']

    if arguments['run'] == "gen_uid":
        generate_uid()
        # gen_uid()
    elif arguments['run'] == "provision_all":
        provision_all()

