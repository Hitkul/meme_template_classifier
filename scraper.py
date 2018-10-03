from __future__ import division
from bs4 import BeautifulSoup
import requests
import shutil
import os.path
import csv

meme_template_path = 'memes'
caption_path = 'captions'
n_captions = 3   #this number *15 is the total number of captions per template
n_templates = 2  #this number *15 is the total number of templates

def get_meme_templates(n_templates):
    links = []
    imgs=[]
    for i in range(1,n_templates):
        print("scraping meme template page number = ",i)
        if i == 1:
            url = 'https://memegenerator.net/memes/popular/alltime'
        else:
            url = 'https://memegenerator.net/memes/popular/alltime/page/' + str(i)

        r = requests.get(url)
        soup = BeautifulSoup(r.text,'html.parser')
        chars = soup.find_all(class_='char-img')
        for char in chars:
            links.append(char.find('a')['href'])
            imgs.append(char.find('img')['src'])
        return links,imgs
    
def download_image_from_url(url):
    response = requests.get(url, stream=True)
    name_of_file = url.split('/')[-1]
    complete_name = os.path.join(meme_template_path, name_of_file)
    with open(complete_name,'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def get_title_and_description(link):
    url = 'https://memegenerator.net'+link
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    title_div = soup.find_all(class_="section-title section-title-hide-mb")
    title = title_div[0].find('h1').text
    description_div =soup.find_all(class_ = 'details-text only-above-1100')
    try:
        description = description_div[0].text 
    except:
        description = None
    return title,description

def dump_list_into_csv(tuple_list):
    with open('title_description.csv','w') as in_file:
        file_writer = csv.writer(in_file)
        file_writer.writerow(('title','description'))
        for row in tuple_list:
            file_writer.writerow(row)

def get_captions(link):
    captions = []
    for k in range(1,n_captions):
        print("scraping caption page number = ",k)
        if k == 1:
            url = 'https://memegenerator.net' + link
        else:
            url = 'https://memegenerator.net' + link + '/images/popular/alltime/page/' + str(k)
        
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'html.parser')
        caption_div = soup.find_all(class_ = "optimized-instance-container img")
        del caption_div[::2]
        for div_i in caption_div:
            temp =  ""
            temp+= div_i.find(class_="optimized-instance-text0").text
            temp+=" "
            temp+= div_i.find(class_="optimized-instance-text1").text
            captions.append(temp)
    return captions

def dump_captions_to_file(link):
    captions = get_captions(link)
    with open(caption_path+link+'.txt','w') as out_file:
        for caption in captions:
            out_file.write("%s\n" % caption)

template_links, template_imgs = get_meme_templates(n_templates)

# title_description_zip = [ get_title_and_description(link) for link in template_links] 

# dump_list_into_csv(title_description_zip)

dump_captions_to_file(template_links[0])
# 


# print("downlaoding images now....")
# for url in template_imgs:
#     download_image_from_url(url)
    



# ======================================================

# for i in range(1,n_templates):
#     if i == 1:
#         url = 'https://memegenerator.net/memes/popular/alltime'
#     else:
#         url = 'https://memegenerator.net/memes/popular/alltime/page/' + str(i)

#     r = requests.get(url)
#     soup = BeautifulSoup(r.text,'html.parser')
#     chars = soup.find_all(class_='char-img')
#     links = [char.find('a') for char in chars]
#     imgs = [char.find('img') for char in chars]
#     assert len(links) == len(imgs)
#     for j,img in enumerate(imgs):
#         img_url = img['src']
#         response = requests.get(img_url, stream=True)
#         name_of_file = img_url.split('/')[-1]
#         completeName = os.path.join(save_path, name_of_file)
#         with open(completeName,'wb') as out_file:
#             shutil.copyfileobj(response.raw, out_file)
#         del response

#         for k in range(1,n_captions):
#             if k == 1:
#                 URL = 'https://memegenerator.net' + links[j]['href']
#             else:
#                 URL = 'https://memegenerator.net' + links[j]['href'] + '/images/popular/alltime/page/' + str(k)

#             R = requests.get(URL)
#             SOUP = BeautifulSoup(R.text,'html.parser')
#             CHARS = SOUP.find_all(class_='char-img')
#             IMGS = [char.find('img') for char in CHARS]
#             with open('Captions.txt', 'a') as f:
#                 for IMG in IMGS:
#                     try:
#                         print(IMG)
#                         f.write('%s\n' % (IMG['alt']))
#                     except UnicodeEncodeError:
#                         Uerrors += 1
#                         pass
#     if i % 10 == 0:
#         print('<'+'='*10+'>')
#         print(i)
#         print(Uerrors)



# URL = 'https://memegenerator.net' + links[0]['href']
# R = requests.get(URL)
# SOUP = BeautifulSoup(R.text,'html.parser')
# CHARS = SOUP.find_all(class_='char-img')
# IMGS = [char.find('img') for char in CHARS]
# print(IMGS[1]['alt'])


# img_url = imgs[0]['src']
# response = requests.get(img_url, stream=True)
# name_of_file = img_url.split('/')[-1]
# completeName = os.path.join(save_path, name_of_file)
# with open(completeName,'wb') as out_file:
#     shutil.copyfileobj(response.raw, out_file)
# del response



