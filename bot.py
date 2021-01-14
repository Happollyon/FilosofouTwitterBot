# twitter bot that sends
# function twitterBot runs every 6 seconds
# function createimage(text,username,userprofilePic)
# function checkForMentions(lastMentionId)
# funciton replyTweet(tweetId,username)

"""
every 6 seconds run twitter bot funcion

"""

from PIL import Image, ImageFont,ImageDraw
import glob, os
#This funciton creates the image to be tweeted back to the user.

def createImage(text,username,userprofile,backgroundImage):
# loads the image or creates black rectangle

    #image = Image.open(backgroundImage)
    image = Image.new("RGB",(600,400))

# Gets the dimensions and calculates where to place the text
    width = image.width
    height = image.height
    newWidth = width*.90
    newHeight = height *.90
    charNumb = round(width/(9*1.333)) 

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
                        print(text[j-1],text[j],text[j+1])
                        newText =newText[:j+1]+ '\n'+newText[j+1:]
                        space = True
                    j -= 1


  
# manipulates the image
    draw = ImageDraw.Draw(image)
    #draw.rectangle([(newWidth,newHeight),(width*.1,height*.1)],fill="#000000",outline="red")
    font = ImageFont.truetype("fonts/Fraunces-VariableFont_SOFT,WONK,opsz,wght.ttf",15)
    draw.text((width*.1,height*.1),newText,font=font)
    

    image.show()
    return


createImage('On Wednesday, Trump became the first US president in history to be impeached twice after the House of Representatives voted on one article of impeachment, charging him with inciting the January 6 attack on the US Capitol building. The next phase is for the Senate to hold a trial','fagnernunes','image','images/2.jfif')
