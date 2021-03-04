#####################
###     TODO      ###
#####################
#Faire une liste à part avec toutes les images à printer
#Créer un fichier word avec les images à printer et attribuer directement le nom du protocole et num d'attachement


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

import cv2
import pytesseract
from os import listdir
from os.path import isfile, join

PATH = "C:\\Users\\WilliamMichaux\\Desktop\\3 - WN30 robot\\Screenshots\\"
fichiers = [f for f in listdir(PATH) if f[-4:] == ".png"]
#recherche = input("Champ cherché : ")

EltRecherche = ["20038", "20039","20041"]
pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\WilliamMichaux\\AppData\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
nbTrouve = 0
i = 0
printProgressBar(0, len(fichiers), prefix = "Progress:", suffix = "Complete", length=50)
for fichier in fichiers:
    if len(EltRecherche) > 0:
        image = cv2.imread(PATH + fichier)
    #image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

        hImg, wImg, _ = image.shape
        conf = r'--oem 3 --psm 6 outputbase digits'
        boxes = pytesseract.image_to_data(image, config=conf)

        for x,b in enumerate(boxes.splitlines()):
            if x != 0 and len(EltRecherche) > 0:
                b = b.split()
                if len(b) == 12:
                    for recherche in EltRecherche:
                        if recherche in b[11]:
                            x,y,w,h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                            cv2.rectangle(image, (x,y), (w+x, h+y), (247,255,0),2)
                            cv2.imshow('Result ' + fichier, image)
                            #cv2.putText(image,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(247,255,0),3)
                            nbTrouve += 1
                            EltRecherche.pop(EltRecherche.index(recherche))
        i = i+1
        printProgressBar(i, len(fichiers), prefix = "Progress:", suffix = "Complete \t| Found : " + str(nbTrouve), length=50)

print("Nombre de screen trouvés :", nbTrouve)
cv2.waitKey(0)
