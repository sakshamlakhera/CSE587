import numpy as np
import pandas as pd

class MCDMManager:
    def __init__(self):
        self.default_method = self.run_topsis

    def run_topsis(self, df, weights=None, impacts=None):
        if weights is None:
            weights = np.ones(df.shape[1])
        if impacts is None:
            impacts = ['+'] * df.shape[1]

        # Normalizing the DataFrame
        norm_df = df / np.sqrt((df**2).sum())

        # Weighted normalized decision matrix
        weighted_df = norm_df * weights

        # Separating the positive and negative ideal solutions
        ideal_positive = []
        ideal_negative = []

        for i in range(len(impacts)):
            if impacts[i] == '+':
                ideal_positive.append(weighted_df.iloc[:, i].max())
                ideal_negative.append(weighted_df.iloc[:, i].min())
            else:
                ideal_positive.append(weighted_df.iloc[:, i].min())
                ideal_negative.append(weighted_df.iloc[:, i].max())

        ideal_positive = np.array(ideal_positive)
        ideal_negative = np.array(ideal_negative)

        # Calculating the distances
        distances_positive = np.sqrt(((weighted_df - ideal_positive) ** 2).sum(axis=1))
        distances_negative = np.sqrt(((weighted_df - ideal_negative) ** 2).sum(axis=1))

        # Calculating the performance score
        scores = distances_negative / (distances_positive + distances_negative)

        df['TOPSIS_Score'] = scores
        df['Rank'] = df['TOPSIS_Score'].rank(ascending=False)

        return df.sort_values(by='Rank')

    def run_weighted_sum(self, df, weights=None):
        if weights is None:
            weights = np.ones(df.shape[1])

        # Multiply each column by its corresponding weight
        weighted_matrix = df * weights

        # Calculate total score
        df['Weighted_Sum_Score'] = weighted_matrix.sum(axis=1)
        df['Rank'] = df['Weighted_Sum_Score'].rank(ascending=False)

        return df.sort_values(by='Rank')

    def run(self, df, method=None, weights=None, impacts=None):
        if method is None:
            method = self.default_method
            
        return method(df, weights, impacts)