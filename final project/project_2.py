import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np

df1 = pd.read_excel("data.xlsx", sheet_name = 0) #survey
df2 = pd.read_excel("data.xlsx", sheet_name = 1) #investment
#df3 = df2[df2['Customer_ID']==261909]
#idx = df3.index.tolist()
#print(idx)
#print(df1[0:3])
#print(df2[0:3])

def create_lst(df, col_name):
    lst=[]
    for elem in df[col_name]:
        if elem not in lst:
            lst.append(elem)
    return lst

def empty_to_zero(data):
    for key in list(data.keys()):
        if data[key] == []:
            data[key] = 0
        else:
            continue
    return data

def create_data1(df, col_name):
    data = {}
    for elem in create_lst(df, col_name):
        ans = dict([('A0', []),
                    ('A01', []),
                    ('A02', []),
                    ('A03', []),
                    ('A04', []),
                    ('A05', []),
                    ('A06', []),
                    ('A07', []),
                    ('A08', []),
                    ('A09', []),
                    ('A10', []),
                    ('A11', []),
                    ('A12', []),
                    ('A13', []),
                    ('A14', []),
                    ('B01', []),
                    ('B02', []),
                    ('B03', []),
                    ('B04', []),
                    ('B05', []),
                    ('B06', []),
                    ('B07', [])])
        
        elem_df = df[df[col_name]==elem]

        for index in elem_df.iterrows():
            ans_key = str(elem_df.ix[index[0], 'Question'])
            if not (ans_key=='A03' or ans_key=='A08' or ans_key=='A09' or ans_key=='B02' or ans_key=='B03'):
                ans[ans_key] = elem_df.ix[index[0], 'ANS_ORDER']
            else:
                ans[ans_key].append(elem_df.ix[index[0], 'ANS_ORDER'])
        ans['Risk_lvl'] = elem_df.ix[elem_df.index[0], 'Risk_lvl']

        total_score=0
        for i in range(1, 8):
            item = 'B0'+str(i)
            if type(ans[item])==list:
                if not ans[item]==[]:
                    total_score+=max(ans[item])
            else:
                total_score+=ans[item]
        ans['Total_score'] = total_score
        empty_to_zero(ans)
        data[elem]=ans
    return data

clean_data1 = create_data1(df1, 'Customer_ID')
#print(clean_data1[274897])

def zero_in_lst(lst):
    cnt = 1
    for elem in lst:
        if 0 in elem:
            return True
        else:
            if cnt == len(lst):
                return False
            cnt+=1
            continue

def create_data2(df, col_name):
    data = {}
    for elem in create_lst(df, col_name):
        inv = {}
        elem_df = df[df[col_name]==elem]

        for index in elem_df.iterrows():
            inv_key = str(elem_df.ix[index[0], 'Risk_lvl'])
            if inv_key not in inv:
                inv[inv_key]=[elem_df.ix[index[0], 'Amount']]
            else:
                inv[inv_key].append(elem_df.ix[index[0], 'Amount'])

        total_amt = 0
        tmp = 0
        for key in inv:
            total_amt+=sum(inv[key])
            tmp += sum(inv[key])*int(key[2])
        if total_amt == 0:
            inv['Actual_risk'] = 0
        else:
            inv['Actual_risk'] = round(tmp/total_amt, 2)
        data[elem] = inv

    return data

clean_data2 = create_data2(df2, 'Customer_ID')
print(clean_data2[1649])


def combine_data(data1, data2):
    new_data = {}
    for elem in data2.keys():
        new_data[elem] = data1[elem]
        new_data[elem]['Actual_risk'] = data2[elem]['Actual_risk']
    return new_data

all_data = combine_data(clean_data1, clean_data2)


check_lst = []
for key in all_data.keys():
    check_lst.append(len(all_data[key].keys()))
print(max(check_lst))
print(min(check_lst))
#print(all_data[1649])


def to_dataframe(data):
    new_df = dict([('Customer_ID', []),
                   ('A0', []),
                   ('A01', []),
                   ('A02', []),
                   ('A03', []),
                   ('A04', []),
                   ('A05', []),
                   ('A06', []),
                   ('A07', []),
                   ('A08', []),
                   ('A09', []),
                   ('A10', []),
                   ('A11', []),
                   ('A12', []),
                   ('A13', []),
                   ('A14', []),
                   ('B01', []),
                   ('B02', []),
                   ('B03', []),
                   ('B04', []),
                   ('B05', []),
                   ('B06', []),
                   ('B07', []),
                   ('Risk_lvl', []),
                   ('Total_score', []),
                   ('Actual_risk', [])])

    for customer_id in list(data.keys()):
        new_df['Customer_ID'].append(customer_id)

    def add_elem(ind_ans, col_name):
        new_df[col_name].append(ind_ans[col_name])
        
    for ans in list(data.values()):
        all_keys = list(new_df.keys())
        for i in range(1, len(all_keys)):
            add_elem(ans, all_keys[i])

    return pd.DataFrame(new_df)

final_data = to_dataframe(all_data)
#print(final_data.head())
        
#condition = np.logical_and(df1['Customer_ID']==261909, df1['Question']=='A0')
#print(df1[condition])

### data analysis ###
'''
final_data.plot.scatter(x='Actual_risk', y='Risk_lvl')
plt.show()
final_data.plot.scatter(x='Total_score', y='Risk_lvl')
plt.show()
final_data.plot.scatter(x='Total_score', y='Actual_risk')
plt.show()
'''
#final_data.plot.scatter(x='A01', y='Actual_risk')
#plt.show()

condition = np.logical_and(final_data['A11']==0, final_data['A12']==0)
wrong_data = final_data[condition]

'''
拿掉錯誤登記資料
'''
for row in wrong_data.iterrows():
    final_data.drop(index=row[0], inplace=True)

#final_data.drop(index=[1064, 1086])
#print(final_data.head())

Actual_lvl = []
for elem in final_data['Actual_risk']:
    Actual_lvl.append(int(round(elem)))

final_data['Actual_lvl']=Actual_lvl

color = {
    5:'r',
    4:'g',
    3:'b',
    2:'black',
    1:'gray',
    0:'white'
    }

final_data['color'] = final_data['Actual_lvl'].map(color)

def all_b(data):
    new_data = data[['B01', 'B04', 'B05', 'B06', 'B07', 'Actual_risk', 'Actual_lvl']]
    new_b02_lst = []
    new_b03_lst = []
    for elem in data['B02']:
        new_b02_lst.append(max(elem))
    for elem in data['B03']:
        new_b03_lst.append(max(elem))
    new_data['B02'] = new_b02_lst
    new_data['B03'] = new_b03_lst
    return new_data

chosen_df_a = final_data[['A01', 'A02', 'A04', 'A05', 'A10', 'A11', 'A12', 'A13', 'A14']]
chosen_df_b = final_data[['B01', 'B04', 'B05', 'B06', 'B07']]
chosen_df_all = final_data[['A01', 'A02', 'A04', 'A05', 'A10', 'A11', 'A12', 'A13', 'A14','B01', 'B04', 'B05', 'B06', 'B07', 'Actual_risk', 'Actual_lvl']]

all_b_data = all_b(final_data)
print(all_b_data.head())
### Correlation matrix ###
#plt.matshow(chosen_df_b.corr())
#chosen_df_b.corr()

#all_b_data.to_csv('All_b.csv')
#df_a = final_data[['Customer_ID', 'A01', 'A02', 'A04', 'A05', 'A10', 'A11', 'A12', 'A13', 'A14', 'Actual_risk', 'Actual_lvl']]

condition = np.logical_and(final_data['B07']==4, final_data['Actual_lvl']==3)
print(final_data[condition])
