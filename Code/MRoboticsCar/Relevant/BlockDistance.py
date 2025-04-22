import cv2
import numpy as np
from picamera2 import Picamera2
import time

# Funktion zur Berechnung der Entfernung
def berechne_entfernung(hohe_im_bild, mittlere_brennweite, echte_hoehe=100):
    """
    Berechnet die Entfernung basierend auf der Blockh�he im Bild und der mittleren Brennweite.
    
    Parameters:
    hohe_im_bild (int): H�he des Blocks im Bild (in Pixel).
    mittlere_brennweite (float): Mittlere Brennweite (in Pixel).
    echte_hoehe (float): Echte H�he des Blocks (in mm), Standardwert ist 100 mm.
    
    Returns:
    float: Berechnete Entfernung (in mm).
    """
    if hohe_im_bild == 0:  # Verhindert Division durch null
        return 0
    entfernung = (echte_hoehe * mittlere_brennweite) / hohe_im_bild
    return entfernung

# Initialisiere die Kamera
picam2 = Picamera2()
picam2.start()

# Mittlere Brennweite, die zuvor berechnet wurde
mittlere_brennweite = 299.0  # Beispielwert, ersetze durch den aktuellen Wert

# Farbbereiche f�r Rot und Gr�n im HSV-Raum
red_lower = np.array([125, 100, 100])
red_upper = np.array([140, 255, 255])

green_lower = np.array([25, 100, 100])
green_upper = np.array([60, 255, 255])

# Funktion zur Blockerkennung im Bild auf Basis von Farbe
def erkenne_block(im_bild):
    """
    Erkennen des Blocks im Bild und Ermitteln der H�he des Blocks in Pixel.
    Nutzt Farbfilterung im HSV-Raum anstelle von Graustufen.
    
    Parameters:
    im_bild (numpy array): Das Bild als NumPy Array.
    
    Returns:
    int: H�he des Blocks im Bild (in Pixel).
    """
    # Konvertiere das Bild in den HSV-Farbraum
    hsv = cv2.cvtColor(im_bild, cv2.COLOR_BGR2HSV)

    # Erstelle Masken f�r Rot und Gr�n
    maske_rot = cv2.inRange(hsv, red_lower, red_upper)
    maske_gruen = cv2.inRange(hsv, green_lower, green_upper)

    # Kombiniere beide Masken
    maske = cv2.bitwise_or(maske_rot, maske_gruen)

    # Finde die Konturen des Blockes
    konturen, _ = cv2.findContours(maske, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if konturen:
        # Finde die gr��te Kontur
        gr�sste_kontur = max(konturen, key=cv2.contourArea)
        
        # Bestimme die Begrenzungsrechteck des Blocks
        x, y, w, h = cv2.boundingRect(gr�sste_kontur)
        
        return h  # H�he des Blocks im Bild (in Pixel)
    
    return 0  # Kein Block erkannt

# Funktion zur Bestimmung der Farbe des Blocks
def bestimme_farbe(im_bild):
    """
    Bestimmt die Farbe des erkannten Blocks im Bild.
    
    Parameters:
    im_bild (numpy array): Das Bild als NumPy Array.
    
    Returns:
    str: Die erkannte Farbe des Blocks ("rot", "gr�n" oder "keine").
    """
    hsv = cv2.cvtColor(im_bild, cv2.COLOR_BGR2HSV)

    # Erstelle Masken f�r Rot und Gr�n
    maske_rot = cv2.inRange(hsv, red_lower, red_upper)
    maske_gruen = cv2.inRange(hsv, green_lower, green_upper)

    # Z�hle die Pixel in jeder Maske
    rot_pixel = np.count_nonzero(maske_rot)
    gruen_pixel = np.count_nonzero(maske_gruen)

    if rot_pixel > gruen_pixel:
        return "rot"
    elif gruen_pixel > rot_pixel:
        return "gr�n"
    else:
        return "keine"  # Keine eindeutige Farbe erkannt

# Echtzeit-Bildverarbeitung und Entfernungsberechnung
try:
    while True:
        # Nimm ein Bild von der Kamera
        bild = picam2.capture_array()

        # Erkenne die H�he des Blocks im Bild
        blockh�he_im_bild = erkenne_block(bild)

        if blockh�he_im_bild > 0:
            # Bestimme die Farbe des Blocks
            farbe = bestimme_farbe(bild)
            print(f"Block erkannt! Farbe: {farbe}, H�he im Bild: {blockh�he_im_bild} Pixel")

            # Berechne die Entfernung
            entfernung = berechne_entfernung(blockh�he_im_bild, mittlere_brennweite)
            print(f"Entfernung: {entfernung:.2f} mm")
        else:
            print("Kein Block erkannt")
        
        # Kurze Pause, um CPU zu schonen (optional)
        time.sleep(0.1)

except KeyboardInterrupt:
    # Stoppt die Kamera bei einem Abbruch
    picam2.stop()
    print("Echtzeit-Entfernungsberechnung gestoppt.")