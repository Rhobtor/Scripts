import socket

# Obtiene la dirección IP y la máscara de red
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Divide la dirección IP en octetos
octetos = ip_address.split('.')
print(f'Dirección IP: {ip_address}')

# Define una función para convertir la máscara de red en notación decimal
def mascara_decimal(mask):
    binary_mask = ''.join(format(int(octeto), '08b') for octeto in mask)
    decimal_mask = sum(int(bit) * (2 ** (7 - i)) for i, bit in enumerate(binary_mask))
    return decimal_mask

# Obtén la máscara de red
mask = socket.gethostbyname_ex(hostname)[-1][-1]

# Divide la máscara de red en octetos
octetos_mask = [int(octeto) for octeto in mask.split('.')]
print(f'Máscara de red: {mask}')

# Convierte la máscara de red en notación decimal
mask_decimal = mascara_decimal(octetos_mask)
print(f'Máscara de red en notación decimal: {mask_decimal}')

# # Realiza una condición para asignar un número a una variable
# if mask_decimal == 24:  # Cambia el número de acuerdo a tu máscara deseada
#     numero_asignado = 42  # Cambia el número a asignar según tu requerimiento
#     print(f'La máscara de red es /24, por lo tanto, el número asignado es: {numero_asignado}')
# else:
#     numero_asignado = None
#     print('La máscara de red no coincide con ninguna condición.')

# # Puedes usar la variable numero_asignado en tu código según tus necesidades
