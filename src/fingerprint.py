#ANTES DE EJECUTAR, HACER "cd src" EN CASO DE ESTAR EN EL DIRECTORIO "Chatbot"
import os
import cv2

sample = cv2.imread("SOCOFing/Altered/Altered-Hard/30__F_Right_thumb_finger_Obl.BMP")

best_score = 0
filename = None
image = None
kp1, kp2, mp = None, None, None

for file in os.listdir("SOCOFing/Real"): #el [:1000] es un limitante para que solo busque los primeros 1000 ejemplos, quitar si queres buscar en todos  
    fingerprint_image = cv2.imread(os.path.join("SOCOFing/Real", file))  

    if sample is None or fingerprint_image is None:
        print(f"Error: Could not read {file}")
        continue

    sift = cv2.SIFT_create()

    keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_image, None)

    matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10}, {}).knnMatch(descriptors_1, descriptors_2, k=2)
    
    match_points = []

    for p, q in matches:
        if p.distance < 0.1 * q.distance:
            match_points.append(p)

    keypoints = min(len(keypoints_1), len(keypoints_2))  

    score = len(match_points) / keypoints * 100 if keypoints > 0 else 0  

    if score > best_score:
        best_score = score
        filename = file
        image = fingerprint_image
        kp1, kp2, mp = keypoints_1, keypoints_2, match_points

print("MEJOR COINCIDENCIA:", filename)
print("PUNTAJE:", best_score)

if image is not None and kp1 is not None and kp2 is not None and mp is not None:
    result = cv2.drawMatches(sample, kp1, image, kp2, mp, None)
    result = cv2.resize(result, None, fx=4, fy=4)
    cv2.imshow("Result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error: No se encontraron coincidencias con la huella introducida")
