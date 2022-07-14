import pandas as pd 
import os
results = pd.DataFrame()
if __name__ == "__main__":
    for filename in os.listdir():
        if "reactive" in filename:
            df = pd.read_csv(filename, sep='\t',  index_col=1)

            df = df[df["Hierarchy Level"] == 1]

            df = df.drop(["Hierarchy Level"], axis=1)
            df.rename(columns = {'Metric Value':filename}, inplace = True)
            df = df.transpose()
            if results.empty:
                results = df
            else:
                results = results.append(df)

    results.to_csv("results.csv")