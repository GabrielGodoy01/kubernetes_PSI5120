import numpy as np
import cv2
import base64
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions

# Load the pre-trained ResNet50 model
model = ResNet50(weights='imagenet')

# Base64 string of the image
base64_string = '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'

# Decode the base64 string to a numpy array
img_data = base64.b64decode(base64_string)
np_arr = np.frombuffer(img_data, np.uint8)

# Decode the numpy array to an image
img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

# Preprocess the image
img = cv2.resize(img, (224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

# Make predictions
preds = model.predict(x)

# Decode and display predictions
print('Predicted:', decode_predictions(preds, top=3)[0])