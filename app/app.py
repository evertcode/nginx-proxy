import psycopg2
import json
import time
import io

from psycopg2 import OperationalError


def get_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            user="demo",
            password="postgres1234#",
            host="postgres",
            port="5432",
            dbname="postgres"
        )
    except OperationalError as e:
        print(f"Error: {e}")
    return connection

def insert_log(connection, log):
    cursor = connection.cursor()

    sql = """
        INSERT INTO logs (
            time_local,
            client,
            method,
            request,
            request_length,
            status,
            bytes_sent,
            body_bytes_sent,
            referer,
            user_agent,
            upstream_addr,
            request_time,
            upstream_response_time,
            upstream_connect_time
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, log)
    connection.commit()

def get_last_position():
    position = 0
    try:
        with open("/app/config/last_position.txt", "r") as file:
            position = int(file.read())
    except FileNotFoundError:
        pass
    return position

def save_last_position(position):
    with open("/app/config/last_position.txt", "w") as file:
        file.write(str(position))

def main():
    connection = get_connection()
    if connection is None:
        return

    while True:
        try:
            with open("/app/logs/access.log", "r+") as file:
                print("Reading logs...")
                position = get_last_position()
                print(f"Last position: {position}")

                file.seek(position)

                logs = file.readlines()

                print(f"Logs: {logs}")

                for log in logs:
                    json_log = json.loads(log)

                    data = (
                        json_log["time_local"],
                        json_log["client"],
                        json_log["method"],
                        json_log["request"],
                        json_log["request_length"],
                        json_log["status"],
                        json_log["bytes_sent"],
                        json_log["body_bytes_sent"],
                        json_log["referer"],
                        json_log["user_agent"],
                        json_log["upstream_addr"],
                        json_log["request_time"],
                        json_log["upstream_response_time"],
                        json_log["upstream_connect_time"]
                    )

                    insert_log(connection, data)

                    position += len(log)
                    save_last_position(position)
        except (json.JSONDecodeError, io.UnsupportedOperation) as e:
            print(f"Error: {e}")

        time.sleep(5)

    connection.close()

if __name__ == "__main__":
    main()
