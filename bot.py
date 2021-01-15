# twitter bot that sends
# function twitterBot runs every 6 seconds
# function createimage(text,username,userprofilePic)
# function checkForMentions(lastMentionId)
# funciton replyTweet(tweetId,username)

"""
every 6 seconds run twitter bot funcion

"""

from PIL import Image, ImageFont,ImageDraw,ImageOps
import glob, os
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
    avatar = Image.open(userprofile)
    print(avatar.width,avatar.height)
    #avatar = avatar.resize((100,100),box=None,reducing_gap=None)
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


createImage('On Wednesday, Trump became the first US president in history to be impeached twice after the House of Representatives voted on one article of impeachment, charging him with inciting the January 6 attack on the US Capitol building. The next phase is for the Senate to hold a trial','fagnernunes','images/user1.jpg','images/2.jfif')
