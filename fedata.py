import pandas as pd
import numpy as np


class FEData:
    def __init__(self, data_name):
        self.data_frame = pd.DataFrame(columns=['game_number',
                                                'victory_rank',
                                                'survival_rank',
                                                'tactic_rank',
                                                'overall_rank',
                                                'units'])
        self.data_name = data_name

    def add_entry(self, game_num, victory_rank, survival_rank, tactic_rank, overall_rank, unit_names: list):
        unit_entry = '-'.join(unit_names)
        pddict = {'game_number': [game_num],
                  'victory_rank': [victory_rank],
                  'survival_rank': [survival_rank],
                  'tactic_rank': [tactic_rank],
                  'overall_rank': [overall_rank],
                  'units': [unit_entry]
                  }
        df = pd.DataFrame(pddict)
        self.data_frame = pd.concat([self.data_frame, df], ignore_index=True, axis=0)
        self.save()

    def save(self):
        self.data_frame.to_csv(f'data/{self.data_name}.csv')
