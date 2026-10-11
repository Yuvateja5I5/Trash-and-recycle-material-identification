# Create your views here.
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import UserRegistrationModel
from django.conf import settings


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})

# def training(request):
#     import numpy as np
#     import pandas as pd
#     import os
#     import cv2
#     import matplotlib.pyplot as plt
#     import seaborn as sns
#     import tensorflow as tf
#     import keras
#     from tqdm import tqdm
#     from keras.callbacks import EarlyStopping, ModelCheckpoint
#     from sklearn.metrics import confusion_matrix, accuracy_score
#     from sklearn.metrics import classification_report
#     from sklearn.model_selection import train_test_split
#     from sklearn.preprocessing import LabelEncoder
#     import glob
#     import pandas as pan
#     import matplotlib.pyplot as plotter
#     import warnings
#     warnings.filterwarnings('ignore')

#     # Create Files_Name
#     image_data = r'media\garbage_classification'
#     pd.DataFrame(os.listdir(image_data), columns=['Files_Name'])

#     files = [i for i in glob.glob(image_data + "//*//*")]
#     np.random.shuffle(files)
#     labels = [os.path.dirname(i).split("/")[-1] for i in files]
#     data = zip(files, labels)
#     dataframe = pan.DataFrame(data, columns=["Image", "Label"])
#     dataframe

#     sns.countplot(x=dataframe["Label"])
#     plotter.xticks(rotation=50)

#     train_data_dir = image_data
#     batch_size = 128
#     target_size = (224, 224)
#     validation_split = 0.2

#     train = tf.keras.preprocessing.image_dataset_from_directory(
#         train_data_dir,
#         validation_split=validation_split,
#         subset="training",
#         seed=50,
#         image_size=target_size,
#         batch_size=batch_size,
#     )
#     validation = tf.keras.preprocessing.image_dataset_from_directory(
#         train_data_dir,
#         validation_split=validation_split,
#         subset="validation",
#         seed=100,
#         image_size=target_size,
#         batch_size=batch_size,
#     )

#     class_names = train.class_names
#     class_names

#     plt.figure(figsize=(10, 10))
#     for images, labels in train.take(1):
#         for i in range(8):
#             ax = plt.subplot(8, 4, i + 1)
#             plt.imshow(images[i].numpy().astype("uint8"))
#             plt.title(class_names[labels[i]])
#             plt.axis("off")

#     base_model = tf.keras.applications.EfficientNetV2B1(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
#     base_model.trainable = False
#     keras_model = keras.models.Sequential()
#     keras_model.add(base_model)
#     keras_model.add(keras.layers.Flatten())
#     keras_model.add(keras.layers.Dropout(0.5))
#     keras_model.add(keras.layers.Dense(13, activation=tf.nn.softmax))  # 12 classes
#     keras_model.summary()

#     tf.keras.utils.plot_model(keras_model, to_file='model.png', show_shapes=True, show_layer_names=True, show_dtype=True, dpi=100)

#     checkpoint = ModelCheckpoint("my_keras_model.h5", save_best_only=True)

#     early_stopping = EarlyStopping(patience=10, restore_best_weights=True)  # patience from 5 to 10

#     keras_model.compile(optimizer='Adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

#     hist = keras_model.fit(train, epochs=1, validation_data=validation, callbacks=[checkpoint, early_stopping])

#     # Save the model
#     keras_model.save("Garbage_model.h5")

#     score, acc = keras_model.evaluate(validation)
#     print('Test Loss =', score)
#     print('Test Accuracy =', acc)

#     hist_df = pd.DataFrame(hist.history)
#     hist_df

#     train_loss = hist_df['loss'].tolist()
#     val_loss = hist_df['val_loss'].tolist()
#     train_accuracy = hist_df['accuracy'].tolist()
#     val_accuracy = hist_df['val_accuracy'].tolist()

#     plt.figure(figsize=(15, 5))
#     plt.subplot(1, 2, 1)
#     plt.plot(train_loss, label='Train Loss')
#     plt.plot(val_loss, label='Validation Loss')
#     plt.title('Train Loss & Validation Loss', fontsize=20)
#     plt.legend()
#     plt.subplot(1, 2, 2)
#     plt.plot(train_accuracy, label='Train Accuracy')
#     plt.plot(val_accuracy, label='Validation Accuracy')
#     plt.title('Train Accuracy & Validation Accuracy', fontsize=20)
#     plt.legend()
#     plt.show()
#     return render(request, 'users/training.html', {
#     'train_loss': train_loss,
#     'val_loss': val_loss,
#     'train_accuracy': train_accuracy,
#     'val_accuracy': val_accuracy
# })
from django.shortcuts import render
import os
import warnings
warnings.filterwarnings('ignore')

def training(request):
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    from tensorflow import keras
    from keras.callbacks import EarlyStopping, ModelCheckpoint
    import matplotlib.pyplot as plt

    # ================= PATH =================
    image_data = os.path.join('media', 'garbage_classification')

    # ================= DATASET =================
    batch_size = 128
    img_size = (224, 224)
    validation_split = 0.2

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        image_data,
        validation_split=validation_split,
        subset="training",
        seed=50,
        image_size=img_size,
        batch_size=batch_size
    )

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        image_data,
        validation_split=validation_split,
        subset="validation",
        seed=50,
        image_size=img_size,
        batch_size=batch_size
    )

    class_names = train_ds.class_names
    num_classes = len(class_names)

    # ================= MODEL =================
    base_model = tf.keras.applications.EfficientNetV2B1(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False

    model = keras.Sequential([
        base_model,
        keras.layers.GlobalAveragePooling2D(),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # ================= CALLBACKS =================
    checkpoint = ModelCheckpoint(
        "Garbage_model.h5",
        monitor='val_accuracy',
        save_best_only=True
    )

    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True
    )

    # ================= TRAIN =================
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=1,   # change to more epochs if needed
        callbacks=[checkpoint, early_stopping]
    )

    # ================= EVALUATE =================
    loss, acc = model.evaluate(val_ds)

    # ================= HISTORY DATA =================
    hist_df = pd.DataFrame(history.history)

    train_loss = hist_df['loss'].tolist()
    val_loss = hist_df['val_loss'].tolist()
    train_accuracy = hist_df['accuracy'].tolist()
    val_accuracy = hist_df['val_accuracy'].tolist()

    # ================= RESPONSE =================
    return render(request, 'users/training.html', {
        'train_loss': train_loss,
        'val_loss': val_loss,
        'train_accuracy': train_accuracy,
        'val_accuracy': val_accuracy,
        'accuracy': round(acc * 100, 2),
        'classes': class_names
    })


# from django.shortcuts import render
# import os
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# import tensorflow as tf
# from PIL import Image

# # Load the model globally to avoid loading it every time the view is called
# model_path = os.path.join(settings.MEDIA_ROOT, 'Garbage_model.h5')
# model = load_model(model_path)

# class_names = ['battery', 'biological', 'brown-glass', 'cardboard', 'clothes', 'green-glass', 'metal', 'paper', 'plastic', 'shoes', 'trash', 'white-glass']  # Replace with your actual class names


# def predict_Garbage(request):
#     if request.method == 'POST' and request.FILES['file']:
#         image_file = request.FILES['file']
#         fs = FileSystemStorage(location="media/garbage_classification/test_data")
#         filename = fs.save(image_file.name, image_file)
#         uploaded_file_url = "/media/garbage_classification/test_data/" + filename
#         path = os.path.join(settings.MEDIA_ROOT, 'garbage_classification/test_data', filename)

#         # Preprocess the image
#         img_height, img_width = 224, 224
#         img = image.load_img(path, target_size=(img_height, img_width))
#         img_array = image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)
#         img_array = tf.keras.applications.vgg16.preprocess_input(img_array)

#         # Make prediction
#         predictions = model.predict(img_array)
#         predicted_class = np.argmax(predictions, axis=1)[0]
#         predicted_label = class_names[predicted_class]

#         result = f"The uploaded image is predicted to be: {predicted_label}"

#         # Display the image
#         img = mpimg.imread(path)
#         plt.figure()
#         plt.imshow(img)
#         plt.title(f'Prediction: {predicted_label}')
#         plt.axis('off')
#         prediction_image_path = os.path.join(settings.MEDIA_ROOT, 'prediction_result.png')
#         plt.savefig(prediction_image_path, bbox_inches='tight')
#         plt.close()
#         prediction_image_url = "/media/prediction_result.png"

#         return render(request, "users/UploadForm.html", {'path': uploaded_file_url, 'result': result, 'prediction_image_url': prediction_image_url})
#     return render(request, "users/UploadForm.html")


# from django.shortcuts import render
# import os
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# import tensorflow as tf
# from PIL import Image

# # Load the model globally to avoid loading it every time the view is called
# model_path = os.path.join(settings.MEDIA_ROOT, 'Garbage_model.h5')
# model = load_model(model_path)

# class_names = ['battery', 'biological', 'brown-glass', 'cardboard', 'clothes', 'green-glass', 'metal', 'paper', 'plastic', 'shoes', 'trash', 'white-glass']

# # Define categories for trash and recyclable items
# recycle_items = {'brown-glass', 'cardboard', 'green-glass', 'metal', 'paper', 'plastic', 'white-glass'}
# trash_items = {'battery', 'biological', 'clothes', 'shoes', 'trash'}

# def predict_Garbage(request):
#     if request.method == 'POST' and request.FILES['file']:
#         image_file = request.FILES['file']
#         fs = FileSystemStorage(location="media/garbage_classification/test_data")
#         filename = fs.save(image_file.name, image_file)
#         uploaded_file_url = "/media/garbage_classification/test_data/" + filename
#         path = os.path.join(settings.MEDIA_ROOT, 'garbage_classification/test_data', filename)

#         # Preprocess the image
#         img_height, img_width = 224, 224
#         img = image.load_img(path, target_size=(img_height, img_width))
#         img_array = image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)
#         img_array = tf.keras.applications.vgg16.preprocess_input(img_array)

#         # Make prediction
#         predictions = model.predict(img_array)
#         predicted_class = np.argmax(predictions, axis=1)[0]
#         predicted_label = class_names[predicted_class]

#         # Determine if the item is trash or recyclable
#         category = "Recyclable" if predicted_label in recycle_items else "Trash"
#         result = f"The uploaded image is predicted to be: {predicted_label} ({category})"

#         # Display the image
#         img = mpimg.imread(path)
#         plt.figure()
#         plt.imshow(img)
#         plt.title(f'Prediction: {predicted_label} ({category})')
#         plt.axis('off')
#         prediction_image_path = os.path.join(settings.MEDIA_ROOT, 'prediction_result.png')
#         plt.savefig(prediction_image_path, bbox_inches='tight')
#         plt.close()
#         prediction_image_url = "/media/prediction_result.png"

#         return render(request, "users/UploadForm.html", {'path': uploaded_file_url, 'result': result, 'prediction_image_url': prediction_image_url})
    
#     return render(request, "users/UploadForm.html")


from django.shortcuts import render
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
from PIL import Image

# Load the model globally to avoid loading it every time the view is called
model_path = os.path.join(settings.MEDIA_ROOT, 'Garbage_model.h5')
model = load_model(model_path)

class_names = ['battery', 'biological', 'brown-glass', 'cardboard', 'clothes', 'green-glass', 'metal', 'paper', 'plastic', 'shoes', 'trash', 'white-glass']

# Define categories for trash and recyclable items
recycle_items = {'brown-glass', 'cardboard', 'green-glass', 'metal', 'paper', 'plastic', 'white-glass'}
trash_items = {'battery', 'biological', 'clothes', 'shoes', 'trash'}

def predict_Garbage(request):
    if request.method == 'POST' and request.FILES['file']:
        image_file = request.FILES['file']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "garbage_classification/test_data"))
        filename = fs.save(image_file.name, image_file)
        uploaded_file_url = f"/media/garbage_classification/test_data/{filename}"
        path = os.path.join(settings.MEDIA_ROOT, 'garbage_classification/test_data', filename)

        # Preprocess the image
        img_height, img_width = 224, 224
        img = image.load_img(path, target_size=(img_height, img_width))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.vgg16.preprocess_input(img_array)

        # Make prediction
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]
        confidence = np.max(predictions)  # Get the highest probability
        threshold = 0.7  # Set confidence threshold

        if confidence < threshold:
            predicted_label = "Cannot classify"
            category = "Unknown"
        else:
            predicted_label = class_names[predicted_class]
            category = "Recyclable" if predicted_label in recycle_items else "Trash"
        
        result = f"The uploaded image is classified as: {predicted_label} ({category})"

        # Display the image
        img = mpimg.imread(path)
        plt.figure()
        plt.imshow(img)
        plt.title(f'Prediction: {predicted_label} ({category})')
        plt.axis('off')
        prediction_image_path = os.path.join(settings.MEDIA_ROOT, 'prediction_result.png')
        plt.savefig(prediction_image_path, bbox_inches='tight')
        plt.close()
        prediction_image_url = "/media/prediction_result.png"

        return render(request, "users/UploadForm.html", {
            'path': uploaded_file_url,
            'result': result,
            'prediction_image_url': prediction_image_url
        })
    
    return render(request, "users/UploadForm.html")