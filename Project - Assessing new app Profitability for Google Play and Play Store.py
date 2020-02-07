#!/usr/bin/env python
# coding: utf-8

# #          Apple Store and Google Play

# # Introduction
# This project analyses _IOS_ and _Android_ apps related variables from a public data base in order to rank the characteristics that can increase free apps **profitability** in both markets.
# 
# We already know that the number of users have great influence in free apps profitability. This work intends to figure out what characteristics attract users and are more likely to make a free app profitable for both markets.
# 
# The Data Sets are [Google Play](https://www.kaggle.com/lava18/google-play-store-apps/home) and [IOS](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps/home) apps. The Columns are app related variables and are organized in the following order:
# 
# Google Play Data Set:
# 
# 
# | App   | Category       | Rating | Reviews | Size | Installs | Type | Price | Content Rating | Genres       | Last Updated    | Current Ver | Android Ver  |
# |------------------------------------------------|----------------|--------|---------|------|----------|------|-------|----------------|--------------|-----------------|-------------|--------------|
# | Photo Editor & Candy Camera & Grid & ScrapBook | ART_AND_DESIGN | 4.1    | 159     | 19M  | 10,000+  | Free | 0     | Everyone       | Art & Design | January 7, 2018 | 1.0.0       | 4.0.3 and up |
# 
# Apple Store Data Set:
# 
# 
# |     id    |    track_name   | size_bytes | currency | price | rating_counter_tot | rating_counter_ver | user_rating | user_rating_ver |  ver  | cont_rating | prime_genre | sup_devices.num | ipadSc_urls.num | lang.num | vpp_lic |
# |:---------:|:---------------:|:----------:|:--------:|:-----:|:------------------:|:------------------:|:-----------:|:---------------:|:-----:|:-----------:|:-----------:|:---------------:|:---------------:|:--------:|:-------:|
# | 281656475 | PAC-MAN Premium |  100788224 |    USD   |  3.99 |        21292       |         26         |      4      |       4.5       | 6.3.5 |      4+     |    Games    |        38       |        5        |    10    |    1    |
# 
# 

# ## 1. Exploring Apple Store and Google Play Data sets.

# 
# In this section I will explore the Apple Store and Google Play data sets by doing the following steps:
# 
#    1. Opening the csv files;
#    2. Using the `explore_data()` function to print few rows;
#    3. Print the column names to gain insight for future analysis.

# ## 1.1. Opening the csv files

# In[1]:


opened_data_ios = open('AppleStore.csv',encoding='utf8')
opened_data_andr = open('googleplaystore.csv',encoding='utf8')
from csv import reader
read_ios = reader(opened_data_ios)
read_andr = reader(opened_data_andr)
ios_data = list(read_ios)
andr_data = list(read_andr)
ios_data = ios_data[1:]
andr_data = andr_data[1:]


# ## 1.2 Defining `explore_data()` and exploring the data sets

# In[2]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))
        
explore_data(ios_data,0,3,True)
explore_data(andr_data,0,3,True)


# ## 2. Cleaning Data

# In this section, I'm going to remove the data that are not useful for my objectives such as **non free apps**, **repeated apps** or **apps with missing information** and, finally, apps which are not in **English**.

# ## 2.1 Removing row with error in Google Play Data Set

# In[3]:


print(andr_data[10472])
print(len(andr_data[10472]))
print(len(andr_data[10471]))


# It can be seen that the row number 10472 has only **12** columns compared to the row number 10471. This error was reported in [Kaggle discussion Google Play Dataset](https://www.kaggle.com/lava18/google-play-store-apps/discussion/66015Thus). To handle this error, I've removed the column number 10472 by using the `del` built in function.

# In[4]:


del andr_data[10472]


# In[5]:


print(andr_data[10472])


# ## 2.2 Removing duplicated rows

# By exploring the Google Play data set, it is possible to see that some apps have **duplicated entries**. in the following, I will track all apps that have repeated entries and print some of them.

# In[6]:


unique_apps = []
duplicate_apps =[]
for i in andr_data:
    name_app = i[0]
    if name_app in unique_apps:
        duplicate_apps.append(name_app)
    else:
        unique_apps.append(name_app)
print(duplicate_apps[0:4])
number_duplicates = len(duplicate_apps)        
print("The number of duplicate apps:",(number_duplicates))


#    
#   Now, a methodology to remove the duplicated will be employed. First, lets check which variable differ for each repeated app.

# In[7]:


for i in andr_data:
    app_name = i[0]
    if app_name == "Quick PDF Scanner + OCR FREE":
        print(i)
        

    


# The criteria to select one of all repeated apps is the number of reviews. The highest, more recent is the app data and better for our analysis. This is used to remove the remaining data from the data set.

# 1. First we start creating an empty list `reviews_max{}`
# 2. Then we loop in the Google Play Data Set and assign, at each iteration, the app name to a variable `name` and the number of reviews to a variable `n_reviews`.
# 3. The first `if` test two conditions
#     * if there is already the current app in the dictionary
#     * if the associated value is lesser than the one already in position
# 4. The second `if` checks if the current app name in evaluation is already in the dictionary. If not, add it to the dictionary

# In[8]:


def rows_selection(dataset,name_idx,reviewn_idx):
    reviews_max = {}
    for i in dataset:
        name= i[name_idx]
        n_reviews = float(i[reviewn_idx])
        if name in reviews_max and reviews_max[name]<n_reviews:
            reviews_max[name] = n_reviews
        if name not in reviews_max:
            reviews_max[name]=n_reviews
    return reviews_max

Android_non_repeated = rows_selection(andr_data,0,3)
print('The amount of rows with no repeated apps in Android is equal to',len(Android_non_repeated))
    


# The next code line creates a initially empty list which will be filled with the non repeated entries.
# Then, we loop through the Google Play Data Set and then check two conditions:
# 1. If the current number of reviews equals the maximum *AND*
# 2. IF the app name was already assessed.
#  **The step 2 is important because the Google Play Data Set contains apps that may have the same numbers of reviews and all being the maximum value**

# In[9]:


android_clean = []
already_added = []
for i in andr_data:
    name = i[0]
    n_reviews = float(i[3])
    if n_reviews == Android_non_repeated[name] and name not in already_added:
        android_clean.append(i)
        already_added.append(name)
print('New Data set size is:',len(android_clean))
        


# The obtained Data set size is in agreement with the result obtained in the dictionary construction `review_max{}`

# ## 2.3 Removing apps with titles not in English Language

# Since we are only interested in apps developed in English Language, the non English Language written apps will be removed from the analysis.To do that, i'm going make use of the way the computer stores strings. It associate numbers to each symbol representing a letter. We can obtain this number by using the built in function `ord()`. The words in english are built with characters that ranges from 0 to 127. Then, we can check if the any string in the title exceed this range to exclude the corresponding app from the data set.

# The following function can classify most words in English or non-English.

# In[10]:


def word_class(string):
    for letter in string:
        if ord(letter)>127:
            return False
word_class('Docs To Go™ Free Office Suite') #testing function

        


# It can be that the previous algorithm missclassify English words due to the presence of special strings. To improve it, a new function will be defined in order to reduce the possibility of missclassification by introducing a more robust checking. The algorithm will return False only if **FOUR** or more strings are indexed greater than 127.

# In[11]:


def word_class2(string):
    true_count = 0
    for letter in string:
        letter_indx = ord(letter)    
        if letter_indx > 127:
            true_count += 1
    if true_count > 3:
        return(False)
    else:
        return(True)
        
        
word_class2('Instachat 😜') #testing function


# The following code removes non-English apps from Google Play and Apple Store Data Sets

# In[12]:


Android_English = []
IOS_English = []
for j in android_clean: #Looping through Google Play Data set with no repeated entries
    name = j[0]
    if word_class2(name):
        Android_English.append(j)
for i in ios_data: #Loooping through Apple Store Data set with no repeated entries
    name = i[1]
    if word_class2(name):
        IOS_English.append(i)   
print('The Google Play English data set has',len(Android_English),'rows')
print('\n')
print('The Apple Store English data set has',len(IOS_English),'rows')
print('\n')
print(Android_English[0])
    


# ## 2.4 Removing non-free apps

# In[13]:


android_finalclean = []
for i in Android_English:
    label = i[7]
    if label == '0':
        android_finalclean.append(i)

print('The Google play data set final length is',len(android_finalclean))

ios_finalclean = []
for i in IOS_English:
    label = i[4]
    if label == '0.0':
        ios_finalclean.append(i)

print('The IOS data set final length is',len(ios_finalclean)) 


# As the first paragraph stated, the objective of the present analysis is finding the characteristics that makes free apps profitable in both IOS and Android Markets. An strong indication of profitability is the number of users. So, this is the sensor to measure profitability success.

# ## 3. Genre Data Set Analysis

# In this section, i'm finally starting the analysis in order to reach the objective stated. This section is intended to rank the apps Genres. This will give a clue on what is the most frequent Genre and will be used later for the averaged numbers of users.

# ## 3.1 Basic Statistics - Calculating proportions of Genres

# In[14]:


def frequence_table(dataset,index):
    proportion = {}
    dictionary = {}
    for row in dataset:
        genre = row[index]
        if genre in dictionary:
            dictionary[genre] +=1
            proportion[genre] = dictionary[genre]/len(dataset)*100
        else:
            dictionary[genre] = 1
            proportion[genre] = dictionary[genre]/len(dataset)*100
    return proportion
            

ANDROID_frequency = frequence_table(android_finalclean,1)
#print(ANDROID_frequency)

print('This is the unsorted relative frequency table for Google Play Data Set')
print('\n')
print(ANDROID_frequency)

    
    


# The following code sort the dictionary in descending order of frequence by using a written function called `display_table`.

# In[15]:


def display_table(dataset, index):
    table = frequence_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])

print('Category relative frequence for Google Play Data Set')
display_table(android_finalclean,1)
print('\n')
print('Genre relative frequence for Google Play Data Set')
display_table(android_finalclean,9)


# In[16]:


print('Table2. Prime Genre relative frequence for Apple Store Data Set')
display_table(ios_finalclean,-5)


# ## 3.2 Results and Discussion

# 1. FOR **IOS**:
#  
#  - It can be seen in Table 2, that the majority of English free apps are entertaiment related. Games account for 58% of the total. However, it does not mean they are the most profitable (have highest numbers of users).
#  
# 2- FOR **ANDROID**
#  - It can be seen from table 1 from Google Play Data Set that the categories Family, Game and Tools accounts for 37% percent of the apps. It can be seen a different picture from IOS market. A significant percentage of apps are not entertainment purposed.When we analyze by genre, it is possible to see a more homogeneous distribution and lot of genres lying between zero and one percent frequence. This may be due to the huge amount of genre classification Google Play store allows.

# # 4. Averaged number of Users Analysis

# The following code is intended to calculate the average number of users by genre in Google Play and Apple Store final Data Sets.

# In[17]:


#Apple Store
def average_users_ios(dataset,genre_idx,users_idx):
    nusers = {} #dictionary for total number of users
    table = frequence_table(dataset, genre_idx)
    for i in dataset:
        genre = i[genre_idx]
        users = float(i[users_idx])
        if genre not in nusers:
            nusers[genre] = users/(table[genre]*len(dataset)/100)
        else:
            nusers[genre] += users/(table[genre]*len(dataset)/100)
    return nusers


def display_table2(table):
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])

test = average_users_ios(ios_finalclean,-5,5) 
print('Rank of averaged Apple Store app users by Genre')       
print('\n')
print(display_table2(test))
print('\n')


#Google Play
def average_users_android(dataset,genre_idx,users_idx):
    nusers = {} #dictionary for total number of users
    table = frequence_table(dataset, genre_idx)
    for i in dataset:
        genre = i[genre_idx]
        installs = i[users_idx]
        installs1 = installs.replace('+', '')
        installs2 = installs1.replace(',', '')
        users = float(installs2)
        if genre not in nusers:
            nusers[genre] = users/(table[genre]*len(dataset)/100)
        else:
            nusers[genre] += users/(table[genre]*len(dataset)/100)
    return nusers
test2 = average_users_android(android_finalclean,1,5)
print('Rank of averaged Google Play users by Genre')       
print('\n')
print(display_table2(test2))

        


# ## 4.1. Results and Discussion

# Based on the average users results on the previous section, it can be seen that for Apple Store, navigation apps are the most used. However this result is skewed since few apps concentrates the majority of users, thus the averaged number of users (users/number_of_apps) is very high. As example we can cite, Google Maps, Waze. 
# 
# The same happens for social networking such as Facebook, Twitter and Instagram. I could perform a few calculations to show a Paretto chart showing with the cumulative proportion of average users in the y axis and the ordinal variables in the x axis and we would able to see that few apps would respond to the majority of users. 
# 
# Thus it would not be a good choice to develop apps with such market. Its worth doing the referred chart at least for top 10 apps and choosing a treshold to pick apps that are not too close or to far from the most "concentrated region".
