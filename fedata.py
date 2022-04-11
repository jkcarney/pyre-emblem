import pandas as pd
import numpy as np
import sqlite3


class FEData:
    def __init__(self, data_name):
        self.conn = sqlite3.connect(f'data/{data_name}.db')

        c = self.conn.cursor()
        c.execute('''CREATE TABLE FEstats (
                    game_number integer,
                    victory_rank text,
                    survival_rank text,
                    tactic_rank text,
                    overall_rank text,
                    units text
                    )''')
        self.conn.commit()
        c.close()
        self.data_name = data_name

    def add_entry(self, game_num, victory_rank, survival_rank, tactic_rank, overall_rank, unit_names: list):
        unit_entry = '-'.join(unit_names)
        c = self.conn.cursor()
        c.execute('INSERT INTO FEstats VALUES (?, ?, ?, ?, ?, ?)',
                  (game_num, victory_rank, survival_rank, tactic_rank, overall_rank, unit_entry))
        self.conn.commit()
        c.close()


def sqlite_data_to_csv(run_name):
    conn = sqlite3.connect(f'data/{run_name}.db')
    db_df = pd.read_sql_query("SELECT * FROM FEstats", conn)
    db_df.to_csv(f'data/{run_name}.csv', index=False)
