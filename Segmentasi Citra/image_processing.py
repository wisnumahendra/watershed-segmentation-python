import cv2
import numpy as np

def apply_watershed(image):
    if image is None:
        print("Gambar tidak ditemukan.")
        return
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Pra-pemrosesan citra untuk mempersiapkan pemrosesan Watershed
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # Marker labels untuk Watershed
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    
    # Aplikasi Watershed
    markers = cv2.watershed(image, markers)

    # Menetapkan warna untuk setiap label yang dihasilkan
    colored_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    unique_markers = np.unique(markers)
    unique_markers = unique_markers[1:]  # Skip background label (-1)
    colors = np.random.randint(0, 255, size=(len(unique_markers), 3))  # Warna acak untuk setiap label

    for i, marker in enumerate(unique_markers):
        colored_image[markers == marker] = colors[i]

    return colored_image
