#import matplotlib.pyplot as plt
import requests
#from PIL import Image
from io import BytesIO
import json
import re

endpoint = "https://westcentralus.api.cognitive.microsoft.com/"
subscription_key = ""#choose 

analyze_url = endpoint + "vision/v2.1/ocr"

# Set image_path to the local path of an image that you want to analyze.
image_path = "crop7.jpg" ### crop 6 and 7 is the one

# Read the image into a byte array
image_data = open(image_path, "rb").read()
# image = Image.open(BytesIO(image_data))
# print(image.size)
# new_Size = (int(image.size[0]/2), int(image.size[1]/2))
# image = image.resize(new_Size,Image.ANTIALIAS)
# # image.save(image_path,optimize=True,quality=95)
# exit()
# image_data = open(image_path, "rb").read()
headers = {'Ocp-Apim-Subscription-Key': subscription_key,
           'Content-Type': 'application/octet-stream'}
params = {'language': 'unk', 'detectOrientation': 'true'}
response = requests.post(
    analyze_url, headers=headers, params=params, data=image_data)
# response.raise_for_status()

# The 'analysis' object contains various fields that describe the image. The most
# relevant caption for the image is obtained from the 'description' property.
analysis = response.json()
'''
print(json.dumps(analysis, indent=4, sort_keys=True))
image_caption = analysis['regions'][2]['lines'][2]['words'][3]['text']
print(image_caption)
image_caption = analysis['regions'][5]['lines'][1]['words'][0]['text']
print (image_caption)
'''
# image_caption = analysis["description"]["captions"][0]["text"].capitalize()

# Display the image and overlay it with the caption.
# plt.imshow(image)
# plt.axis("off")
# _ = plt.title(image_caption, size="x-large", y=-0.1)

region_used = analysis['regions']### length 3
length_region = 0
list_title=[]
while(length_region < len(region_used)):

    first_part = region_used[length_region]
    #second_part = region_used[1]
    #third_part = region_used[2]
    
    first_sub_part = first_part['lines'] ### length is 9
    
    index_first_sub_part = 0
    
    while(index_first_sub_part <len(first_sub_part)):
        first_intermediate_part = first_sub_part[index_first_sub_part]['words']
        index_first_intermediate = 0
        title =''
        while(index_first_intermediate<len(first_intermediate_part)):
            title = title +' '+first_intermediate_part[index_first_intermediate]['text']
            index_first_intermediate = index_first_intermediate + 1
        list_title.append(title)  
        index_first_sub_part = index_first_sub_part + 1
    length_region = length_region + 1



text = " ".join(list_title)

#### Policy number
policy_regex = r'((?:policy\s*no\s*(?:\s*|.)\s*(?:\s|:)\s*\w+))'
policy_number = re.findall(policy_regex,text,re.IGNORECASE)
policy =policy_number[0].encode('ascii','ignore')
policy = policy.replace('Policy No','')
policy = policy.replace(':','')
policy = policy.replace('.','')
policy = policy.lstrip()
####  start date 
regex_start_date = r'(From\s*(?:\d+/\d+/\d+))'
start_date = re.findall(regex_start_date,text,re.IGNORECASE)
start_date = start_date[0].encode('ascii','ignore')
start_date = start_date.replace('From','')
start_date = start_date.lstrip()
#### end date
regex_end_date = r'(to\s*(?:\d+/\d+/\d+))'
end_date = re.findall(regex_end_date,text,re.IGNORECASE)
end_date = end_date[0].encode('ascii','ignore')
end_date = end_date.replace('to','')
end_date = end_date.lstrip()

# Sum insured 
regex_sum_insured = r'((?:SUM\s*INSURED\s*(?:\(|\s*)\s*(?:Rs\.?|\s*)\s*(?:\)|\s)\s*(?:\s|\:)\s*\d+\s*(?:\(|\s)\s*(?:Rs\.?|\s*)\s*\d+\s*\w+\s*\w+\s*\w+\s*(?:\)|\s)))'
sum_insured = re.findall(regex_sum_insured,text,re.IGNORECASE)
sum_insured  = sum_insured [0].encode('ascii','ignore')
sum_insured = sum_insured.replace(':','')
sum_insured= sum_insured.replace('SUM INSURED(Rs.)','')
sum_insured=sum_insured.replace('.','')
sum_insured  = sum_insured.lstrip()

#geo coordinates
lattitude_list = []
longitude_list = []
regex_latitudes = r'((?:Latitude))'
i =0
index_list = []
while(i<len(list_title)):
    lattitude = re.findall(regex_latitudes,list_title[i],re.IGNORECASE)
    if(lattitude != []):
        index_list.append(i)
    i = i + 1
j = 0
if(len(index_list)==4):
    while(j < len(index_list)):
        index = index_list[j]
        value = list_title[index]
        value  = value.encode('ascii','ignore')
        lati,lon = value.split(',')
        lati = lati.replace('Latitude','')
        lati = lati.replace(':','')
        lati = lati.lstrip()
        lattitude_list.append(lati)
        lon = lon.replace('Longitude','')
        lon = lon.replace(':','')
        lon = lon.lstrip()
        longitude_list.append(lon)
        
        j = j + 1
 
### interest rate
interest_regex = r'((?:\d\.\d\s*%))'  
interest = re.findall(interest_regex,text,re.IGNORECASE)  
interest = interest[0].encode('ascii','ignore')  
interest = interest.lstrip()
# premium
premium_regex = r'((?:Premium\s*(?:\(|\s*)\s*(?:\s|RS)\s*(?:\)\s*(?:\s|\:)\s*(?:Rs|\s)(?:\s|\.)\s*\d+)))'
premium = re.findall(premium_regex,text,re.IGNORECASE)
premium = premium[0].encode('ascii','ignore')
premium = premium.replace('PREMIUM (Rs)','')
premium = premium.replace(':','')
premium = premium.lstrip()

############# creating dictionary
dict_list ={'policy_no':policy,'start_date':start_date,'end_date':end_date,'sum_insured':sum_insured,\
            'geo_coordinates_lattitude':lattitude_list,'geo_coordinates_longtitude':longitude_list,\
            'interest_rate':interest,'premium_value':premium}
