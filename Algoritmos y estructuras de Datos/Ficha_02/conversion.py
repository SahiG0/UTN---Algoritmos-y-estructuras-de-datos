tiempo_total = int(input("Ingrese el tiempo transcurrido (en segundos): "))

horas = tiempo_total // 3600
remanente = tiempo_total % 3600
minutos = remanente // 60
segundos = remanente % 60

print("Horas:", horas, ":", minutos, ":", segundos)
