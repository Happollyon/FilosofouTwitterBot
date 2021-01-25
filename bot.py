from requests_oauthlib import OAuth1
from requests.utils import quote
from PIL import Image, ImageFont,ImageDraw,ImageOps
import glob, os, requests,random,string,time, hashlib, hmac, base64,tweepy,json
from hashlib import sha1


#This funciton creates the image to be tweeted back to the user.
def createImage(text,username,userprofile,backgroundImage):
    oauth_consumer_KEY= "uIMIjQPNpRNThpvZV0PrmtkSf"
    oauth_consumer_secrete= "fXxuzxuM0OxaKzhgbRQ0pLvwbgCc2uPrgtwj0Q2NJZUDVgB1xx"
    oauth_token= "1349500149396082688-RMlUZfOkdQYEHokXDXwd1Lqgzyo7jt"
    oauth_secret_token= "uUH2yfUNDypNwikkt6WY8cC7GjrV6D1O0dVlWJyEYdEKv"
    bearer_token= "Bearer AAAAAAAAAAAAAAAAAAAAAGUbLwEAAAAARixXM9tGdeIw0Q5MaZIbTdg8Hzk%3Defz0L9377HhZsuxDylZdJsR0uSzucGNktndyVA1LgzxYahTuLY"
    
    auth = tweepy.OAuthHandler(oauth_consumer_KEY,oauth_consumer_secrete)
    auth.set_access_token(oauth_token,oauth_secret_token)
    api = tweepy.API(auth)
    
    username = '@' +username 
    text = '"'+text+'"'
# loads the image or creates black rectangle

    image = Image.open(backgroundImage)
    #image = Image.new("RGB",(1200,800))

# Gets the dimensions and calculates where to place the text
    if len(text)<=195:
        font_size = 40
    else:
        font_size = 40
    
    width = image.width
    height = image.height
    newWidth = width*.90
    newHeight = height *.90
    charNumb = round(width/(25*1.333)) 

# Prepares the text to be pasted on image   
    newText=''
    for i in range(0,len(text)):
        
        newText += text[i]  
        if (i+1) % charNumb == 0:
            if text[i] ==' ':
                newText += '\n'
            else:
                j = i
                space=False
                while(space==False):
            
                    if newText[j] == " ":
                        newText =newText[:j+1]+ '\n'+newText[j+1:]
                        space = True
                    j -= 1

# this section prepares user avatar
    
    avatar = Image.open(requests.get(userprofile, stream=True).raw)    
    avatar = avatar.convert('LA')
    avatar = avatar.convert('RGBA')
    
    avatar = avatar.resize((300,300),box=None,reducing_gap=None)
    
    #mask = Image.open("images/mask.png")
    #mask = mask.resize((100,100),box=None,reducing_gap=None)
    #avatar = ImageOps.fit(avatar,mask.size,centering=(0.5,0.5))
    #alpha = mask.split()[-1]
    #avatar.putalpha(alpha)
    
    size = (300,300)
    mask = Image.new('L', size, 0)
    drawMask = ImageDraw.Draw(mask) 
    drawMask.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    
# manipulates the image
    
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("fonts/Fraunces-VariableFont_SOFT,WONK,opsz,wght.ttf",font_size)
    draw.text((width*.1,height*.8),username,font=font)
    draw.text((width*.13,height*.1),newText,font=font)
    
    image.paste(output,(width-334,height-347),output)

       
    filename = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))
    image = image.resize((600,400),Image.ANTIALIAS)
    image.save(filename+'.png')
    res = api.media_upload(filename+'.png')
    os.remove(filename+'.png')
    
    return [res.media_id]
    
#print(2)
#createImage('Caso eu venha a falecer, gostaria de deixar registrado aqui tambm que tenho interesse em ser doador de e tecidos.','fagnernunes11','https://pbs.twimg.com/profile_images/1251218278191640576/UpID8lrn_400x400.jpg','images/image1.png')

def postAtweet(media_id,token,oauth_consumer_secret, oauth_token_secret,status,in_reply_to_status_id,oauth_consumer_key,oauth_token):
    
    
# using tweepy to post a tweet 
    auth = tweepy.OAuthHandler(oauth_consumer_key,oauth_consumer_secret)
    auth.set_access_token(oauth_token,oauth_token_secret)
    api = tweepy.API(auth)
        
    res = api.update_status(status,in_reply_to_status_id=in_reply_to_status_id,media_ids=media_id)
    
# end of tweepy    
      

def getMentions():
    oauth_consumer_KEY= "uIMIjQPNpRNThpvZV0PrmtkSf"
    oauth_consumer_secrete= "fXxuzxuM0OxaKzhgbRQ0pLvwbgCc2uPrgtwj0Q2NJZUDVgB1xx"
    oauth_token= "1349500149396082688-RMlUZfOkdQYEHokXDXwd1Lqgzyo7jt"
    oauth_secret_token= "uUH2yfUNDypNwikkt6WY8cC7GjrV6D1O0dVlWJyEYdEKv"
    bearer_token= "Bearer AAAAAAAAAAAAAAAAAAAAAGUbLwEAAAAARixXM9tGdeIw0Q5MaZIbTdg8Hzk%3Defz0L9377HhZsuxDylZdJsR0uSzucGNktndyVA1LgzxYahTuLY"
    

    auto = OAuth1(oauth_consumer_KEY,oauth_consumer_secrete, oauth_token,oauth_secret_token )
    
    with open('test.json','r+') as file:
        data = json.load(file)
        last_mention = data['last_mention']
                  
    mentions =  requests.get('https://api.twitter.com/1.1/statuses/mentions_timeline.json?since_id='+last_mention,auth=auto)      

    response =  mentions.json()
    
    for mention in reversed(response):   
        tweet= requests.get('https://api.twitter.com/2/tweets?ids='+mention['in_reply_to_status_id_str']+'&user.fields=profile_image_url&expansions=author_id', auth=auto)
        with open('test.json','r+') as file:
            data = json.load(file)
            #print('updated')
            data['last_mention'] = mention['id_str']
            file.seek(0)
            file.write(json.dumps(data))
            file.truncate()
        text = tweet.json()
        url = text['includes']['users'][0]['profile_image_url']
        url= url.replace("normal","400x400")
        media_id = createImage(text['data'][0]['text'],mention['in_reply_to_screen_name'],url,'images/image1.png')               
        status = '@'+mention['user']['screen_name'] +' '+'@'+mention['in_reply_to_screen_name']
        if mention['user']['screen_name'] != 'filosofou4' and mention['in_reply_to_screen_name']!= 'filosofou4':
            postAtweet(media_id,auto,oauth_consumer_secrete,oauth_secret_token,status,mention['id_str'],oauth_consumer_KEY,oauth_token)
            

starttime = time.time()
i = 0
while True:
    getMentions()
    i+=1
    
    time.sleep(90 - ((time.time() - starttime) % 60.0))
