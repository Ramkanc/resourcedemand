import pandas as pd
import os

Mgr_BCS_1 = r"\BCS_Mgr1.csv"
Mgr_BCS_2 = r"\BCS_Mgr2.csv"
Mgr_BCS_3 = r"\BCS_Mgr3.csv"
Mgr_FCS_1 = r"\FCS_Mgr1.csv"
Mgr_FCS_2 = r"\FCS_Mgr2.csv"
Mgr_FCS_3 = r"\FCS_Mgr3.csv"
Mgr_MCS_1 = r"\MCS_Mgr1.csv"
Mgr_MCS_2 = r"\MCS_Mgr2.csv"
Mgr_MCS_3 = r"\MCS_Mgr3.csv"
Mgr_EngSv_1 = r"\EngSv_Mgr1.csv"

df_prgms = r".\Prg_rd.csv"

val_streams = {"FCS" :["Mgr_FCS_1","Mgr_FCS_2","Mgr_FCS_3"],"BCS" : ["Mgr_BCS_1","Mgr_BCS_2","Mgr_BCS_3"],"MCS" : ["Mgr_MCS_1","Mgr_MCS_2","Mgr_MCS_3"],"EngServices": ["Mgr_EngSv_1"]}
val_streams_mgrs = [x for (k,v) in val_streams.items() for x in v]
#print(f"Value streams: {val_streams_mgrs}")

def get_mgr (mgr):    
    file_name  = f"{mgr}.csv"
    full_path = os.path.join(os.getcwd(), file_name)       
    df = pd.read_csv(full_path)
    return df

def get_whole_vls():
    df = pd.DataFrame()
    for mgr in val_streams_mgrs:
        df = pd.concat([df, get_mgr(mgr)], ignore_index=True)
    return df

def get_single_vls(vls):
    df = pd.DataFrame()
    for mgr in val_streams[vls]:
        df = pd.concat([df, get_mgr(mgr)], ignore_index=True)
    return df
    

def get_prog_of_vsl(vls):
    df = pd.read_csv(df_prgms)
    prog = df[df['Value Stream'] == vls]['Program name'].to_list()
    return prog

def set_mgr(mgr, my_dict):
    file_name  = f"{mgr}.csv"
    full_path = os.path.join(os.getcwd(), file_name) 
    df = pd.read_csv(full_path)
    strt = my_dict["stt_wk"]
    endt = strt + my_dict["end_wk"]+1
    eng_name = my_dict["name"]
    prog_name = my_dict["program"]
    row_ind = df[df["EngNames"]==eng_name].index    
    df.iloc[row_ind[0], strt:endt] = [prog_name]* (endt-strt)
    df.to_csv(full_path, index=False)    
    return df


def get_plot_df(df_i):
    df_p = df_i.iloc[:, 2:]
    df_p_t = df_p.T
    df_p_t = df_p_t.apply(pd.Series.value_counts, axis=1).fillna(0).astype(int)
    df_p_t = df_p_t.drop(columns=['NoProgram'], errors='ignore')
    return df_p_t

