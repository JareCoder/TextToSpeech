from google.cloud import texttospeech
import os
import textract
import tkinter as tk
from tkinter import filedialog

appPath = os.path.dirname(os.path.abspath(__file__))

#Google Authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r''+appPath+"/OSM Fireextinguisher-9bf685177ed7.json"
print('Credendtials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))

#Smart file reader
def StringSplitter(text, split="*/*"):
    list = []
    a=0
    text = str(text)

    if split=="":
        split="*/*"

    #print(split)

    while a<len(text):
        a = text.find(split)+len(split)
        b = text.find(split, a)

        #print(a)
        #print(b)
        #print(text[a:b])

        if a == -1 or b == -1:
            break
    
        list.append(text[a:b])
        text=text[b+1:]

    return list

def OutPutFolder(path):
    #Output folder

    print("\n")

    if path != "_":

        UI = input("Saving method: \n1. Use saved folder \n2. Select a new folder \n")

        if UI == "1":
            print("Using saved folder: "+path)

        elif UI == "2":

            input("Select a folder to save the files to. Press ENTER to continue.")

            path = r''+filedialog.askdirectory()

    else:
        input("Select a folder to save the files to. Press ENTER to continue.")

        path = r''+filedialog.askdirectory()

    return path

def SaveFiles(ReadList, ConfValue):

    #Setting values the lazy way
    path = ConfValue[0]
    lang_code = ConfValue[1]
    lang_name = ConfValue[2]
    pitch = int(ConfValue[4])
    speed = float(ConfValue[5])

    #print(path)
    #print(lang_code)
    #print(lang_name)
    #print(pitch)
    #print(speed)

    #Getting path
    path = OutPutFolder(path)
    #print(path)
    
    #File name
    name = input("Insert name for files: ")
    
    count = 0

    #Going through all found texts and making them into audio files
    for i in ReadList:

        count += 1

        fileName = path+'/'+name+str(count)
        
        #Setting up T2Speech
        client = texttospeech.TextToSpeechClient()

        s_input = texttospeech.SynthesisInput(text=i)

        if ConfValue[3] == "MALE":
            voice = texttospeech.VoiceSelectionParams(language_code=lang_code, name=lang_name, ssml_gender=texttospeech.SsmlVoiceGender.MALE)
        elif ConfValue[3] == "FEMALE":
            voice = texttospeech.VoiceSelectionParams(language_code=lang_code, name=lang_name, ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
        else:
            voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Standard-C", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)

        audio_cfg = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=speed, pitch=pitch)

        response = client.synthesize_speech(input=s_input, voice=voice, audio_config=audio_cfg)

        #Output as MP3
        with open(fileName+".mp3", "wb") as out:
            out.write(response.audio_content)
            print('Audio saved to file "'+fileName+'.mp3"')

    return path

def ReadFile(ConfValue = []):
    try:
        #print("1")
        with open("config.txt", "r") as file:
            for line in file:
                fileLine = line.strip()
                fileLine = fileLine.split(": ")
                ConfValue.append(fileLine[1])
                #print(ConfValue)

    except:
        print("Error reading the config file. Creating a new one.")
        with open("config.txt", "w") as file:
            file.write('Path: _  \nLanguage Code: en_US \nLanguage Name: en-US-Standard-D \nLanguage Gender: MALE \nPitch: 0 \nSpeed: 1.0')
        ReadFile(ConfValue)

    
    #print("2")
    return ConfValue

def SaveConfFile(ConfValue, path):
    print("Saving Config file...")
    with open("config.txt", "w") as file:
        file.write('Path: '+path+'\nLanguage Code: '+ConfValue[1]+'\nLanguage Name: '+ConfValue[2]+'\nLanguage Gender: '+ConfValue[3]+'\nPitch: '+ConfValue[4]+'\nSpeed: '+ConfValue[5])


def Options(ConfValue):
    while True:
        NewScreen()
        print('1. Language Code: '+ConfValue[1]+'\n2. Language Name: '+ConfValue[2]+'\n3. Language Gender: '+ConfValue[3]+'\n4. Pitch: '+ConfValue[4]+'\n5. Speed: '+ConfValue[5]+'\n6. Quit')
    
        a = input("\nSelect an option: ")

        if a == "1":
            ConfValue[1] = input('Insert Langage Code (en_US): ')
            continue
        elif a == "2":
            ConfValue[2] = input('Insert Langage Name (en-US-Standard-D): ')
            continue
        elif a == "3":
            ConfValue[3] = input('Insert Language Gender (MALE or FEMALE): ')
            continue
        elif a == "4":
            ConfValue[4] = input('Insert Pitch (0): ')
            continue
        elif a == "5":
            ConfValue[5] = input('Insert Speed (1.0): ')
            continue
        elif a == "6":
            NewScreen()
            break
        else:
            input("Invalid input! Press ENTER to try again")
            continue

        break

    return ConfValue


def NewScreen():
    for i in range(100):
        print("\n")

#---PROGRAM---

#Tkinter setup
root = tk.Tk()
root.withdraw()

#Reading settings
ConfValue = ReadFile()
path = ConfValue[0]
#print(path)

while True:

    print("\nText2Speech")
    a = input("1. Select file\n2. Change settings \n3. Quit\n")

    if a == "1":

        #filepath popup
        file_path = r''+filedialog.askopenfilename()
        print(file_path)

        #Getting text out of the file
        text = textract.process(file_path)
        #print(text)


        #Using smart file reader
        default = input("Insert split word or characters. Leave empty if using default (*/*): ")
        print("Processing...")
        ReadList = StringSplitter(text, default)
        print("Generating "+ str(len(ReadList))+ " audio files.")


        f = SaveFiles(ReadList, ConfValue)
        continue

    elif a == "2":
        ConfValue = Options(ConfValue)
        continue

    elif a == "3":
        try:
            SaveConfFile(ConfValue, f)
        except:
            print("Program hasn't been used. Changes to config file will not be saved!")

        print("Quitting...")
        break

    else:
        input("Input false. Press ENTER to try again.")
        NewScreen()
        continue

    break


    
