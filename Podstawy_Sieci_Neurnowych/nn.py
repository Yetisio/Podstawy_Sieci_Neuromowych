from data import get_mnist
import numpy as np
import matplotlib.pyplot as plt
import cv2


"""
w = weights, b = bias, i = input, h = hidden, o = output, l = label
e.g. w_i_h = weights from input layer to hidden layer
"""
images, labels = get_mnist()
w_i_h = np.random.uniform(-0.5, 0.5, (20, 784))
w_h_o = np.random.uniform(-0.5, 0.5, (10, 20))
b_i_h = np.zeros((20, 1))
b_h_o = np.zeros((10, 1))

learn_rate = 0.01
nr_correct = 0
epochs = 3
for epoch in range(epochs):
    for img, l in zip(images, labels):
        img.shape += (1,)
        l.shape += (1,)
        # Forward propagation input -> hidden
        h_pre = b_i_h + w_i_h @ img
        h = 1 / (1 + np.exp(-h_pre))
        # Forward propagation hidden -> output
        o_pre = b_h_o + w_h_o @ h
        o = 1 / (1 + np.exp(-o_pre))

        # Cost / Error calculation
        e = 1 / len(o) * np.sum((o - l) ** 2, axis=0)
        nr_correct += int(np.argmax(o) == np.argmax(l))

        # Backpropagation output -> hidden (cost function derivative)
        delta_o = o - l
        w_h_o += -learn_rate * delta_o @ np.transpose(h)
        b_h_o += -learn_rate * delta_o
        # Backpropagation hidden -> input (activation function derivative)
        delta_h = np.transpose(w_h_o) @ delta_o * (h * (1 - h))
        w_i_h += -learn_rate * delta_h @ np.transpose(img)
        b_i_h += -learn_rate * delta_h

    # Show accuracy for this epoch
    print(f"Acc: {round((nr_correct / images.shape[0]) * 100, 2)}%")
    nr_correct = 0


def process_uploaded_image(image_path):
    img = cv2.imread(image_path, 0)  # Read image in grayscale
    resized_img = cv2.resize(img, (28, 28))  # Resize to 28x28 (MNIST image size)
    normalized_img = resized_img / 255.0  # Normalize pixel values (like the MNIST dataset)
    flattened_img = normalized_img.flatten()  # Flatten to match the input size
    return flattened_img

# Load a sample image for testing
uploaded_image_path = 'nr.jpg'  # Replace with your image path
uploaded_image = process_uploaded_image(uploaded_image_path)

# Forward propagation for the uploaded image
uploaded_image = uploaded_image.reshape(784, 1)  # Reshape for input compatibility

# Forward propagation input -> hidden
h_pre = b_i_h + w_i_h @ uploaded_image
h = 1 / (1 + np.exp(-h_pre))
# Forward propagation hidden -> output
o_pre = b_h_o + w_h_o @ h
o = 1 / (1 + np.exp(-o_pre))

# Display the results
plt.imshow(uploaded_image.reshape(28, 28), cmap="Greys")
plt.title(f"Predicted digit: {o.argmax()}")
plt.show()
