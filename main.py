import tools
import keras
from keras import layers

search = input('search>> ')
tools.grabFromGoogleImages(search)
tools.cropAll()
tools.resizeAll((50, 50))

model = keras.models.Sequential()
model.add(layers.Conv2D())
