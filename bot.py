# twitter bot that sends
# function twitterBot runs every 6 seconds
# function createimage(text,username,userprofilePic)
# function checkForMentions(lastMentionId)
# funciton replyTweet(tweetId,username)

"""
every 6 seconds run twitter bot funcion

"""
from requests_oauthlib import OAuth1
from requests.utils import quote
from PIL import Image, ImageFont,ImageDraw,ImageOps
import glob, os, requests,random,string,time, hashlib, hmac, base64,tweepy
from hashlib import sha1


#This funciton creates the image to be tweeted back to the user.

def createImage(text,username,userprofile,backgroundImage):

    username = '@' +username 
    text = '"'+text+'"'
# loads the image or creates black rectangle

    #image = Image.open(backgroundImage)
    image = Image.new("RGB",(600,400))

# Gets the dimensions and calculates where to place the text
    width = image.width
    height = image.height
    newWidth = width*.90
    newHeight = height *.90
    charNumb = round(width/(10*1.333)) 

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
    print(userprofile)
    avatar = Image.open(requests.get(userprofile, stream=True).raw)    
    avatar = avatar.resize((100,100),box=None,reducing_gap=None)
    #mask = Image.open("images/mask.png")
    #mask = mask.resize((100,100),box=None,reducing_gap=None)
    #avatar = ImageOps.fit(avatar,mask.size,centering=(0.5,0.5))
    #alpha = mask.split()[-1]
    #avatar.putalpha(alpha)
    
    size = (100,100)
    mask = Image.new('L', size, 0)
    drawMask = ImageDraw.Draw(mask) 
    drawMask.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    print(avatar.width, avatar.height)
# manipulates the image
    draw = ImageDraw.Draw(image)
    #draw.rectangle([(newWidth,newHeight),(width*.1,height*.1)],fill="#000000",outline="red")
    font = ImageFont.truetype("fonts/Fraunces-VariableFont_SOFT,WONK,opsz,wght.ttf",16)
    draw.text((width*.1,height*.8),username,font=font)
    draw.text((width*.1,height*.1),newText,font=font)
    image.paste(output,(round(width*.7),round(height*.6)),output)
    image = image.convert('LA')
    #output.show()
    image.show()
    return


#createImage('On Wednesday, Trump became the first US president in history to be impeached twice after the House of Representatives voted on one article of impeachment, charging him with inciting the January 6 attack on the US Capitol building. The next phase is for the Senate to hold a trial','fagnernunes','images/user1.jpg','images/2.jfif')

def createSignature(consumer_secret,oauth_token_secret):
    signing_key = quote(consumer_secret,safe = '')+'&'+quote(oauth_token_secret,safe = '')
    
    return signing_key



def postAtweet(token,oauth_consumer_secret, oauth_token_secret,status,in_reply_to_status_id,oauth_consumer_key,oauth_token):
    

# using tweepy to post a tweet 
    auth = tweepy.OAuthHandler(oauth_consumer_key,oauth_consumer_secret)
    auth.set_access_token(oauth_token,oauth_token_secret)
    api = tweepy.API(auth)
    api.update_status('teste')
# end of tweepy    
    include_entities = 'true'
    oauth_nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))
    oauth_version = '1.0'
    oauth_signature_method = 'HMAC-SHA1'
    oauth_timestamp = str(time.time())
    cleanURL = 'https://api.twitter.com/1.1/statuses/update.json?status='+status+'&in_reply_to_status_id='+in_reply_to_status_id    
    url = quote('https://api.twitter.com/1.1/statuses/update.json?status='+status+'&in_reply_to_status_id='+in_reply_to_status_id,safe = '')
    
    
    paramters = {
            quote('status',safe = ''):quote(status,safe = ''),
            quote('include_entities',safe = ''):quote(include_entities,safe = ''),
            quote('oauth_consumer_key',safe = ''):quote(oauth_consumer_key,safe = ''),
            quote('oauth_nonce',safe = ''):quote(oauth_nonce,safe = ''),
            quote('oauth_signature_method',safe = ''):quote(oauth_signature_method,safe = ''),
            quote('oauth_timestamp',safe = ''):quote(oauth_timestamp,safe = ''),
            quote('oauth_token',safe = ''):quote(oauth_token,safe = ''),
            quote('oauth_version',safe = ''):quote(oauth_version,safe = '')
            }

    paramter_string=''
    
    for key in sorted(paramters):
        if(key!='status'):
            paramter_string += key+'='+paramters[key]
     
    signatureBaseString = 'POST&'+url+'&'+quote(paramter_string,safe='')
    signing_key = oauth_consumer_secret+'&'+oauth_token_secret
    key = bytes(signatureBaseString,'utf-8')
    message = bytes(signatureBaseString,'utf-8')
    digester = hmac.new(key, message, sha1).digest()
    signaturekey = base64.urlsafe_b64encode(digester)      
    signaturekey = signaturekey.decode('utf-8').rstrip('\n')
    #print(token)
    header = {'authorization':'OAuth',
             'oauth_consumer_key':oauth_consumer_key,
             'oauth_nonce':oauth_nonce,
             'oauth_signature_method':oauth_signature_method,
             'oauth_timestamp':oauth_timestamp,
             'oauth_token':oauth_token,
             'oauth_version':oauth_version}
    response = requests.post(cleanURL,auth=token)
    print(response.text)

def postImage(status,in_reply_to_status_id,auth):
    url = 'https://api.twitter.com/1.1/statuses/update.json?status='+status+'&in_reply_to_status_id='+in_reply_to_status_id
    response = requests.get(url,auth=auth)
    print(response)

def getMentions():
#    GET https://api.twitter.com/1.1/statuses/mentions_timeline.json?count=2&since_id=14927799
    oauth_consumer_KEY= "uIMIjQPNpRNThpvZV0PrmtkSf"
    oauth_consumer_secrete= "fXxuzxuM0OxaKzhgbRQ0pLvwbgCc2uPrgtwj0Q2NJZUDVgB1xx"
    oauth_token= "1349500149396082688-RMlUZfOkdQYEHokXDXwd1Lqgzyo7jt"
    oauth_secret_token= "uUH2yfUNDypNwikkt6WY8cC7GjrV6D1O0dVlWJyEYdEKv"
    bearer_token= "Bearer AAAAAAAAAAAAAAAAAAAAAGUbLwEAAAAARixXM9tGdeIw0Q5MaZIbTdg8Hzk%3Defz0L9377HhZsuxDylZdJsR0uSzucGNktndyVA1LgzxYahTuLY"
    

    auto = OAuth1(oauth_consumer_KEY,oauth_consumer_secrete, oauth_token,oauth_secret_token )
    mentions =  requests.get('https://api.twitter.com/1.1/statuses/mentions_timeline.json',auth=auto)   
    response =  mentions.json()
    for mention in response:   
        tweet= requests.get('https://api.twitter.com/2/tweets?ids='+mention['in_reply_to_status_id_str']+'&user.fields=profile_image_url&expansions=author_id', auth=auto)
    
        text = tweet.json()
        url = text['includes']['users'][0]['profile_image_url']
        url= url.replace("normal","400x400")
        #createImage(text['data'][0]['text'],mention['in_reply_to_screen_name'],url,'backgroundImage'               
        status = '@'+mention['user']['screen_name'] +' '+'@'+mention['in_reply_to_screen_name']
       
        postAtweet(auto,oauth_consumer_secrete,oauth_secret_token,status,mention['id_str'],oauth_consumer_KEY,oauth_token)
                
        
getMentions()
#postAtweet('Hello Ladies + Gentlemen, a sigined OAuth request!','true','xvz1evFS4wEEPTGEFPHBog','kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg','HMAC-SHA1','1318622958','370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb','1.0')
