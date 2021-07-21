import service_drive
from googleapiclient.http import MediaFileUpload,MediaIoBaseDownload
import os,io,shutil
import service_gmail

def verificacion_eleccion(numero:int) -> tuple:
    """ 
    Pre: Le ingreso el numero de opcion elegida por el usuario.
    Post: Imprimo un confirmacion de la eleccion del usuario
    """
    correcta_eleccion = False
    opcion_correcta = input(f"\nUsted a elegido la opcion {numero}. Esta seguro que desa continuar? (si/no): ")
    if opcion_correcta == "si" or opcion_correcta == "Si":
        correcta_eleccion = True
    else:
        print("\nMuy bien, eliga otra opcion:\n")
    return correcta_eleccion

def verificador_decision(decision:str)-> tuple:
    """ 
    Pre: Recibe si el usuario decidio continuar o no.
    Post: Retorna una variable que define si continua o no en base a lo que haya elegiddo el usuario.
    """
    if decision != "si":
        correcta_eleccion = False
        print("\nMuy bien, que desea hacer a continuacion?\n")
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
            file_name = input("\nUsted a decidido subir un archivo nuevo. Por favor ingrese el nombre del archivo y la extension: ")
            folder_id = input("\nPor favor introduzca el id de la carpeta a la cual quiere subir este archivo: ")
            subir_archivo_drive(drive_service,file_name,folder_id)
            decision = input("Desea seguir decargando archivos?: (si/no): ")
            correcta_eleccion = verificador_decision(decision)
    elif eleccion == 4:
        correcta_eleccion = verificacion_eleccion(4)
        while correcta_eleccion:
            file_id = input("\nIngrese el id del archivo a descargar: ")
            file_name = input("\nIngrese el nombre con la extension del archivo a descargar: ")
            file_path = input("\nIngrese la ruta en la cual quiere descargar el archivo: ")
            descargar_archivo_drive(drive_service,file_id,file_name,file_path)
            decision = input("Desea seguir decargando archivos?: (si/no): ")
            correcta_eleccion = verificador_decision(decision)
    elif eleccion == 5:
        correcta_eleccion = verificacion_eleccion(5)
        while correcta_eleccion:
            #ejecutar funcion
            decision = input("Desea seguir decargando archivos?: (si/no): ")
            correcta_eleccion = verificador_decision(decision)
            pass
        pass
    elif eleccion == 6:
        correcta_eleccion = verificacion_eleccion(6)
        while correcta_eleccion:
            #ejecutar funcion
            decision = input("Desea seguir decargando archivos?: (si/no): ") #cambiar por la funcion
            correcta_eleccion = verificador_decision(decision)
            pass
        pass
    elif eleccion == 7:
        correcta_eleccion = verificacion_eleccion(7)
        while correcta_eleccion:
            #ejecutar funcion
            decision = input("Desea seguir decargando archivos?: (si/no): ")#cambiar por la funcion
            correcta_eleccion = verificador_decision(decision)
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
        while decision == "a":
            nombre_carpeta = input("\nPor favor ingrese el nombre de la carpeta a crear: ")
            crear_carpeta_drive(drive_service,nombre_carpeta)
            repeticion = input("Desea crear otra carpeta? (si/no) ")
            if repeticion != "si":
                decision = repeticion
        if decision == "b":
            file_name = input("\nIngrese el nombre con la extension del archivo a crear: ")
            folder_id = input("\nIngrese el id de la carpeta en la cual se va a almacenar: ")
            crear_archivo_drive(drive_service,file_name,folder_id)
            repeticion = input("Desea crear otro archivo? (si/no) ")
            if repeticion != "si":
                decision = repeticion
    
def listar_archivos_drive(drive_service)-> None: 
    """ 
    Pre: Recibe lo servicios de google drive.
    Post: Printea los archivos de la capeta especificada por el usuario.
    """
    listar = True
    archivos = drive_service.files().list(fields="nextPageToken, files(id, name, mimeType)").execute()

    while listar:
        ids_carpetas,ids_archivos = separador_archivos_carpetas(archivos)
        imprimir_carpetas(ids_carpetas)
        imprimir_archivos(ids_archivos)

        decision,carpetas = verificador_de_carpetas(ids_carpetas)
        
        if decision == "a":
            carpeta = input("Introduci el numero de la carpeta: ")
            carpeta = conversor_int(carpeta)
            id_carpeta = ids_carpetas[carpeta-1][0]
            archivos = drive_service.files().list(q= f"'{id_carpeta}' in parents",fields="nextPageToken, files(id, name, mimeType)").execute()
        elif decision == "b":
            obtener_ids(carpetas,ids_archivos,ids_carpetas)
            listar = False
        else:
            print("\nUsted eligio vover al menu principal.\n")
            listar = False

def conversor_int(numero:str) -> int:
    """ 
    Pre: Recibo un str.
    Post: Si es un numero lo transformo a int, en caso contario le pido devuelta un numero.
    """
    es_numero = False

    while es_numero == False:
        if numero.isnumeric():
            numero = int(numero) 
            es_numero = True
        else:
            numero = input("El valor ingresado no es un numero, por favor intente nuevamente: ")
    return numero

def obtener_ids(carpeta:bool,ids_archivos:list,ids_carpetas:list) -> None:
    """ 
    Pre: Recibe las listas de archivos y el booleano carpeta.
    Post: Le pregunta al usuario que id quiere obtener (en caso de que no haya carpetas asume que es de archivos) y lo imprime.
    """
    if carpeta: #si hay carpetas te pregunta si queres obtener el id, sino lo evita y asume que queres el id de un archivo
        decision_2 = input("\nDesea obtener el id de un archivo o carpeta? (a/b): ")
    else:
        decision_2 = "a"

    if decision_2 == "a":
        num_archivo = input("\nIngrese el numero del archivo que desea obtener el id: ")
        num_archivo = conversor_int(num_archivo)
        print(f"\nEl id del archivo {num_archivo} es: {ids_archivos[num_archivo-1][0]}")
    else:
        num_carpeta = input("\nIngrese el numero de carpeta que desea obtener el id: ")
        num_carpeta = conversor_int(num_carpeta)
        print(f"\nEl id de la carpeta {num_carpeta} es: {ids_carpetas[num_carpeta-1][0]}")

def separador_archivos_carpetas(archivos)-> list:
    """ 
    Pre: Recibo un conjunto de archivos.
    Post: Separo esos dos conjuntos en archivos y carpetas y los almaceno en las listas creadas.
    """
    ids_carpetas = list()
    ids_archivos = list()
    numero = 0
    for file in archivos.get('files', []): 
        numero += 1
        if file.get("mimeType") == "application/vnd.google-apps.folder":
            ids_carpetas.append((file.get('id'),file.get('name')))
        else: 
            ids_archivos.append((file.get('id'),file.get('name')))
    return ids_carpetas,ids_archivos

def verificador_de_carpetas(ids_carpetas:list)-> tuple:
    """ 
    Pre: Recibe una lista de carpetas.
    Post: Verifica que esa lista tenga contenido y devuelve un str que sera usado en el programa principal.
    """
    carpetas = True
    if not ids_carpetas:
        decision = input("Desea obtener algun id o volver al menu principal? (a/b): ")
        if decision == "a":
            decision = "b"
            carpetas = False
        elif decision == "b":
            decision = "c"
    else:
        decision = input("Desea entrar en una carpeta, obtener algun id o volver al menu principal? (a/b/c): ")
    return decision,carpetas

def imprimir_carpetas(ids_carpetas:list)-> None:
    """ 
    Pre: Recibe una lista de carpetas.
    Post: Imprime esa lista separada por un numero inicial.
    """
    numero = 0
    for file in ids_carpetas: #Imprime las carpetas
        numero += 1
        print(f'\nCarpeta Nº {numero}: {ids_carpetas[numero-1][1]}')

def imprimir_archivos(ids_archivos:list)-> None:
    """ 
    Pre: Recibe una lista de archivos.
    Post: Imprime esa lista separada por un numero inicial.
    """
    numero = 0
    for file in ids_archivos: 
        numero += 1
        print(f'\nArchivo Nº {numero}: {ids_archivos[numero-1][1]}')

def crear_carpeta_drive(drive_service,nombre_carpeta:str)-> None: 
    """ 
    Pre: Recibe el servicio de drive.
    Post: Crea una carpeta en google drive y la almacena donde quiera el usuario.
    """
    file_metadata = {
    'name': nombre_carpeta,
    'mimeType': 'application/vnd.google-apps.folder'
    }

    file = drive_service.files().create(body=file_metadata,
                                    fields='id').execute()
    file_id = file.get('id')

    ubicacion = input("\nDesea almacenar esta carpeta en su unidad principal? (si/no): ")

    if ubicacion == "no":
        folder_id = input("\nPor favor introduzca el id de la carpeta: ")
        mover_archivos_drive(drive_service,file_id,folder_id)
        print("\nSu carpeta fue creada con exito.\n")
    else:
        print("\nVamos a almacenarla en tu unidad principal.\n")

    print('\nFolder ID: %s\n' % file_id)

def crear_archivo_drive(drive_service,file_name:str,folder_id:str)-> None:
    """ 
    Pre: Recibe el servicio de drive, el nombre y la carpeta del archivo a almacenar.
    Post: Crea un archivo en la carpaeta que selecciono el usuario.
    """

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

def subir_archivo_drive(drive_service,file_name:str,folder_id:str) -> None: 
    """ 
    Pre: Recibe los servicios de google drive, el n ombre del archivo y el id de la carpeta.
    Post: Recibe un archivo y lo sube a la carpeta deseada por el usuraio.
    """

    file_metadata = {'name': file_name} #ver como obtener la fecha de modificacion de un archivo local. Si no coincide con la subida, se vuelve a subir.
    media = MediaFileUpload(file_name)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    file_id = file.get('id')

    mover_archivos_drive(drive_service,file_id,folder_id)
    print('\nID del archivo: %s\n' % file_id)

def descargar_archivo_drive(drive_service,file_id:str,file_name:str,file_path:str) -> None: 
    """
    Pre: Recibo el servico de google drive API, el nombre del archivo, su ID y la carpeta en la cual lo quiere descargar.
    Post: Descarga el archivo solicitado por el usuario.
    """
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

def buscar_archivos_drive(drive_service,palabra_buscador:str) -> None:
    """ 
    Pre: Recibe el servicio de google drive, y la palabra a buscar.
    Post: Imprime por pantalla los resultados encontrados con su correspondiente id.
    """
    query = f"name contains '{palabra_buscador}'"

    results = drive_service.files().list(fields="nextPageToken, files(id, name)",q=query).execute() #ahi me devuelve todos los archivos que tengan la palabra hola
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")

def mover_archivos_drive(drive_service,file_id:str,folder_id:str) -> None: 
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
    drive_service = service_drive.obtener_servicio() #este es el servicio de drive
    gmail_service = service_gmail.obtener_servicio() #este es el servicio de gmail
    print("\nHola! Bienvenidos a nuestro servicio de google drive y gmail.\n")
    menu(drive_service)
    
    print("Muchas gracias por utilizar nuestro programa!")

if __name__ == '__main__':
    main()