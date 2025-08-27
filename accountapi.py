import psycopg2

# Connection helper function
def get_connection():
    return psycopg2.connect(
        host="localhost",
        user="postgres",       # 🔁 replace with your PostgreSQL username
        password="Yash_4903@",  # 🔁 replace with your PostgreSQL password
        database="account"     # 🔁 replace with your DB name
    )


def user_exists(username):
    print("Existence tool called")
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM acc WHERE user_name = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return bool(result)


def authenticate_user(username, password):
    print("Authenticater called")
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM acc WHERE user_name = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return "The user is an authenticated one"
    else:
        return "The credentials are not valid..."


def get_balance(username):
    print("Balance checker called")
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT balance FROM acc WHERE user_name = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return f"Balance is : {result[0]}"
    else:
        return "User not found"


def transfer_money(from_username, to_username, amount):
    amount = int(amount)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM acc WHERE user_name = %s", (from_username,))
    from_result = cursor.fetchone()

    cursor.execute("SELECT balance FROM acc WHERE user_name = %s", (to_username,))
    to_result = cursor.fetchone()

    if from_result and to_result:
        from_balance = from_result[0]

        if from_balance >= amount:
            # Deduct from sender
            cursor.execute("UPDATE acc SET balance = balance - %s WHERE user_name = %s", (amount, from_username))
            # Add to receiver
            cursor.execute("UPDATE acc SET balance = balance + %s WHERE user_name = %s", (amount, to_username))

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


def create_account(user_name, password):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if username already exists
    cursor.execute("SELECT user_id FROM acc WHERE user_name = %s", (user_name,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return "Error: Username already exists. Please choose a different username"

    insert_query = "INSERT INTO acc (user_name, password) VALUES (%s, %s) RETURNING user_id"
    cursor.execute(insert_query, (user_name, password))
    
    account_number = cursor.fetchone()[0]
    conn.commit()

    cursor.close()
    conn.close()

    return f"Account created successfully. Account number is {account_number}. Initial balance is set to 500."


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
