from modules.thread import statistics, calculate_rate, gen_test
from config import database
CONN = database.connect_db()


def main():
    cursor = CONN.cursor()
    # Step 1
    # statistics.run(cursor)

    # Step 2
    # calculate_rate.run(cursor)

    # Step 3
    gen_test.run()


if __name__ == "__main__":
    main()
