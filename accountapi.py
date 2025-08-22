import psycopg2

# Connection helper function
def get_connection():
    return psycopg2.connect(
        host="localhost",
        user="postgres",       # 🔁 replace with your PostgreSQL username
        password="Yash_4903@",  # 🔁 replace with your PostgreSQL password
        database="account"     # 🔁 replace with your DB name
    )


def user_exists(user_id):
    print("Existence tool called")
    user_id = int(user_id)
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM acc WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return bool(result)


def authenticate_user(user_id, password):
    print("Authenticater called")
    user_id = int(user_id)

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM acc WHERE user_id = %s AND password = %s"
    cursor.execute(query, (user_id, password))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return "The user is an authenticated one"
    else:
        return "The credentials are not valid..."


def get_balance(user_id):
    print("Balance checker called")
    user_id = int(user_id)
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT balance FROM acc WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return f"Balance is : {result[0]}"
    else:
        return "User not found"


def transfer_money(from_user, to_user, amount):
    from_user = int(from_user)
    to_user = int(to_user)
    amount = int(amount)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM acc WHERE user_id = %s", (from_user,))
    from_result = cursor.fetchone()

    cursor.execute("SELECT balance FROM acc WHERE user_id = %s", (to_user,))
    to_result = cursor.fetchone()

    if from_result and to_result:
        from_balance = from_result[0]

        if from_balance >= amount:
            # Deduct from sender
            cursor.execute("UPDATE acc SET balance = balance - %s WHERE user_id = %s", (amount, from_user))
            # Add to receiver
            cursor.execute("UPDATE acc SET balance = balance + %s WHERE user_id = %s", (amount, to_user))

            conn.commit()
            cursor.close()
            conn.close()
            return "Transfer successful"
        else:
            cursor.close()
            conn.close()
            return "Insufficient balance"
    else:
        cursor.close()
        conn.close()
        return "One or both users not found"


def create_account(user_name):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = "INSERT INTO acc (user_name, balance) VALUES (%s, %s) RETURNING user_id"
    cursor.execute(insert_query, (user_name, 0))
    
    account_number = cursor.fetchone()[0]
    conn.commit()

    cursor.close()
    conn.close()

    return f"Account created successfully. Account number is {account_number}"


def delete_account(account_number):
    account_number = int(account_number)
    conn = get_connection()
    cursor = conn.cursor()

    delete_query = "DELETE FROM acc WHERE user_id = %s"
    cursor.execute(delete_query, (account_number,))
    
    conn.commit()

    if cursor.rowcount == 0:
        result = f"No account found with account number {account_number}"
    else:
        result = f"Account {account_number} deleted successfully."

    cursor.close()
    conn.close()

    return result
