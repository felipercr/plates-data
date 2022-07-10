import os
import pandas as pd
import numpy as np

#Constants
def area(): return 0.005806
def g():    return 9.783816
def dh():   return 0.0762  

def file_to_df(file):

    data = np.loadtxt(file)
    df = pd.DataFrame(
        data,
        columns = [
            't (s) não corrigido', 'Vaz[kg/s]', 'u',
            'Vaz [l/min]', 'u', 'P0 [bar]',
            'u', 'T ST [C]', 'u',
            'ro ST [kg/m3]', 'u', 'Visc *10000',
            'u', 'T PO', 'u',
            'ro PO', 'u', 'Visc PO *10000',
            'u', 'Re ST', 'u',
            'Tomadas', 'Transmissor', 'DP',
            'u DP'
        ]
    )

    return df

def calcs(df):
    #Flow rate(Kg/s)
    flw_rt_mean = df['Vaz[kg/s]'].mean()

    #Dp(mbar)
    dp_mean = df['DP'].mean()

    #Standard deviation
    dp_std = df['DP'].std()

    #V(m/s)
    v = flw_rt_mean / (area() * df['ro ST [kg/m3]'].mean())

    #Re
    re = (df['ro ST [kg/m3]'].mean() * v * dh()) / (df['Visc *10000'].mean() / 10000)

    results = np.array([v, flw_rt_mean, re, dp_mean, dp_std])
    return results


def main():
    res = 1
    result_plt = np.empty([0,5])
    df_index = []
    all_results = []

    for plt in range(200):

        if os.path.exists(f'placa_{plt}/res_{res}'):

            while os.path.exists(f'placa_{plt}/res_{res}'):

                df = file_to_df(f'placa_{plt}/res_{res}')
                result_plt = np.vstack((result_plt, calcs(df)))
                if res == 1: df_index.append(f'Placa_{plt} {res}')
                else:        df_index.append(f'{res}')
                res += 1

            result_df = pd.DataFrame(
                result_plt,
                columns = [
                    'V(m/s)', 'Vaz.(kg/s)', 'Re',
                    'Dp(mbar)', 'Desv.Pad.'
                ],
                index = df_index
            )

            all_results.append(result_df)

            result_plt = np.empty([0,5])
            df_index = []
            res = 1

    all_results = pd.concat(all_results)

    if os.path.exists(f'resultados.xlsx'): 
        os.remove(f'resultados.xlsx')
    all_results.to_excel(f'resultados.xlsx')

if __name__ == '__main__':
    main()

