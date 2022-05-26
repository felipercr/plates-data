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



def main():
    df = file_to_df('Placa_pvc_3,0_4')
    calcs(df)


if __name__ == '__main__':
    main()