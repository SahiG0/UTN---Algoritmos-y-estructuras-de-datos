# Entradas

nombre = input("Introduzca el nombre del paciente: ")
codigo = input("Introduzca el código ICD10 del diagnóstico: ")
monto_base = int(input("Introduzca el monto base a pagar por el tratamiento: "))

# Proceso

# Determinación del monto por letra

letra = codigo[0]
monto_base += 25000

if "A" <= letra <= "L":
    monto_final = monto_base + 25000
elif letra == "U":
    monto_final = monto_base + 100000
else:
    monto_final = monto_base + 40000

# Determinación de capítulo

num = float(codigo[1:3])

if letra == "A" or letra == "B":
    capitulo = "Ciertas enfermedades infecciosas y parasitarias"
elif letra == "C":
    capitulo = "Tumores [neoplasias]"
elif letra == "D":
    if num <= 48:
        capitulo = "Tumores [neoplasias]"
    elif 50 <= num <= 89:
        capitulo = "Enfermedades de la sangre y de los órganos hematopoyéticos, y ciertos trastornos que afectan el mecanismo de la inmunidad"
    else:
        capitulo = "Desconocido"
elif letra == "E":
    if num <= 90:
        capitulo = "Enfermedades endocrinas, nutricionales y metabolicas"
    else:
        capitulo = "Desconocido"
elif letra == "F":
    capitulo = "Trastornos mentales y del comportamiento"
elif letra == "G":
    capitulo = "Enfermedades del sistema nervioso"
elif letra == "H":
    if num <= 59:
        capitulo = "Enfermedades del ojo y sus anexos"
    elif 60 <= num <= 95:
        capitulo = "Enfermedades del oido y de la apofisis mastoides"
    else:
        capitulo = "Desconocido"
elif letra == "I":
    capitulo = "Enfermedades del sistema circulatorio"
elif letra == "J":
    capitulo = "Enfermedades del sistema respiratorio"
elif letra == "K":
    if num <= 93:
        capitulo = "Enfermedades del sistema digestivo"
    else:
        capitulo = "Desconocido"
elif letra == "L":
    capitulo = "Enfermedades de la piel y del tejido subcutáneo"
elif letra == "M":
    capitulo = "Enfermedades del sistema osteomuscular y del tejido conjuntivo"
elif letra == "N":
    capitulo = "Enfermedades del sistema genitourinario"
elif letra == "O":
    capitulo = "Embarazo, parto y puerperio"
elif letra == "P":
    if num <= 96:
        capitulo = "Ciertas afecciones originadas en el período perinatal"
    else:
        capitulo = "Desconocido"
elif letra == "Q":
    capitulo = "Malformaciones congénitas, deformidades y anomalías cromosómicas"
elif letra == "R":
    capitulo = "Síntomas, signos y hallazgos anormales clínicos y de laboratorio, no clasificados en otra parte"
elif letra == "S" or letra == "T":
    if letra == "T" and num <=98:
        capitulo = "Traumatismos, envenenamientos y algunas otras consecuencias de causas externas"
    elif letra == "S":
        capitulo = "Traumatismos, envenenamientos y algunas otras consecuencias de causas externas"
    else:
        capitulo = "Desconocido"
elif letra == "V" or letra == "W" or letra == "X" or letra == "Y":
    if (letra == "V" and num >= 1) or (letra == "W") or (letra == "X") or (letra == "Y" and num <= 98):
        capitulo = "Causas externas de morbilidad y de mortalidad"
    else:
        capitulo = "Desconocido"
elif letra == "Z":
    capitulo = "Factores que influyen en el estado de salud y contacto con los servicios de salud"
elif letra == "U":
    capitulo = "Códigos para propósitos especiales"
else:
    capitulo = "Desconocido"

# Determinación de monto porcentual

if len(codigo) >= 5:
    porcen = int(codigo[4])
    extra = (monto_final * porcen) / 100
    monto_final += extra

# Salidas
print("Nombre del paciente:", nombre)
print("Codigo:", codigo)
print("Capitulo:", capitulo)
print("Monto a pagar:", monto_final)