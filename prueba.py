file_name = "holahgfuiebviuebf.jpg"

filename = file_name[-4:]
while filename != ".txt" and filename != ".csv" and filename != "json":
    print("\nLa extension del archivo no esta permitida. Los formatos permitidos son .txt, .json o .csv.\n")
    file_name = input("\nIngrese el nombre del archivo junto su extension: ")
    filename = file_name[-4:] 
