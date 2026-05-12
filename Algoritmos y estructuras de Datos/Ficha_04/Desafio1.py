# Inestable
# Equilibrado Armónico
# Equilibrado Balanceado


# Entrada...

p = input("Ingrese un numero de 6 digitos: ")
n = len(p)

if len(p)!= 6:
    print("Número no valido para este desafío")

# Proceso...

else:
    a = int(p[0])
    b = int(p[1])
    c = int(p[2])
    d = int(p[3])
    e = int(p[4])
    f = int(p[5])

    suma_1 = a + b + c
    suma_2 = d + e + f

    if suma_1 == suma_2:

        invertido = p[5] + p[4] + p[3] + p[2] + p[1] + p[0]

        numero_1 = int(p)
        numero_2 = int(invertido)

        if numero_1 > numero_2:
            dif = numero_1 - numero_2
        else:
            dif = numero_2 - numero_1

        dif = str(dif)

        if len(dif) == 5:
            dif = "0" + dif

        elif len(dif) == 4:
            dif = "00" + dif

        elif len(dif) == 3:
            dif = "000" + dif

        elif len(dif) == 2:
            dif = "0000" + dif

        elif len(dif) == 1:
            dif = "00000" + dif

        g = int(dif[0])
        h = int(dif[1])
        i = int(dif[2])
        j = int(dif[3])
        k = int(dif[4])
        l = int(dif[5])

        suma_3 = g + h + i
        suma_4 = j + k + l

# Salidas...

        if suma_3 == suma_4:
            print("El numero es Equilibrado Armónico")

        else:
            print("El numero es Equilibrado Balanceado")

    else:
        print("El numero es Inestable")