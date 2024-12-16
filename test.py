

def testreadxls():
    
    import pandas as pd
    import numpy as np
    import os
    
    # Read the data from the Excel file
    data = pd.read_excel('./utils/data.xlsx')
    # ? 只要第1列
    tele = data.iloc[:, 0]
    # ? 转换为list
    telelist = tele.tolist()
    print(telelist)
    
    # Return the data
    return data


    

if __name__ == "__main__":
    testreadxls()