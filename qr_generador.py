import qrcode
import os

def generar_qr(enlace, nombre_archivo):
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(enlace)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    
    carpeta_imagenes = "imagenes"
    if not os.path.exists(carpeta_imagenes):
        os.makedirs(carpeta_imagenes)
    
    
    ruta_archivo = os.path.join(carpeta_imagenes, nombre_archivo)
    img.save(ruta_archivo)

if __name__ == "__main__":
    enlace = "https://www.uts.edu.co/sitio/biblioteca/" #Cambie por el link deseado
    nombre_archivo = "biblioteca.png" #nombre deseado
    generar_qr(enlace, nombre_archivo)
    print(f"Código QR generado y guardado como {os.path.join('imagenes', nombre_archivo)}")
