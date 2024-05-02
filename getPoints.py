import cv2 as cv
from sys import argv
import requests

from imageWorker import *
from coordinatesWorker import *
from constants import PROJECT_FOLDER

def writeToFile(pairs):
    file = open(fr'{PROJECT_FOLDER}\resources\points.txt', 'w')
    for pair in pairs:
        file.write(f'{pair[0]} {pair[1]}\n')
        
        
def saveGraphImage(pairs):
    x, y = list(zip(*pairs))

    plt.plot(x, y)
    plt.grid(True)
    plt.xlabel('2О, град')
    plt.ylabel('Интенсивность (импл/сек)')

    plt.savefig(fr'{PROJECT_FOLDER}\resources\graphic.png')


def getGraphicPoints(image_url, x_min, y_min, x_max, y_max):
    
    response =  requests.get(image_url).content
    nparr = np.frombuffer(response, np.uint8)
    image = cv.imdecode(nparr, cv.IMREAD_GRAYSCALE)
    
    image = makeBlackAndWhite(image)
            
    im_rows, first_row, last_row = removeHorizontalAxes(image)
    cleared_image, first_col, last_col = removeVerticalAxes(im_rows[first_row:last_row])
    cleared_image = cleared_image[:, first_col:last_col]
            
    coordinates = getImageCoordinates(cleared_image)
    coordinates.sort()
    x, y = map(list, zip(*coordinates))
    x_scaled = scale(x, x_min, x_max)
    y_scaled = scale(y, y_min, y_max)
            
    function = getGraphicFunction(x_scaled, y_scaled)
    unique_x = list(set(x_scaled))
    unique_x.sort()
            
    coords = [(x_val, function(x_val)) for x_val in unique_x]
    #writeToFile(coords)
    #saveGraphImage(coords)
    return coords