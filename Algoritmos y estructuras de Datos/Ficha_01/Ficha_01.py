try:

    Edad = int(input("Ingrese su edad porfavor: "))

    if Edad < 18:
        print("No podes ingresar, tu edad es menor a 18 años")
    else:
        print("Puedes ingresar")

except ValueError:
    print("Error: Por favor, ingresá un número válido")

