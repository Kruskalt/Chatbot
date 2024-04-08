import os
import shutil
import cv2

def copiar_archivo_a_carpeta(src_ruta_archivo):
    # Verificar si la ruta del archivo existe
    if not os.path.exists(src_ruta_archivo):
        raise FileNotFoundError(f"El archivo {src_ruta_archivo} no existe.")
    # Verificar si la carpeta de destino existe, si no, crearla
    if check_fingerprint(src_ruta_archivo):
        return False
    carpeta_destino = "src/SOCOFing/Real"
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    

    # Obtener el nombre del archivo
    nombre_archivo = os.path.basename(src_ruta_archivo)

    # Construir la ruta de destino
    ruta_destino_archivo = os.path.join(carpeta_destino, nombre_archivo)

    # Copiar el archivo a la carpeta de destino
    shutil.copyfile(src_ruta_archivo, ruta_destino_archivo)

    # Devolver la ruta de la copia
    return True


def load_sample_image(file_path):
    """
    Carga la imagen de muestra.

    Args:
        file_path (str): Ruta del archivo de imagen de muestra.

    Returns:
        numpy.ndarray: Imagen de muestra.
    """
    sample = cv2.imread(file_path)
    
    return sample

def load_fingerprint_images(directory):
    """
    Carga todas las imágenes de huellas dactilares de un directorio.

    Args:
        directory (str): Directorio que contiene las imágenes de huellas dactilares.

    Returns:
        list: Lista de imágenes de huellas dactilares.
    """
    fingerprint_images = []
    for file in os.listdir(directory):
        fingerprint_image = cv2.imread(os.path.join(directory, file))
        if fingerprint_image is not None:
            fingerprint_images.append(fingerprint_image)
        else:
            print(f"Error: No se pudo leer {file}")
    return fingerprint_images

def match_fingerprint(sample, fingerprint_images):
    """
    Encuentra la mejor coincidencia entre la imagen de muestra y las imágenes de huellas dactilares.

    Args:
        sample (numpy.ndarray): Imagen de muestra.
        fingerprint_images (list): Lista de imágenes de huellas dactilares.

    Returns:
        tuple: Mejor coincidencia (nombre de archivo, puntaje, imagen, keypoints_1, keypoints_2, match_points).
    """
    best_score = 0
    best_match = None

    sift = cv2.SIFT_create()
    keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)

    for fingerprint_image in fingerprint_images:
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
            best_match = (fingerprint_image, keypoints_1, keypoints_2, match_points)

    return best_match, best_score
def check_extension(user_input):
    if not(user_input.lower().endswith('.bmp')):
            return False
    return True
def check_fingerprint(user_input):
    
    
    sample = load_sample_image(user_input)
    
    fingerprint_images = load_fingerprint_images("src/SOCOFing/Real")
    best_match, best_score = match_fingerprint(sample, fingerprint_images)

    if best_match is not None:
        #filename = "MEJOR COINCIDENCIA: " + str(best_match[0])
        image = best_match[0]
        kp1, kp2, mp = best_match[1], best_match[2], best_match[3]
        puntaje = "PUNTAJE: ", best_score
        # Dibuja los resultados si se encontró una coincidencia
        """
        result = cv2.drawMatches(sample, kp1, image, kp2, mp, None)
        result = cv2.resize(result, None, fx=4, fy=4)
        cv2.imshow("Result", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        """
        return True
    else:
        return False

def main():
    resultado, puntaje = check_fingerprint("SOCOFing/Altered/1__M_Left_index_finger_CR.BMP")
    print(resultado)
    print(puntaje)

# if __name__ == "__main__":
#     main()
