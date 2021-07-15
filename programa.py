from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


"""Shows basic usage of the Drive v3 API.
Prints the names and ids of the first 10 files the user has access to.
"""
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token_drive.json'):
    creds = Credentials.from_authorized_user_file('token_drive.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'token_drive.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('drive', 'v3', credentials=creds)

def verificacion_eleccion(numero:int) -> tuple:
    """ 
    Pre: Le ingreso el numero de opcion elegida por el usuario.
    Post: Imprimo un confirmacion de la eleccion del usuario
    """
    opcion_correcta = input(f"\nUsted a elegido la opcion {numero}. Esta seguro que desa continuar? (si/no): ")
    if opcion_correcta == "si" or opcion_correcta == "Si":
        exit = "si"
        correcta_eleccion = True
    else:
        print("\nMuy bien, eliga otra opcion:\n")
    return exit,correcta_eleccion

def elecciones(eleccion:int,) -> str:
    """ 
    Pre: Recibe un numero.
    Post: En base al numero, decide que funcion ejecutar y retorna un str que indica si el usuario quiere cerrar el programa o no.
    """
    if eleccion == 1:
        exit,correcta_eleccion = verificacion_eleccion(1)
        if correcta_eleccion:
            listar_archivos_drive()
            pass
        pass
    elif eleccion == 2:
        exit,correcta_eleccion = verificacion_eleccion(2)  
        if correcta_eleccion:
            eleccion_crear_archivo_o_carpeta()
    elif eleccion == 3:
        exit,correcta_eleccion = verificacion_eleccion(3)
        if correcta_eleccion:
            #ejecutar funcion
            pass
        pass
    elif eleccion == 4:
        exit,correcta_eleccion = verificacion_eleccion(4)
        if correcta_eleccion:
            #ejecutar funcion
            pass
        pass
    elif eleccion == 5:
        exit,correcta_eleccion = verificacion_eleccion(5)
        if correcta_eleccion:
            #ejecutar funcion
            pass
        pass
    elif eleccion == 6:
        exit,correcta_eleccion = verificacion_eleccion(6)
        if correcta_eleccion:
            #ejecutar funcion
            pass
        pass
    elif eleccion == 7:
        exit,correcta_eleccion = verificacion_eleccion(7)
        if correcta_eleccion:
            #ejecutar funcion
            pass
        pass
    elif eleccion == 8:
        exit = input("A decidido cerrar el programa, seguro que desea salir? (si/no): ")
    
    return exit

def menu() -> None:
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
            exit = elecciones(eleccion)
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

def eleccion_crear_archivo_o_carpeta() -> None:
    """ 
    Pre: -
    Post: El usuario elige que opcion quiere y se ejecuta la funcion correspondiente a esa accion.
    """
    decision = input("a)Crear una carpeta\nb)Crear un archivo.\nQue desea hacer?: ")
    while decision != "a" and decision != "b":
        print("\nEsa opcion no es valida, por favor intente nuevamente.\n")
        decision = input("a)Crear una carpeta\nb)Crear un archivo.\nQue desea hacer?: ")
    confirmacion = input(f"Usted eligio la opcion '{decision}', esta seguro que desea continuar? (si/no): ")
    if confirmacion == "si" or confirmacion == "Si":
        if decision == "a":
            crear_carpeta(service)
        if decision == "b":
            pass

def listar_archivos_drive():
    results = service.files().list(fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")


def crear_carpeta():
    """
    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

      
   if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id'])) """
    
    nombre_carpeta = input("Por favor ingrese el nombre de la carpeta a crear: ")
    file_metadata = {
    'name': nombre_carpeta,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata,
                                    fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))

def main()->None:
    print("\nHola! Bienvenidos a nuestro servicio de google drive y gmail.\n")

    menu()
    
    print("Muchas gracias por utilizar nuestro programa!")

if __name__ == '__main__':
    main()