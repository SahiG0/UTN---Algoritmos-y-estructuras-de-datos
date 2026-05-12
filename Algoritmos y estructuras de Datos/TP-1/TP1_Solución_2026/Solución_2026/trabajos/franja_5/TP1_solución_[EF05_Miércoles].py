# Entradas

nombre_paciente = input("Ingrese el nombre del paciente: ")
codigo = input("Ingrese el código ICD10 de la enfermedad: ")
monto_base = int(input("Ingrese el monto base: "))

CAPITULOS = ("Ciertas enfermedades infecciosas y parasitarias",
    "Tumores [neoplasias]",
    "Enfermedades de la sangre y de los órganos hematopoyéticos, y ciertos trastornos que afectan el mecanismo de la inmunidad",
    "Enfermedades endocrinas, nutricionales y metabólicas",
    "Trastornos mentales y del comportamiento",
    "Enfermedades del sistema nervioso",
    "Enfermedades del ojo y sus anexos",
    "Enfermedades del oído y de la apófisis mastoides",
    "Enfermedades del sistema circulatorio",
    "Enfermedades del sistema respiratorio",
    "Enfermedades del sistema digestivo",
    "Enfermedades de la piel y del tejido subcutáneo",
    "Enfermedades del sistema osteomuscular y del tejido conjuntivo",
    "Enfermedades del sistema genitourinario",
    "Embarazo, parto y puerperio",
    "Ciertas afecciones originadas en el período perinatal",
    "Malformaciones congénitas, deformidades y anomalías cromosómicas",
    "Síntomas, signos y hallazgos anormales clínicos y de laboratorio, no clasificados en otra parte",
    "Traumatismos, envenenamientos y algunas otras consecuencias de causas externas",
    "Causas externas de morbilidad y de mortalidad",
    "Factores que influyen en el estado de salud y contacto con los servicios de salud",
    "Códigos para propósitos especiales",
    "Sin capítulo")

monto_adicional = 25000

if "A" <= codigo[0] <= "L":
    monto_adicional += 25000
elif "M" <= codigo[0] <= "Z" and codigo[0] != "U":
    monto_adicional += 40000
else:
    monto_adicional += 100000

monto_final = monto_base + monto_adicional
monto_final = round(monto_final * (1 + int(codigo[4:]) / 100), 2)

letra = codigo[0]
numero_bloque = int(codigo[1:3])
aux = "-C-EFG--IJKLMNOPQR--ZU"

if letra in "AB":
    indice = 0
elif letra == "D":
    if 0 <= numero_bloque <= 48:
        indice = 1
    elif 50 <= numero_bloque <= 89:
        indice = 2
    else:
        indice = -1
elif letra == "H":
    if 0 <= numero_bloque <= 59:
        indice = 6
    elif 60 <= numero_bloque <= 95:
        indice = 7
    else:
        indice = -1
elif letra in "ST":
    indice = 18
elif letra in "VWXY":
    indice = 19
else:
    indice = aux.find(letra)

capitulo = CAPITULOS[indice]

# Extra
if letra == "J" and numero_bloque % 2 == 0:
    recargo = monto_base * 0.12
    if recargo > 25000:
        recargo = 25000
    monto_final += recargo

if letra not in "JK":
    monto_final *= 1.08


# Salidas
print("Beneficiario:", nombre_paciente)
print("Codigo:", codigo)
print("Capitulo:", capitulo)
print("Monto a pagar:", monto_final)