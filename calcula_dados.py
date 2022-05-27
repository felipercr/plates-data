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
    #Vazão(Kg/s)
    flw_rt_mean = df['Vaz[kg/s]'].mean()

    #Dp(mbar)
    dp_mean = df['DP'].mean()

    #Desvio Padrão
    dp_std = df['DP'].std()

    #V(m/s)
    v = flw_rt_mean / (area() * df['ro ST [kg/m3]'].mean())

    #Re
    re = (df['ro ST [kg/m3]'].mean() * v * dh()) / (df['Visc *10000'].mean() / 1000)

    results = np.array([v, flw_rt_mean, re, dp_mean, dp_std])
    return results


def main():
    plt = 1
    res = 1
    result_plt = np.empty([0,5])

    while os.path.exists(f'placa_{plt}/res_{res}'):

        while os.path.exists(f'placa_{plt}/res_{res}'):

            df = file_to_df(f'placa_{plt}/res_{res}')
            result_plt = np.vstack((result_plt, calcs(df)))
            res += 1

        result_df = pd.DataFrame(
            result_plt,
            columns = [
                'V(m/s)', 'Vaz.(kg/s)', 'Re',
                'Dp(mbar)', 'Desv.Pad.'
            ]
        )

        if os.path.exists(f'placa_{plt}/resultados_{plt}.xlsx'): 
            os.remove(f'placa_{plt}/resultados_{plt}.xlsx')
        result_df.to_excel(f'placa_{plt}/resultados_{plt}.xlsx')

        plt += 1 

        result_plt = np.empty([0,5])
        res = 1

if __name__ == '__main__':
    main()

