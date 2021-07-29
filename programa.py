from email import message
from email.message import Message
from typing import List, Tuple
from googleapiclient.discovery import Resource
from random import randint
import service_drive
from googleapiclient.http import MediaFileUpload,MediaIoBaseDownload
import os,io,shutil,tempfile,time,sys
import service_gmail
import csv
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
    correcta_eleccion = True
    if decision != "si" and decision != "Si":
        correcta_eleccion = False
        print("\nMuy bien, que desea hacer a continuacion?\n")
    return correcta_eleccion

def elecciones(eleccion:int,drive_service:Resource, gmail_service:Resource) -> str: #modularizarr
    """ 
    Pre: Recibe un numero.
    Post: En base al numero, decide que funcion ejecutar y retorna un str que indica si el usuario quiere cerrar el programa o no.
    """
    exit = "no"

    if eleccion == 1:
        correcta_eleccion = verificacion_eleccion(1)
        if correcta_eleccion:
            print('\nEstos son los archivos locales: \n')
            listar_archivos_local()
            print('\nEstos son los archivos de drive: \n')
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
            file_path = input("Por favor ingrese la ruta del archivo: ")
            file_name = input("\nUsted a decidido subir un archivo nuevo. Por favor ingrese el nombre del archivo y la extension: ")
            folder_id = input("\nPor favor introduzca el id de la carpeta a la cual quiere subir este archivo: ")
            subir_archivo_drive(drive_service,file_name,folder_id,file_path)
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
            sincronizacion_drive(drive_service)
            decision = input("Desea sincronizar algo mas?: (si/no): ")
            correcta_eleccion = verificador_decision(decision)
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

def menu(drive_service:Resource, gmail_service:Resource) -> None:
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
        4. Descargar un archivo.
        5. Sincronizar.
        6. Generar carpetas de una evaluacion.
        7. Actualizar entregas de alumnos via mail.
        8. Salir. 
        Que accion desea realizar?: """)
        eleccion = int(verificador_numero(eleccion))

        if eleccion == 1 or eleccion == 2 or eleccion == 3 or eleccion == 4 or eleccion == 5 or eleccion == 6 or eleccion == 7 or eleccion == 8:
            exit = elecciones(eleccion,drive_service, gmail_service)
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

def eleccion_crear_archivo_o_carpeta(drive_service:Resource) -> None:
    """ 
    Pre: Recibe el servicoi de google drive.
    Post: El usuario elige que opcion quiere y se ejecuta la funcion correspondiente a esa accion.
    """
    decision = input("a)Crear un archivo.\nb)Crear una carpeta.\nQue desea hacer?: ")

    while decision != "a" and decision != "b":
        print("\nEsa opcion no es valida, por favor intente nuevamente.\n")
        decision = input("a)Crear un archivo.\nb)Crear una carpeta.\nQue desea hacer?: ")
    confirmacion = input(f"Usted eligio la opcion '{decision}', esta seguro que desea continuar? (si/no): ")

    if confirmacion == "si" or confirmacion == "Si":
        while decision == "b":
            nombre_carpeta = input("\nPor favor ingrese el nombre de la carpeta a crear: ")
            file_path = input("\nIngrese el directorio donde se va a almacenar la carpeta creada: ")
            crear_carpeta_drive(drive_service,nombre_carpeta)
            crear_carpeta_local(nombre_carpeta, file_path)
            repeticion = input("Desea crear otra carpeta? (si/no) ")
            if repeticion != "si":
                decision = repeticion
        while decision == "a":
            file_name = input("\nIngrese el nombre con la extension del archivo a crear: ")
            file_path = input("\nIngrese el directorio donde se va a almacenar el archivo creado: ")
            print('\nVamos a navegar por sus carpetas de Drive. Al llegar a la carpeta en la que quiere almacenar el archivo, seleccione la opcion obtener ID.\n')
            folder_id = navegacion_carpetas_drive(drive_service)
            crear_archivo_local(file_name)
            subir_archivo_drive(drive_service,file_name,folder_id,file_path)
            repeticion = input("Desea crear otro archivo? (si/no) ")
            if repeticion != "si":
                decision = repeticion
    
def listar_archivos_drive(drive_service:Resource)-> None:
    """ 
    Pre: Recibe lo servicios de google drive.
    Post: Printea los archivos de la capeta especificada por el usuario.
    """
    listar = True
    archivos = drive_service.files().list(q= f"'Root' in parents",fields="nextPageToken, files(id, name, mimeType)").execute()

    while listar:
        ids_carpetas,ids_archivos = separador_archivos_carpetas(archivos)
        imprimir_carpetas(ids_carpetas)
        imprimir_archivos_drive(ids_archivos)

        decision,carpetas = verificador_de_carpetas(ids_carpetas)
        
        if decision == "a":
            carpeta = input("Introduci el numero de la carpeta: ")
            carpeta = conversor_int(carpeta)
            id_carpeta = ids_carpetas[carpeta-1][0]
            archivos = drive_service.files().list(q= f"'{id_carpeta}' in parents",fields="nextPageToken, files(id, name, mimeType)").execute()
        elif decision == "b":
            id = obtener_ids(carpetas,ids_archivos,ids_carpetas)
            listar = False
        else:
            print("\nUsted eligio vover al menu principal.\n")
            listar = False

def listar_archivos_local() -> None:
    """ 
    Pre:
    Post: Printea los archivos de la capeta especificada por el usuario.
    """
    lista_de_archivos = os.listdir(os.path.abspath(os.getcwd()))

    imprimir_archivos_local(lista_de_archivos)

def crear_carpeta_local(nombre_carpeta:str, file_path:str) -> None: 
    """ 
    Pre: Recibe el nombre de la carpeta y el path.
    Post: Crea la carpeta en el directorio que el usuario elige.
    """
    try:
        carpeta_nueva = os.mkdir(nombre_carpeta)
        shutil.move(carpeta_nueva, file_path)
        print('Creaste la carpeta.')
    except FileNotFoundError:
        print('\nEl directorio ingresado es inexistente, error creando la carpeta\n')
    except:
        print('\nError creando la carpeta\n')

def crear_archivo_local(file_name:str) -> None: # Ver esto
    """ 
    Pre: Recibe el nombre del archivo.
    Post: Crea un archivo.
    """
    # nuevo_archivo = os.mknod(input("Ingrese el nombre del nuevo archivo con su extendion: "))
    filename = file_name[-4:]
    while filename != ".txt" and filename != ".csv" and filename != "json":
        print("\nLa extension del archivo no esta permitida. Los formatos permitidos son .txt, .json o .csv.\n")
        file_name = input("\nIngrese el nombre del archivo junto su extension: ")
        filename = file_name[-4:] 
    try:
        open(file_name, 'a').close()
    except OSError:
        print('Error creando el archivo.')
    else:
        print('Archivo creado.')

def navegacion_carpetas_drive(drive_service:Resource) -> str:
    """ 
    Pre: Recibe lo servicios de google drive.
    Post: Permite la navegacion por carpetas de drive.
    """
    listar = True
    archivos = drive_service.files().list(fields="nextPageToken, files(id, name, mimeType)").execute()

    while listar:
        ids_carpetas,ids_archivos = separador_archivos_carpetas(archivos)
        imprimir_carpetas(ids_carpetas)

        decision,carpetas = verificador_de_carpetas(ids_carpetas)
        
        if decision == "a":
            carpeta = input("Introduci el numero de la carpeta: ")
            carpeta = conversor_int(carpeta)
            id_carpeta = ids_carpetas[carpeta-1][0]
            archivos = drive_service.files().list(q= f"'{id_carpeta}' in parents",fields="nextPageToken, files(id, name, mimeType)").execute()
        elif decision == "b":
            id_carpeta = obtener_id_carpeta(ids_carpetas)
            listar = False
        else:
            print("\nUsted eligió vover al menu principal.\n")
            listar = False
    return id_carpeta

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

def obtener_ids(carpeta:bool,ids_archivos:list,ids_carpetas:list) -> str:
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
        id_carpeta = obtener_id_carpeta(ids_carpetas)

def obtener_id_carpeta(ids_carpetas:list) -> str:
    """ 
    Pre: Recibe las listas de carpetas.
    Post: Le pregunta al usuario que id quiere obtener y lo imprime.
    """
    num_carpeta = input("\nIngrese el numero de carpeta que desea obtener el id: ")
    num_carpeta = conversor_int(num_carpeta)
    print(f"\nEl id de la carpeta {num_carpeta} es: {ids_carpetas[num_carpeta-1][0]}")

    return ids_carpetas[num_carpeta-1][0]

def separador_archivos_carpetas(archivos:dict)-> list:
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

def imprimir_archivos_drive(ids_archivos:list)-> None:
    """ 
    Pre: Recibe una lista de archivos.
    Post: Imprime esa lista separada por un numero inicial.
    """
    numero = 0
    for file in ids_archivos: 
        numero += 1
        print(f'\nArchivo Nº {numero}: {ids_archivos[numero-1][1]}')

def imprimir_archivos_local(archivos:list)-> None:
    """ 
    Pre: Recibe una lista de archivos.
    Post: Imprime esa lista separada por un numero inicial.
    """
    numero = 0
    for file in archivos: 
        numero += 1
        print(f'\nArchivo Nº {numero}: {file}')

def crear_carpeta_drive(drive_service:Resource,nombre_carpeta:str)-> None: #chequear q este ok el try except
    """ 
    Pre: Recibe el servicio de drive.
    Post: Crea una carpeta en google drive y la almacena donde quiera el usuario.
    """
    try:
        file_metadata = {
        'name': nombre_carpeta,
        'mimeType': 'application/vnd.google-apps.folder'
        }

        ubicacion = input("\nDesea almacenar esta carpeta en su unidad principal? (si/no): ")

        if ubicacion == "no":
            print("\nA continuacion le daremos la opcion de navegar entre las carpetas y al llegar a la carpeta en la cual quiere almacenar la carpeta a crear,\npor favor solicite el id.\n")
            folder_id = navegacion_carpetas_drive(drive_service) 

            file = drive_service.files().create(body=file_metadata,fields='id').execute()
            file_id = file.get('id')

            mover_archivos_drive(drive_service,file_id,folder_id)
            print("\nSu carpeta fue creada con exito.\n")
        else:
            file = drive_service.files().create(body=file_metadata,fields='id').execute()
            file_id = file.get('id')

            print("\nVamos a almacenarla en tu unidad principal.\n")
        print('\nFolder ID: %s\n' % file_id)
    except:
        print("\nLos datos ingresados no son validos, por favor intente nuevamente.\n")  

def subir_archivo_drive(drive_service:Resource,file_name:str,folder_id:str,file_path:str) -> None: 
    """ 
    Pre: Recibe los servicios de google drive, el n ombre del archivo y el id de la carpeta.
    Post: Recibe un archivo y lo sube a la carpeta deseada por el usuraio.
    """
    #try:
    file_metadata = {'name': file_name} 
    filepath = f"{file_path}/{file_name}"
    media = MediaFileUpload(filepath)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    file_id = file.get('id')

    mover_archivos_drive(drive_service,file_id,folder_id)
    print('\nID del archivo: %s\n' % file_id)
    #except: 
        #print("\nLos datos ingresados no son validos, por favor intente nuevamente.\n")

def descargar_archivo_drive(drive_service:Resource,file_id:str,file_name:str,file_path:str) -> None: #funcion para navegar entre archivos locales y que me devuuelva el path?
    """ 
    Pre: Recibo el servico de google drive API, el nombre del archivo, su ID y la carpeta en la cual lo quiere descargar.
    Post: Descarga el archivo solicitado por el usuario.
    """
    
    try:
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
    except PermissionError:
        print("\nNo tienes los permisos necesarios para acceder a esa carpeta. Intente nuevamente.\n")
    except shutil.Error:
        print("\nEl archivo que esta intentando descargar ya se encuentra en este directorio. Por favor intente nuevamente.\n")
    except FileNotFoundError:
        print("\nLa carpeta en la cual quiere almacenar el archivo no exsiste.\n") #ver de crear sola la carpeta 
    except:
        print("\nLos datos ingresados no son validos, por favor intente nuevamente.\n")

def buscar_archivos_drive(drive_service:Resource,palabra_buscador:str) -> None:
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

def mover_archivos_drive(drive_service:Resource,file_id:str,folder_id:str) -> None:
    """ 
    Pre: Recibe el Id del archivo a mover y el Id de la carpeta a la cual quiere mover el archivo.
    Post: Mueve el archivo hacia la carpeta elegida por el usuario.
    """
    try:
        # Retrieve the existing parents to remove
        file = drive_service.files().get(fileId=file_id,
                                        fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        # Move the file to the new folder
        file = drive_service.files().update(fileId=file_id,
                                            addParents=folder_id,
                                            removeParents=previous_parents,
                                            fields='id, parents').execute()
    except:
        print("\nLos datos ingresados no son validos, intente nuevamente.\n")

def escanear_archivos_locales(carpeta_local:str)-> list: 
    """ 
    Pre: Recibo una carpeta local.
    Post Creo una lista con el contenido de esa carpeta seleccionando un par de caracteristicas.
    """
    
    archivos_locales = list()
    try:
        with os.scandir(carpeta_local) as ficheros: #escanea todos los archivos en determinada carpeta
            for fichero in ficheros:
                ultima_modifiacion = time.ctime(os.path.getmtime(fichero))

                lista_l = [fichero.name,ultima_modifiacion,os.path.getsize(fichero)]
                archivos_locales.append(lista_l) #creo una lista con el nombre, el ultimo tiempo de modificacion local y su peso.
    except FileNotFoundError:
        print("La carpeta elegida no exsiste, por favor vuelva a intentarlo.")
    return archivos_locales

def escanear_archivos_drive(drive_service:Resource,carpeta_drive:str)-> list:
    """ 
    Pre: Recibo el servicio de drive api y la carpeta remota a escanear.
    Post: Escaneo la misma y armo una lista con los archivos y determinadas caracteristicas que me interesan.
    """
    lista_archivos_drive = list()
    archivos_drive = drive_service.files().list(q= f"'{carpeta_drive}' in parents",fields="nextPageToken, files(id, name, size, modifiedTime, mimeType)").execute()
    for archivo in archivos_drive.get('files', []):
        lista_d = [archivo.get('name'),archivo.get('modifiedTime'),archivo.get('size'),archivo.get('id')]
        lista_archivos_drive.append(lista_d)
    return lista_archivos_drive

def buscar_exsistencia_archivo(file_path:str,file_name:str)-> bool:
    """ 
    Pre: Le doy el file path y el nombre del archivo.
    Post: Verifica si el archivo exsiste o no.
    """
    filePath = f"{file_path}/{file_name}"
    try:
        with open(filePath, 'r') as f:
            exsiste = True
    except FileNotFoundError as e:
        exsiste = False
    except IOError as e:
        exsiste = False
    return exsiste

def comparacion_carpetas(drive_service:Resource,lista_local:list,lista_drive:list,carpeta_local:str,carpeta_drive:str) -> None: #ver como hacer para decsragar carpetas
    """ 
    Pre: Recibe la drive API, la lista local con su ruta y la del drive con su id.
    Post: Las compara y si hay diferencias, descarga o sube algun archivo.
    """
    if (len(lista_drive)) != len(lista_local): #si hay archivos q no fueron subidos, los sube y luego hace las comparaciones.
        if len(lista_local) > len(lista_drive):
            for archivo in lista_local:
                for archivo_drivee in lista_drive:
                    if archivo[0] != archivo_drivee[0]:
                        subir_archivo_drive(drive_service,archivo[0],carpeta_drive,carpeta_local)
        else:
            for archivo_drive in lista_drive:
                for archivo_local in lista_local:
                    if archivo_drive[0] != archivo_local[0]:
                        descargar_archivo_drive(drive_service,archivo_drive[3],archivo_drive[0],carpeta_local)

def conversor_formato_fecha(dia_drive:str)-> str:
    """ 
    Pre: Recibe la fecha de modificacion en el formato de google drive.
    Post: La cambia y la transforma en una fecha con el formato de los archivos locales.
    """
    meses = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    ano = dia_drive[0:4]
    num_mes = int(dia_drive[5:7])
    mes = meses[num_mes-1]
    dia = dia_drive[8:10]
    hora = dia_drive[11:19]

    fecha_final = (f"{mes} {dia} {hora} {ano}")
    return fecha_final

def filtrar_archivos(carpeta_drive:list,carpeta_local:list) -> list:
    """ 
    Pre: Recibo dos carpetas.
    Post: Le aplico filtros y creo nuevas carpetas con los archivos que me quedaron tras pasar los filtros.
    """
    contador = 0
    carpeta_filtrada_local = list()
    carpeta_filtrada_drive = list()
    for i in range(len(carpeta_drive)): #veo si coinciden las fechas de modificacion y el tamaño. [1] = dia , [2] = tamaño
        carpeta_drive[contador][1] = conversor_formato_fecha(carpeta_drive[contador][1]) #convierto la fecha al mismo formato
        carpeta_local[contador][1] = carpeta_local[contador][1][4:] #elimino el nombre del dia que era inecesario

        if carpeta_local[contador][1] != carpeta_drive[contador][1] or carpeta_local[contador][2] != carpeta_drive[contador][2]:
            carpeta_filtrada_local.append(carpeta_local[contador])
            carpeta_filtrada_drive.append(carpeta_drive[contador])
        contador += 1

    return carpeta_filtrada_drive,carpeta_filtrada_local

def analizis_linea_a_linea(carpeta_local:str,archivo_local:str,temporal:str,archivo_drive:str)-> Tuple: #no la uso
    """ 
    Pre: Recibe la carpeta local, el archivo local, una carpeta temporal y un archivo de drive.
    Post: Crea un archivo de texto en el cual van a estar las diferencias de linea entre los archivos a comparar.
    """
    with open(f"{carpeta_local}/{archivo_local}", 'r') as file_l:
        with open(f"{temporal}/{archivo_drive}", 'r') as file_d:
            difference = set(file_l).difference(file_d) #crea un set con las diferencias entre los archivos.

    difference.discard('\n')

    with open('output_file.txt', 'w') as file_out:
        for line in difference:
            file_out.write(line) #crea un archivo escribiendo las diferencias.
    return file_out,file_l,file_d

def crear_carpeta_temporal(drive_service:Resource,segundo_filtro_local:list,segundo_filtro_drive:list,carpeta_local:list,carpeta_drive:list): #nola borre x las dudas, pero no tiene uso
    """ 
    Pre: Recibe las listas filtradas, y las carpetas.
    Post: Crea una carpeta temporal en la cual se van a descargar los archivos de drive para ser analizados linea a linea.
    """
    with tempfile.TemporaryDirectory() as temporal: #carpeta temporal local para descragar los archivos y queluego se eliminen.
        contador = 0
        for i in segundo_filtro_local:
            archivo_local = segundo_filtro_local[contador][0]
            archivo_drive = segundo_filtro_drive[contador][0]

            descargar_archivo_drive(drive_service,segundo_filtro_drive[contador][3],segundo_filtro_drive[contador][0],temporal) #es necesaria la descarga de los archivos para luego comparar linea por linea

            file_out,file_l,file_d = analizis_linea_a_linea(carpeta_local,archivo_local,temporal,archivo_drive)

            if os.stat('output_file.txt').st_size != 0:
                print(f"\nEl archivo {archivo_local} tiene modificaciones y sera subido a la nube.")
                subir_archivo_drive(drive_service,archivo_local,carpeta_drive,carpeta_local)
                drive_service.files().delete(fileId=segundo_filtro_drive[contador][3]).execute() #elimina el archivo viejo

            file_out.close()
            os.remove('some_output_file.txt') #elimina el txt
            file_l.close()
            file_d.close()
            contador += 1

def sincronizacion_drive(drive_service:Resource)-> None:  #chequear q funcionen bien los filtros. Permitir navegacion por carpetas drive y local
    """ 
    Pre: Servicio de drive API.
    Post: Sincronza los archivos locales de determinada carpeta con los de la nube de otra carpeta especificada por el usuario.
    """
    print("\nVamos a sincronizar sus archivos! Por favor indiquenos su carpeta a sincronizar y su equivalente en el drive.\n") #"/home/fransobral/Documents/prueba"
    carpeta_local = input("\nPor favor ingrese la ruta de la carpeta local a sincronizar: ")
    carpeta_drive = input("\nPor favor ingrese el id de la carpeta en drive a sincronizar: ") # "18_khSXz0n70PQExWRJHrUygBGMS-1kOu"

    while not os.path.exists(carpeta_local):
        carpeta_local = input("Ese diectorio no existe, por favor ingreselo nuevamente: ")
    try:
        primer_filtro_local = escanear_archivos_locales(carpeta_local)
        primer_filtro_drive = escanear_archivos_drive(drive_service,carpeta_drive)

        comparacion_carpetas(drive_service,primer_filtro_local,primer_filtro_drive,carpeta_local,carpeta_drive)

        primer_filtro_local = escanear_archivos_locales(carpeta_local) #vuelvo a ejecutar estas funciones ya que pueden haber sufrido modificaciones.
        primer_filtro_drive = escanear_archivos_drive(drive_service,carpeta_drive)
        
        contador = 0
        
        for i in primer_filtro_local:
            archivo_local = primer_filtro_local[contador][0]
            print(f"\nEl archivo {archivo_local} tiene modificaciones.")
            subir_archivo_drive(drive_service,archivo_local,carpeta_drive,carpeta_local)
            drive_service.files().delete(fileId=primer_filtro_drive[contador][3]).execute() #elimina el archivo viejo
            contador += 1

        print("\nSincronizacion exitosa!\n")
    except FileNotFoundError:
        print("\nLa carpeta elegida no exsiste, por favor vuelva a intentarlo.\n")
    except:
        print("\nSu id de drive es inexsistente, por favor intente nuevamente\n.")

def comprobacion_recepcion_entregas(gmail_service:Resource) -> None:
    """
    PRE: Se le pasa el servicio de gmail.
    POST: Ejecuta las funciones de mandar mails segun la entrega.
    """
    mensajes = buscar_mails(gmail_service)
    validar_mail = validar_mail_evaluacion(gmail_service, mensajes)
    mandar_mail(validar_mail, gmail_service, mensajes)

def conseguir_asunto(gmail_service:Resource, mensajes_obtenidos) -> list:
    """ 
    Pre: Recibe los servicios de Gmail y todos los mails.
    Post: Retorna una lista con todos los asuntos con los que se enviaron los mails.
    """
    mail_subject = list()
    
    for mensaje in mensajes_obtenidos:

        informacion_de_mail = gmail_service.users().messages().get(userId = 'me', id = mensaje).execute()
    
        for informacion_asunto in informacion_de_mail['payload']['headers']:
            try:
                if informacion_asunto['name'] == 'Subject':
                    padron_asunto = informacion_asunto['value'].split(',')
                    mail_subject.append(padron_asunto[1])
            except:
                print('Por favor revise haber enviado el mail correctamente.')

    return mail_subject

def conseguir_to(gmail_service:Resource, mensajes_obtenidos) -> list:
    """ 
    Pre: Recibe los servicios de Gmail y todos los mails.
    Post: Retorna una lista con todas las direcciones a donde se enviaron los mails.
    """
    mail_to = list()

    for mensaje in mensajes_obtenidos:

            informacion_de_mail = gmail_service.users().messages().get(userId = 'me', id = mensaje).execute()

            for informacion_to in informacion_de_mail['payload']['headers']:
                if informacion_to['name'] == 'To':
                    mail_to.append(informacion_to['value'])
    
    return mail_to

def conseguir_from(gmail_service:Resource, mensajes_obtenidos) -> list:
    """ 
    Pre: Recibe los servicios de Gmail y todos los mails.
    Post: Retorna una lista con todos los destinatarios donde se enviaron los mails.
    """
    mail_from = list()
    
    for mensaje in mensajes_obtenidos:

        informacion_de_mail = gmail_service.users().messages().get(userId = 'me', id = mensaje).execute()

        for informacion_from in informacion_de_mail['payload']['headers']:
            if informacion_from['name'] == 'From':
                mail_from.append(informacion_from['value'])
    
    return mail_from

def validar_mail_evaluacion(gmail_service:Resource, mensajes_obtenidos) -> bool:
    """ 
    Pre: Recibe el servicio de Gmail.
    Post: Validar que el subject del mail (padron) este en el archivo csv.
    """
    validacion = False
    subject = conseguir_asunto(gmail_service, mensajes_obtenidos)

    with open('alumnos.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = list(csv_reader)
        for fila in range(len(data)):
            for asunto in range(len(subject)):
                if data[fila][1] in subject[asunto]:
                    validacion = True 

    return validacion

def buscar_mails(gmail_service:Resource) -> list: # Revisar esto
    """ 
    Pre: Recibe los servicios de gmail.
    Post: Agrega a una lista todos los mails que cumplan esa condicion.
    """
    mensajes = list()
    recibir_mails = gmail_service.users().messages().list(userId = 'me', q = 'label:inbox has:attachment is:unread').execute()
    mensajes_obtenidos = recibir_mails['messages']

    for mensaje_obtenido in mensajes_obtenidos:
        mensajes.append(mensaje_obtenido['id'])
    
    return mensajes

def mandar_mail(validacion:bool, gmail_service:Resource, mensajes_obtenidos) -> None:  # Terminar de ver si anda.
    """ 
    Pre: Recibe los datos del usuario que mando un mail.
    Post: Envia un mail avisando si la entrega fue correcta o no.
    """
    to_mail = conseguir_from(gmail_service, mensajes_obtenidos)
    from_mail = conseguir_to(gmail_service, mensajes_obtenidos)

    if validacion == True:
        validar = 'correcta'
    else:
        validar = 'incorrecta, por favor revisar y enviar datos correctamente'

    mimeMessage = MIMEMultipart()
    mimeMessage['subject'] = "Entrega evaluacion"
    message = f'Tu entrega esta {validar}.'
    mimeMessage['to'] = to_mail        
    mimeMessage['from'] = from_mail         
    mimeMessage.attach(MIMEText(message, "plain"))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    try:
        message = gmail_service.users().messages().send(userId = 'me', body = {'raw': raw_string}).execute()
    except Exception:
        print('Ha ocurrido un error, en cuanto podamos enviaremos el mail.')

#FRAN: AGREGAR PRE Y POST CONDICIONES Y TIPO DE PARAMETROS.

def verificar_nombre(padron:int, matcheo:str) -> str:

    alumno = "No existe"
    with open(matcheo, mode='r', newline='', encoding="UTF-8") as archivo:
        csv_reader = csv.reader(archivo, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            nombre = row[0]
            padron_csv = row[1]
            if padron_csv == padron:
                alumno = nombre
                
    return alumno
    
def verificar_docente(nombre:str, matcheo:str) -> str:
    profe = "No tiene profe"
    with open(matcheo, mode='r', newline='', encoding="UTF-8") as archivo: #open matcheo no exssiste. tenes q abrir un archivo
        csv_reader = csv.reader(archivo, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            profesor = row[0]
            nombre_csv = row[1]
            if nombre_csv == nombre:
                profe = profesor
                
    return profe    

def sistema_carpetas()-> None: #ver que onda esto
    ruta_carpeta_evaluaciones = input ("\nIngrese la ruta en la cual desea almacenar la carpeta Evaluaciones: ")
    crear_carpeta_local("Evaluaciones",ruta_carpeta_evaluaciones)
    archivo_alumno = "alumnos.csv" #abrir archivo csv
    archvio_alumnos_docentes = "docente-alumnos.csv" #abrir archivo csv
    
    for alumno in archivo_alumno:
        nombre = verificar_nombre(alumno, archivo_alumno) #le estas pasando el nombre de un alumno a un padron. archivo alumno != matcheo, son cosas distintas.
        docente = verificar_docente(nombre, archvio_alumnos_docentes) #le estas pasando un nombre de un archivo a un matcheo. archvio_alumnos_docentes != matcheo, son cosas distintas.
        ruta_docentes = f"{ruta_carpeta_evaluaciones}/{docente}"
        crear_carpeta_local(docente,ruta_docentes)
        nombre_carpeta_alumnos = alumno
        ruta_alumnos = f"{ruta_docentes}/{nombre}"
        crear_carpeta_local(nombre_carpeta_alumnos,ruta_alumnos)
      
def main()-> None:
    drive_service = service_drive.obtener_servicio() #este es el servicio de drive
    gmail_service = service_gmail.obtener_servicio() #este es el servicio de gmail
    comprobacion_recepcion_entregas(gmail_service)
    print("\nHola! Bienvenidos a nuestro servicio de google drive y gmail.\n")
    menu(drive_service,gmail_service)
    print("\nMuchas gracias por utilizar nuestro programa!\n")

if __name__ == '__main__':
    main()
