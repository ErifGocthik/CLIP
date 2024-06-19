'''

async def render_images(user: str,
                        class_index: str,
                        images: List[str] = None,
                        ):
    # return {'user': user, 'images': images}

    images_list = []

    for image in images:
        img = image
        # img = keras.api.preprocessing.image.load_img(img)
        test_image = load_img(img, target_size=(224, 224))
        test_image = img_to_array(test_image)
        # test_image.shape
        # test_image = preprocess_input(test_image)
        # test_image = np.expand_dims(test_image, axis=0)
        # test_image = test_image.astype(np.float32).tobytes()
        prediction = nermodel.predict(test_image)
        prediction_class = np.argmax(prediction[0])

        if str(class_index) == str(prediction_class):
            images_list.append(image)
    images = images_list
    return images

'''