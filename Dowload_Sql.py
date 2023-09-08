import paramiko

# Configuración de la conexión al servidor
servidor_host = 'Server'
usuario = 'User'
contraseña = 'Password'
ruta_base_de_datos_remota = '/home/azken/Database/sensor.db'  # Ruta en el servidor

# Nombre del archivo de la base de datos en tu ordenador local
archivo_local = 'datos.db'

try:
    # Crear una conexión SFTP al servidor
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(servidor_host, username=usuario, password=contraseña)

    # Abrir una conexión SFTP
    sftp = ssh.open_sftp()

    # Descargar la base de datos desde el servidor al ordenador local
    sftp.get(ruta_base_de_datos_remota, archivo_local)

    # Cerrar la conexión SFTP
    sftp.close()

    # Cerrar la conexión SSH
    ssh.close()

    print(f"Base de datos descargada en '{archivo_local}'")

except Exception as e:
    print("Error al descargar la base de datos:", str(e))
