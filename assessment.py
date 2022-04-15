import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import date
from tabulate import tabulate
import mysql.connector


con = mysql.connector.connect(host="localhost",user="root",password="Newme@2022",database="demo")

mycur = con.cursor()

url = "https://en.wikipedia.org/wiki/List_of_prime_ministers_of_India"

source = requests.get(url)

soup = BeautifulSoup(source.text,'html.parser')

table = soup.find('table',class_="wikitable")

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('expand_frame_repr', True)

pd.options.display.max_columns = None
pd.options.display.max_rows = None

df = pd.read_html(str(table))

df = df[0]

cols = (df.columns.to_list())

df = df[[cols[2],cols[4],cols[5],cols[10]]]

colms = ["Name","Took office","Left office","Party"]

df.columns = colms

# removing the unwanted special characters in dataframe
rep_str = ['†','[RES]','[NC]','[§]','(Secular)','(National Front)','(United Front)','(Rashtriya)','(I)','(NDA)','(UPA)']

def ch_replace(x):
  global rep_str
  rep_char = rep_str
  for g in rep_char:
    if g in x:
      out = x.replace(g,"")
      return out
  return x

df = df.applymap(ch_replace)

today = date.today()
current_date = today.strftime('%d %B %Y')

fil = df['Left office'] == "Incumbent"
df.loc[fil,'Left office'] = current_date

df['Name'] = df['Name'].str.strip()
df['Took office'] = df['Took office'].str.strip()
df['Left office'] = df['Left office'].str.strip()
df['Party'] = df['Party'].str.strip()

df = df.astype('string')

data = df.to_dict()

names = data['Name'].values()
party = data['Party'].values()
took_office = data['Took office'].values()
left_office = data['Left office'].values()

insert_date = zip(names,party,took_office,left_office)


# for a,b,c,d in zip(names,party,took_office,left_office):
#     print(a,b,c,d,sep="|")

def create_table():
    query = """create table if not exists Indianprimeminister(
			Name varchar(50),
            Party varchar(50),
            `Took office` varchar(30),
            `Left office` varchar(30)       
);
    """
    mycur.execute(query)


def insert_data():
    for a,b,c,d in zip(names,party,took_office,left_office):
            query = "insert into indianprimeminister values(%s,%s,%s,%s)"
            cols = [a,b,c,d]
            mycur.execute(query,cols)
            con.commit()

# def retrive_data():
#     query = "select * from indianprimeminister"
#     mycur.execute(query)
#     result = mycur.fetchall()
#     out = tabulate(result,headers=colms)
#     return out
        
def clean_up():
  query = "drop table if exists indianprimeminister;"
  mycur.execute(query)
  con.commit()
  print("clean up completed")




def query_1():
  query = r"""
              with time_spent_off as
              (SELECT 
                  *,
                  STR_TO_DATE(`took office`, '%e %M %Y') nf_took_off,
                  STR_TO_DATE(`left office`, '%e %M %Y') nf_left_off,
                  DATEDIFF(STR_TO_DATE(`left office`, '%e %M %Y'),STR_TO_DATE(`took office`, '%e %M %Y')) as days_at_off
              FROM
                  indianprimeminister)
              SELECT 
                  name, SUM(days_at_off) total_day_at_off
              FROM
                  time_spent_off
              GROUP BY name
              ORDER BY total_day_at_off DESC;"""
  mycur.execute(query)
  result = mycur.fetchall()
  out = tabulate(result,headers=['Name','total days at office'])
  return out


def query_2():
  query = r"""
              SELECT 
                  name, COUNT(*) times_as_PM
              FROM
                  indianprimeminister
              GROUP BY name
              ORDER BY times_as_PM DESC;"""
  mycur.execute(query)
  result = mycur.fetchall()
  out = tabulate(result,headers=['Name','times as PM'])
  return out

def query_3():
  query = r"""
              select * from 
              (select *,dense_rank() over(order by total_time_at_off desc) as d_rank from 
              (with time_spent_off as
              (SELECT 
                  *,
                  STR_TO_DATE(`took office`, '%e %M %Y') nf_took_off,
                  STR_TO_DATE(`left office`, '%e %M %Y') nf_left_off,
                  DATEDIFF(STR_TO_DATE(`left office`, '%e %M %Y'),STR_TO_DATE(`took office`, '%e %M %Y')) as days_at_off
              FROM
                  indianprimeminister)
              SELECT 
                  name, SUM(days_at_off) total_time_at_off
              FROM
                  time_spent_off group by name) as pm_at_off) as main_table where d_rank=3;"""
  mycur.execute(query)
  result = mycur.fetchall()
  out = tabulate(result,headers=['Name','total days at office','rank'])
  return out

if __name__=="__main__":
  clean_up()
  create_table()
  insert_data()
  print("x-"*30) 
  print(query_1())
  print("x-"*30)
  print(query_2())
  print("x-"*30)
  print(query_3())
