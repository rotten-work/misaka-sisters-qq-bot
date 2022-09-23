from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

# Import magic cause weired problems. Don't know why for now.
# from graia.ariadne.message.element import Plain
from graia.ariadne.message.element import *
# from graia.ariadne.message.element import Member
# import graia.ariadne.message.element as element
from graia.ariadne.message.parser.base import *


import io
import pathlib
# import PIL.Image
from  PIL import Image as PILImage
# from PIL import GifImagePlugin
# GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS

import json
import requests

import random
import numpy as np

from tensorflow.keras.applications.vgg19 import preprocess_input, decode_predictions

use_tf_serving = False

cat_breeds = [
    "tabby",
    "tiger_cat",
    "Persian_cat",
    "Siamese_cat",
    "Egyptian_cat",
    "lynx" # Not a cat, but very close to cats
    ]

emoji_gif_filenames = [
    "detect_a_cat_12fps_optim.gif",
    "meow_12fps.gif"
    ]

lines_when_seeing_cats = [
    "好可爱，是御坂发现的哦，と，御坂如此宣扬自己的功绩",
    "喵···"
    ]

if use_tf_serving:
    MODEL_DIR = "vgg_serving"
else:
    from tensorflow.keras.applications.vgg19 import VGG19
    
    model = VGG19(weights='imagenet')
    # Probably we can feed fake data to model.predict to preload cuDNN to increase performance

channel = Channel.current()

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage]))
async def see_a_cat(app: Ariadne, member: Member, group: Group, message: MessageChain):
    img_elements = message[Image]
    print(img_elements)

    is_a_cat = False
    if (img_elements):
        img_elem = img_elements[0]
        img_bytes = await img_elem.get_bytes()
        img = PILImage.open(io.BytesIO(img_bytes))
        img = img.convert('RGB')
        # img.show()

        img = img.resize((224, 224), resample=PILImage.BILINEAR)
        img_array = np.array(img)
        # if (len(img_array.shape) == 2):
        #     img_array = np.stack((img_array,)*3, axis=-1)
        # elif (len(img_array.shape == 3)):
        #     if (img_array.shape[-1] == 4):
        #         img_array = img_array[:, :, :3]
        # else:
        #     raise ValueError(f'Unsupported image shape: {img_array.shape}')

        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        preds = None

        if use_tf_serving:
            print("Using Tensorflow Serving:")

            MODEL_DIR = "vgg_serving"
            data = json.dumps({"instances": img_array.tolist()})
            json_response = requests.post(f"http://localhost:8501/v1/models/{MODEL_DIR}:predict", data=data)

            prediction_list = json.loads(json_response.text)['predictions']
            # convert list to array
            preds = np.asarray(prediction_list)
        else:
            preds = model.predict(img_array)
            
        # decode the results into a list of tuples (class, description, probability)
        # (one such list for each sample in the batch)
        labels_top = decode_predictions(preds, top=3)[0]
        # Predicted: [(u'n02504013', u'Indian_elephant', 0.82658225), (u'n01871265', u'tusker', 0.1122357), (u'n02504458', u'African_elephant', 0.061040461)]
        print('Predicted:', labels_top)

        for label in labels_top:
            if (label[1] in cat_breeds):
                is_a_cat = True
                break

        print("Is it a cat?", is_a_cat)

    if (is_a_cat):
        idx = random.randint(0, 1)
        gif_filename = emoji_gif_filenames[idx]
        line = lines_when_seeing_cats[idx]

        current_dir = pathlib.Path(__file__).parent.resolve()
        gif_path = pathlib.Path(current_dir, gif_filename)

        img_elem = Image(path=gif_path)
        message = MessageChain.create(
            At(member),
            img_elem,
            Plain(line)
        )
        
        await app.sendGroupMessage(
            group,
            message
        )