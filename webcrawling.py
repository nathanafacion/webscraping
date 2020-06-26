# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 16:22:50 2020

@author: nathana
"""

import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from dateutil import parser

def web_scraping(category):
    site = "https://garotanocontrole.com.br/category/"+ category
    res = requests.get(site)
    res.encoding = res.apparent_encoding 
    soup = BeautifulSoup(res.text,'html.parser')
    posts = soup.find_all(class_="post")
    all_posts = []
    for post in posts:
        url = post.a['href']
        title = post.a['title']
        date = parser.parse(post.find(class_="entry-date")['datetime'])
        all_posts.append({
          'url':url,
          'title': title,
          'date': str(date.day) + "/" + str(date.month) + "/" + str(date.year)
        })
    
    create_table(category,all_posts)
    
    return all_posts, len(posts)
  
def save_json(category, all_posts):
    name =  category + '.json'
    with open( name,'w') as json_file:
        json.dump(all_posts, json_file)
        
        
def create_plot(categories, categories_size):
    y_pos = np.arange(len(categories))
    plt.bar(y_pos, categories_size, align='center', alpha=0.5)
    plt.xticks(y_pos, categories)
    plt.ylabel('Quantidade de posts')
    plt.title('Categorias')
    plt.savefig('grafico.png')

def create_table(category, all_posts):
    print('\n' + category.upper())
    print(tabulate(all_posts,tablefmt="grid"))

def main():
    categories = ["analise","promocao","curiosidade","entrevista","lista"]
    categories_size = []

    for category in categories:
        posts, size = web_scraping(category)
        categories_size.append(size)
        save_json(category,posts)
        
    create_plot(categories,categories_size)


main()
