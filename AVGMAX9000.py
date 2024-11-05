import pandas as pd
import numpy as np
import os
os.chdir(os.getcwd())

#FILE HOOD
repo1=[]
hit_list=[]
excluded_cases=[]

for file in os.listdir():
    if file.endswith(".csv"):
        print(file)
        df=pd.read_csv(file, sep='delimiter', encoding='latin1',engine='python')
        rows,columns=df.shape
        file_name=file.rstrip(".csv")

        #ROWS HOOD
        repo2=[]
        for r in range(rows):
            ll=list(df.iloc[r,:])[0].rstrip(",")
            if 'Elements' in ll: #looking for the interested row
                df_main=pd.read_csv(file,skiprows=r+1, encoding='latin1',engine='python')
                df_main.dropna(axis=1, inplace=True)
                print(df_main.shape)
                #df_main=df_main[~df_main['Loadcase'].isin(excluded_cases)] #excluding desired cases
                df_main=df_main.query('Loadcase not in @excluded_cases')
                print(df_main.shape)
                elements=df_main['Elements'].unique()
                  
                #ELEMENTS HOOD
                for el in elements:
                    df_filter=df_main[df_main['Elements']==el] #filtering the element
                    df_sorted=df_filter.sort_values(by='Mag',ascending=False) #sorting max load
                    max_load=df_sorted['Mag'].iloc[0] #getting max load
                    lcid=df_sorted['Loadcase'].iloc[0] #getting corresponding lcid
                    
                    repo2.append((el,lcid,max_load)) #all elements and their max load storage
                    hit_list.append((el,lcid,max_load)) #all elements hit list

        df_repo2=pd.DataFrame(repo2,columns=['ELID','LCID','MAX_LOAD'])
        value_counts=list(df_repo2['LCID'].value_counts().items())[0] 
        lcid,count=value_counts[0],value_counts[1] #file hit list
        repo1.append((file,lcid,np.mean(df_repo2['MAX_LOAD']),np.std(df_repo2['MAX_LOAD']))) #file level and avg max load storage

#main file output
df_repo1=pd.DataFrame(repo1,columns=['FILE','LCID','AVGMAX_LOAD','STD'])
df_repo1.to_excel(f"AVGMAX9000.xlsx",index=False)

#load hist plot
df_repo1['AVGMAX_LOAD']=df_repo1['AVGMAX_LOAD']/1e3 #kN conversion
fig=df_repo1['AVGMAX_LOAD'].hist(bins=100).get_figure()
fig.savefig("AVGMAX_histplot.png")

#lcid hit plot
df_hit=pd.DataFrame(hit_list,columns=["ELID","LCID","MAX_LOAD"])
fig=df_hit["LCID"].value_counts().plot(kind="barh").get_figure()
fig.savefig("AVGMAX_barplot.png")

print("DONE")