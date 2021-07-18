import service_drive
from googleapiclient.http import MediaFileUpload,MediaIoBaseDownload
import os,io,shutil


def verificacion_eleccion(numero:int) -> tuple:
    """ 
    Pre: Le ingreso el numero de opcion elegida por el usuario.
    Post: Imprimo un confirmacion de la eleccion del usuario
    """
    opcion_correcta = input(f"\nUsted a elegido la opcion {numero}. Esta seguro que desa continuar? (si/no): ")
    if opcion_correcta == "si" or opcion_correcta == "Si":
        correcta_eleccion = True
    else:
        print("\nMuy bien, eliga otra opcion:\n")
    return correcta_eleccion

def elecciones(eleccion:int,drive_service) -> str:
    """ 
    Pre: Recibe un numero.
    Post: En base al numero, decide que funcion ejecutar y retorna un str que indica si el usuario quiere cerrar el programa o no.
    """
    exit = "no"

    if eleccion == 1:
        correcta_eleccion = verificacion_eleccion(1)
        if correcta_eleccion:
            listar_archivos_drive(drive_service)
            print("\nMuy bien, que desea hacer a continuacion?\n")
    elif eleccion == 2:
        correcta_eleccion = verificacion_eleccion(2)  
        if correcta_eleccion:
            eleccion_crear_archivo_o_carpeta(drive_service)
            print("\nMuy bien, que desea hacer a continuacion?\n")
    elif eleccion == 3:
        correcta_eleccion = verificacion_eleccion(3)
        if correcta_eleccion:
            subir_archivo_drive(drive_service)
            print("\nMuy bien, que desea hacer a continuacion?\n")
    elif eleccion == 4:
        correcta_eleccion = verificacion_eleccion(4)
        if correcta_eleccion:
            descargar_archivo_drive(drive_service)
            print("\nMuy bien, que desea hacer a continuacion?\n")
    elif eleccion == 5:
        correcta_eleccion = verificacion_eleccion(5)
        if correcta_eleccion:
            #ejecutar funcion
            print("\nMuy bien, que desea hacer a continuacion?\n")
            pass
        pass
    elif eleccion == 6:
        correcta_eleccion = verificacion_eleccion(6)
        if correcta_eleccion:
            #ejecutar funcion
            print("\nMuy bien, que desea hacer a continuacion?\n")
            pass
        pass
    elif eleccion == 7:
        correcta_eleccion = verificacion_eleccion(7)
        if correcta_eleccion:
            #ejecutar funcion
            print("\nMuy bien, que desea hacer a continuacion?\n")
            pass
        pass
    elif eleccion == 8:
        exit = input("A decidido cerrar el programa, seguro que desea salir? (si/no): ")
    
    return exit

def menu(drive_service) -> None:
    """ 
    Pre: Recibe el servicio de google drive.
    Post: Printea las opciones del programa para que el usuario eliga una.
    """
    exit = "no"
    while exit != "si" and exit != "Si":
        eleccion = input(""" 
        1. Listar archivos de la carpeta actual.
        2. Crear un archivo/carpeta.
        3. Subir un archivo.
        4. Descragar un archivo.
        5. Sincronizar.
        6. Generar carpetas de una evaluacion.
        7. Actualizar entregas de alumnos via mail.
        8. Salir. 
        Que accion desea realizar?: """)
        eleccion = int(verificador_numero(eleccion))

        if eleccion == 1 or eleccion == 2 or eleccion == 3 or eleccion == 4 or eleccion == 5 or eleccion == 6 or eleccion == 7 or eleccion == 8:
            exit = elecciones(eleccion,drive_service)
        else: 
            print("Esa opcion no esta en el rango, por favor intente nuevamente.")

def verificador_numero(numero:str) -> int:
    """
    Pre: Le ingreso un numero.
    Post: Verifica que sea un numero, en el caso contrario lo solicita devuelta hasta que ingrese un valor valido.
    """
    while not numero.isnumeric():
            numero = input("Eso no es un numero, por favor vuelva a intentarlo: ")
    return numero

def eleccion_crear_archivo_o_carpeta(drive_service) -> None:
    """ 
    Pre: Recibe el servicoi de google drive.
    Post: El usuario elige que opcion quiere y se ejecuta la funcion correspondiente a esa accion.
    """
    decision = input("a)Crear una carpeta\nb)Crear un archivo.\nQue desea hacer?: ")
    while decision != "a" and decision != "b":
        print("\nEsa opcion no es valida, por favor intente nuevamente.\n")
        decision = input("a)Crear una carpeta\nb)Crear un archivo.\nQue desea hacer?: ")
    confirmacion = input(f"Usted eligio la opcion '{decision}', esta seguro que desea continuar? (si/no): ")
    if confirmacion == "si" or confirmacion == "Si":
        if decision == "a":
            crear_carpeta_drive(drive_service)
        if decision == "b":
            crear_archivo_drive(drive_service)

def listar_archivos_drive(drive_service)-> None: #ver como elegir la carpeta a mostrar
    """ 
    Pre: Recibe lo servicios de google drive.
    Post: Printea los archivos de la capeta especificada por el usuario.
    """
    
    results = drive_service.files().list(fields="nextPageToken, files(id, name)").execute()
    carpetas = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)',).execute()
    for file in carpetas.get('files', []):
        # Process change
        print('Found file: %s (%s)\n' % (file.get('name'), file.get('id')))

    items = results.get('files', [])
    if not items:
        print('\nNo files found.\n')
    else:
        print('\nArchivos:\n')
        for item in items:
            print(f"{item['name']} ({item['id']})\n")

def crear_carpeta_drive(drive_service)-> None: 
    """ 
    Pre: Recibe el servicio de drive.
    Post: Crea una carpeta en google drive y la almacena donde quiera el usuario.
    """
    nombre_carpeta = input("\nPor favor ingrese el nombre de la carpeta a crear: ")

    file_metadata = {
    'name': nombre_carpeta,
    'mimeType': 'application/vnd.google-apps.folder'
    }

    file = drive_service.files().create(body=file_metadata,
                                    fields='id').execute()
    file_id = file.get('id')

    ubicacion = input("\nDesea almacenar esta carpeta en su unidad principal? (si/no): ")

    if ubicacion == "si":
        folder_id = input("\nPor favor introduzca el id de la carpeta: ")
        mover_archivos_drive(drive_service,file_id,folder_id)
        print("\nSu carpeta fue creada con exito.\n")
    else:
        print("\nVamos a almacenarla en tu unidad principal.\n")

    print('\nFolder ID: %s\n' % file_id)

def crear_archivo_drive(drive_service)-> None:
    file_name = input("\nIngrese el nombre con la extension del archivo a crear: ")
    folder_id = input("\nIngrese el id de la carpeta en la cual se va a almacenar: ")

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(f'files/{file_name}',
                            resumable=True)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

    print('ID del archivo: %s' % file.get('id'))

def subir_archivo_drive(drive_service) -> None: 
    """ 
    Pre: Recibe los servicios de google drive.
    Post: Le pregunta al usuario que archivo desea subir al drive y lo sube.
    """
    nombre_archivo = input("\nUsted a decidido subir un archivo nuevo. Por favor ingrese el nombre del archivo y la extension: ")
    folder_id = input("\nPor favor introduzca el id de la carpeta a la cual quiere subir este archivo: ")

    file_metadata = {'name': nombre_archivo}
    media = MediaFileUpload(nombre_archivo)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    file_id = file.get('id')

    mover_archivos_drive(drive_service,file_id,folder_id)
    print('\nID del archivo: %s\n' % file_id)

def descargar_archivo_drive(drive_service) -> None: 
    """
    Pre: Recibo el servico de google drive API.
    Post: Descarga el archivo solicitado por el usuario.
    """
    file_id = input("\nIngrese el id del archivo a descargar: ")
    file_name = input("\nIngrese el nombre con la extension del archivo a descargar: ")
    file_path = input("\nIngrese la ruta en la cual quiere descargar el archivo: ")

    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False

    while done is False:
        status, done = downloader.next_chunk()
        print("Descarga %d%%." % int(status.progress() * 100))

    with io.open(file_name,'wb') as f:
        fh.seek(0)
        f.write(fh.read())
    
    shutil.move(file_name, file_path) #mueve el archivo descargado al directorio que pidio el usuario

def buscar_archivos_drive(drive_service) -> None:
    query = "name contains 'holaa'"
    results = drive_service.files().list(fields="nextPageToken, files(id, name)",q=query).execute() #ahi me devuelve todos los archivos que tengan la palabra hola
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")

def mover_archivos_drive(drive_service,file_id,folder_id) -> None: 
    """ 
    Pre: Recibe el Id del archivo a mover y el Id de la carpeta a la cual quiere mover el archivo.
    Post: Mueve el archivo hacia la carpeta elegida por el usuario.
    """
    # Retrieve the existing parents to remove
    file = drive_service.files().get(fileId=file_id,
                                    fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    # Move the file to the new folder
    file = drive_service.files().update(fileId=file_id,
                                        addParents=folder_id,
                                        removeParents=previous_parents,
                                        fields='id, parents').execute()

def main()-> None:
    drive_service = service_drive.obtener_servicio()
    print("\nHola! Bienvenidos a nuestro servicio de google drive y gmail.\n")
    menu(drive_service)
    
    print("Muchas gracias por utilizar nuestro programa!")

if __name__ == '__main__':
    main()