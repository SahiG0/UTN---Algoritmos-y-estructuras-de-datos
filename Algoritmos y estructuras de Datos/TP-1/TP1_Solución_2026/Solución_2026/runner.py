# Runner TP1 versión 3.0

# Historial de versiones:
# v1.0 desarrollada por el profesor Federico Bett
# v2.0 desarrollada por el profesor Valerio Frittelli
# v3.0 desarrollada por el profesor Jorge Harah
#      v3.0 control de juego de caracteres en consola aportado por el profesor Pablo Villalba

import os
import sys
import subprocess


class ResultRange:
    # Representa un rango real, permitiendo validar resultados en rangos
    # y no con valores puntuales

    def __init__(self, r_start, r_stop, include_start=True, include_end=True):
        self.__r_start = float(r_start) if isinstance(r_start, str) else r_start
        self.__r_stop = float(r_stop) if isinstance(r_stop, str) else r_stop
        self.__include_start = include_start
        self.__include_end = include_end

    def is_contained(self, value):
        # Determina si el valor a controlar está contenido en este rango
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                return False

        if self.__include_start and self.__include_end:
            res = self.__r_start <= value <= self.__r_stop

        elif self.__include_start:
            res = self.__r_start <= value < self.__r_stop

        elif self.__include_end:
            res = self.__r_start < value <= self.__r_stop

        else:
            res = self.__r_start < value < self.__r_stop

        return res

    def __str__(self):
        op1 = '<=' if self.__include_start else '<'
        op2 = '<=' if self.__include_end else '<'
        return f'{self.__r_start} {op1} resultado {op2} {self.__r_stop}'


# Directorio donde se almacenan los programas entregados por los estudiantes
SOURCES = "./trabajos/"

# Lotes de prueba contra los que serán corridos los programas de los estudiantes.
# ("Paciente\nCódigo\Monto base\n", Contexto, r1, r2, r3, r4)
BATCH_F1 = [
    # 3 Casos Base
    ("B01\nA01.5\n10000\n", "Base 1", "B01", "A01.5", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(62999, 63001)),
    ("B02\nM12.0\n10000\n", "Base 2", "B02", "M12.0", "Enfermedades del sistema osteomuscular y del tejido conjuntivo", ResultRange(74999, 75001)),
    ("B03\nU07.1\n5000\n", "Base 3", "B03", "U07.1", "Códigos para propósitos especiales", ResultRange(131299, 131301)),
    # 7 Casos Extra
    ("E01\nH10.0\n100000\n", "Extra 1", "E01", "H10.0", "Enfermedades del ojo y sus anexos", ResultRange(166999, 167001)),
    ("E02\nH10.0\n300000\n", "Extra 2", "E02", "H10.0", "Enfermedades del ojo y sus anexos", ResultRange(381999, 382001)),
    ("E03\nH05.5\n100000\n", "Extra 3", "E03", "H05.5", "Enfermedades del ojo y sus anexos", ResultRange(174499, 174501)),
    ("E04\nI05.0\n100000\n", "Extra 4", "E04", "I05.0", "Enfermedades del sistema circulatorio", ResultRange(157499, 157501)),
    ("E05\nI12.0\n100000\n", "Extra 5", "E05", "I12.0", "Enfermedades del sistema circulatorio", ResultRange(149999, 150001)),
    ("E06\nI09.9\n50000\n", "Extra 6", "E06", "I09.9", "Enfermedades del sistema circulatorio", ResultRange(114449, 114451)),
    ("E07\nH95.9\n10000\n", "Extra 7", "E07", "H95.9", "Enfermedades del oído y de la apófisis mastoides", ResultRange(67099, 67101))
]

BATCH_F2 = [
    # 3 Casos Base
    ("B01\nA01.5\n10000\n", "Base 1", "B01", "A01.5", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(62999, 63001)),
    ("B02\nM12.0\n10000\n", "Base 2", "B02", "M12.0", "Enfermedades del sistema osteomuscular y del tejido conjuntivo", ResultRange(74999, 75001)),
    ("B03\nU07.1\n5000\n", "Base 3", "B03", "U07.1", "Códigos para propósitos especiales", ResultRange(131299, 131301)),
    # 7 Casos Extra
    ("E01\nE10.0\n200000\n", "Extra 1", "E01", "E10.0", "Enfermedades endocrinas, nutricionales y metabólicas", ResultRange(157499, 157501)),
    ("E02\nE10.0\n100000\n", "Extra 2", "E02", "E10.0", "Enfermedades endocrinas, nutricionales y metabólicas", ResultRange(149999, 150001)),
    ("E03\nF10.0\n500000\n", "Extra 3", "E03", "F10.0", "Trastornos mentales y del comportamiento", ResultRange(302499, 302501)),
    ("E04\nF10.0\n400000\n", "Extra 4", "E04", "F10.0", "Trastornos mentales y del comportamiento", ResultRange(449999, 450001)),
    ("E05\nE05.5\n200000\n", "Extra 5", "E05", "E05.5", "Enfermedades endocrinas, nutricionales y metabólicas", ResultRange(165374, 165376)),
    ("E06\nF05.9\n500000\n", "Extra 6", "E06", "F05.9", "Trastornos mentales y del comportamiento", ResultRange(599499, 599501)),
    ("E07\nE01.1\n50000\n", "Extra 7", "E07", "E01.1", "Enfermedades endocrinas, nutricionales y metabólicas", ResultRange(100999, 101001))
]

BATCH_F3 = [
    # 3 Casos Base
    ("B01\nA01.5\n10000\n", "Base 1", "B01", "A01.5", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(62999, 63001)),
    ("B02\nM12.0\n10000\n", "Base 2", "B02", "M12.0", "Enfermedades del sistema osteomuscular y del tejido conjuntivo", ResultRange(74999, 75001)),
    ("B03\nU07.1\n5000\n", "Base 3", "B03", "U07.1", "Códigos para propósitos especiales", ResultRange(131299, 131301)),
    # 7 Casos Extra
    ("E01\nE06.0\n200000\n", "Extra 1", "E01", "E06.0", "Enfermedades endocrinas, nutricionales y metabólicas", ResultRange(157499, 157501)),
    ("E02\nE06.0\n100000\n", "Extra 2", "E02", "E06.0", "Enfermedades endocrinas, nutricionales y metabólicas", ResultRange(149999, 150001)),
    ("E03\nE04.0\n200000\n", "Extra 3", "E03", "E04.0", "Enfermedades endocrinas, nutricionales y metabólicas", ResultRange(249999, 250001)),
    ("E04\nF01.0\n500000\n", "Extra 4", "E04", "F01.0", "Trastornos mentales y del comportamiento", ResultRange(302499, 302501)),
    ("E05\nF01.0\n400000\n", "Extra 5", "E05", "F01.0", "Trastornos mentales y del comportamiento", ResultRange(449999, 450001)),
    ("E06\nF02.0\n500000\n", "Extra 6", "E06", "F02.0", "Trastornos mentales y del comportamiento", ResultRange(549999, 550001)),
    ("E07\nE05.0\n200000\n", "Extra 7", "E07", "E05.0", "Enfermedades endocrinas, nutricionales y metabólicas", ResultRange(249999, 250001))
]


BATCH_F4 = [
    # 3 Casos Base
    ("B01\nA01.5\n10000\n", "Base 1", "B01", "A01.5", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(62999, 63001)),
    ("B02\nU07.1\n5000\n", "Base 2", "B02", "U07.1", "Códigos para propósitos especiales", ResultRange(131299, 131301)),
    ("B03\nE10.0\n100000\n", "Base 3", "B03", "E10.0", "Enfermedades endocrinas, nutricionales y metabólicas", ResultRange(149999, 150001)),
    # 7 Casos Extra
    ("E01\nM12.0\n10000\n", "Extra 1", "E01", "M12.0", "Enfermedades del sistema osteomuscular y del tejido conjuntivo", ResultRange(94999, 95001)),
    ("E02\nM05.0\n10000\n", "Extra 2", "E02", "M05.0", "Enfermedades del sistema osteomuscular y del tejido conjuntivo", ResultRange(74999, 75001)),
    ("E03\nM10.0\n10000\n", "Extra 3", "E03", "M10.0", "Enfermedades del sistema osteomuscular y del tejido conjuntivo", ResultRange(74999, 75001)),
    ("E04\nN01.0\n10000\n", "Extra 4", "E04", "N01.0", "Enfermedades del sistema genitourinario", ResultRange(74999, 75001)),
    ("E05\nN02.0\n10000\n", "Extra 5", "E05", "N02.0", "Enfermedades del sistema genitourinario", ResultRange(80999, 81001)),
    ("E06\nN11.0\n10000\n", "Extra 6", "E06", "N11.0", "Enfermedades del sistema genitourinario", ResultRange(74999, 75001)),
    ("E07\nM15.5\n10000\n", "Extra 7", "E07", "M15.5", "Enfermedades del sistema osteomuscular y del tejido conjuntivo", ResultRange(98749, 98751))
]

BATCH_F5 = [
    # 3 Casos Base
    ("B01\nK00.0\n100000\n", "Base 1", "B01", "K00.0", "Enfermedades del sistema digestivo", ResultRange(149999, 150001)),
    ("B02\nK12.0\n100000\n", "Base 2", "B02", "K12.0", "Enfermedades del sistema digestivo", ResultRange(149999, 150001)),
    ("B03\nK05.5\n10000\n", "Base 3", "B03", "K05.5", "Enfermedades del sistema digestivo", ResultRange(62999, 63001)),
    # 7 Casos Extra
    ("E01\nJ02.0\n100000\n", "Extra 1", "E01", "J02.0", "Enfermedades del sistema respiratorio", ResultRange(161999, 162001)),
    ("E02\nJ02.0\n300000\n", "Extra 2", "E02", "J02.0", "Enfermedades del sistema respiratorio", ResultRange(374999, 375001)),
    ("E03\nJ03.0\n100000\n", "Extra 3", "E03", "J03.0", "Enfermedades del sistema respiratorio", ResultRange(149999, 150001)),
    ("E04\nA00.0\n100000\n", "Extra 4", "E04", "A00.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(161999, 162001)),
    ("E05\nZ00.0\n100000\n", "Extra 5", "E05", "Z00.0", "Factores que influyen en el estado de salud y contacto con los servicios de salud", ResultRange(178199, 178201)),
    ("E06\nJ02.5\n100000\n", "Extra 6", "E06", "J02.5", "Enfermedades del sistema respiratorio", ResultRange(169499, 169501)),
    ("E07\nA00.5\n100000\n", "Extra 7", "E07", "A00.5", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(170099, 170101))
]

BATCH_F6 = [
    # 3 Casos Base
    ("B01\nM12.0\n10000\n", "Base 1", "B01", "M12.0", "Enfermedades del sistema osteomuscular y del tejido conjuntivo", ResultRange(74999, 75001)),
    ("B02\nU07.1\n5000\n", "Base 2", "B02", "U07.1", "Códigos para propósitos especiales", ResultRange(131299, 131301)),
    ("B03\nE10.0\n100000\n", "Base 3", "B03", "E10.0", "Enfermedades endocrinas, nutricionales y metabólicas", ResultRange(149999, 150001)),
    # 7 Casos Extra
    ("E01\nA00.0\n10000\n", "Extra 1", "E01", "A00.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(41999, 42001)),
    ("E02\nA00.0\n30000\n", "Extra 2", "E02", "A00.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(62399, 62401)),
    ("E03\nA00.0\n50000\n", "Extra 3", "E03", "A00.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(99999, 100001)),
    ("E04\nA00.0\n0\n", "Extra 4", "E04", "A00.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(34999, 35001)),
    ("E05\nA00.0\n23000\n", "Extra 5", "E05", "A00.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(51099, 51101)),
    ("E06\nA00.0\n24000\n", "Extra 6", "E06", "A00.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(57719, 57721)),
    ("E07\nA00.5\n10000\n", "Extra 7", "E07", "A00.5", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(44099, 44101))
]

BATCH_F7 = [
    # 3 Casos Base
    ("B01\nA00.0\n10000\n", "Base 1", "B01", "A00.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(59999, 60001)),
    ("B02\nA02.0\n10000\n", "Base 2", "B02", "A02.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(59999, 60001)),
    ("B03\nM12.0\n10000\n", "Base 3", "B03", "M12.0", "Enfermedades del sistema osteomuscular y del tejido conjuntivo", ResultRange(74999, 75001)),
    # 7 Casos Extra
    ("E01\nA05.0\n10000\n", "Extra 1", "E01", "A05.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(179999, 180001)),
    ("E02\nA07.0\n10000\n", "Extra 2", "E02", "A07.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(179999, 180001)),
    ("E03\nA01.0\n10000\n", "Extra 3", "E03", "A01.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(194999, 195001)),
    ("E04\nA99.0\n10000\n", "Extra 4", "E04", "A99.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(194999, 195001)),
    ("E05\nA05.5\n10000\n", "Extra 5", "E05", "A05.5", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(188999, 189001)),
    ("E06\nA01.5\n10000\n", "Extra 6", "E06", "A01.5", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(203999, 204001)),
    ("E07\nU07.1\n5000\n", "Extra 7", "E07", "U07.1", "Códigos para propósitos especiales", ResultRange(393899, 393901))
]

BATCH_F8 = [
    # 3 Casos Base
    ("B01\nE10.0\n100000\n", "Base 1", "B01", "E10.0", "Enfermedades endocrinas, nutricionales y metabólicas", ResultRange(149999, 150001)),
    ("B02\nM12.0\n10000\n", "Base 2", "B02", "M12.0", "Enfermedades del sistema osteomuscular y del tejido conjuntivo", ResultRange(74999, 75001)),
    ("B03\nU07.1\n5000\n", "Base 3", "B03", "U07.1", "Códigos para propósitos especiales", ResultRange(131299, 131301)),
    # 7 Casos Extra
    ("E01\nA00.0\n10000\n", "Extra 1", "E01", "A00.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(59999, 60001)),
    ("E02\nA01.0\n10000\n", "Extra 2", "E02", "A01.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(62999, 63001)),
    ("E03\nA05.0\n10000\n", "Extra 3", "E03", "A05.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(62999, 63001)),
    ("E04\nA06.0\n10000\n", "Extra 4", "E04", "A06.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(71999, 72001)),
    ("E05\nA08.0\n10000\n", "Extra 5", "E05", "A08.0", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(74999, 75001)),
    ("E06\nC05.0\n10000\n", "Extra 6", "E06", "C05.0", "Tumores [neoplasias]", ResultRange(62999, 63001)),
    ("E07\nD10.0\n10000\n", "Extra 7", "E07", "D10.0", "Tumores [neoplasias]", ResultRange(74999, 75001))
]

BATCH_F9 = [
    # 3 Casos Base
    ("B01\nA01.5\n10000\n", "Base 1", "B01", "A01.5", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(62999, 63001)),
    ("B02\nM12.0\n10000\n", "Base 2", "B02", "M12.0", "Enfermedades del sistema osteomuscular y del tejido conjuntivo", ResultRange(74999, 75001)),
    ("B03\nU07.1\n5000\n", "Base 3", "B03", "U07.1", "Códigos para propósitos especiales", ResultRange(131299, 131301)),
    # 7 Casos Extra
    ("E01\nJ09.0\n100000\n", "Extra 1", "E01", "J09.0", "Enfermedades del sistema respiratorio", ResultRange(149999, 150001)),
    ("E02\nJ10.0\n100000\n", "Extra 2", "E02", "J10.0", "Enfermedades del sistema respiratorio", ResultRange(164999, 165001)),
    ("E03\nJ10.0\n200000\n", "Extra 3", "E03", "J10.0", "Enfermedades del sistema respiratorio", ResultRange(274999, 275001)),
    ("E04\nP07.0\n100000\n", "Extra 4", "E04", "P07.0", "Ciertas afecciones originadas en el período perinatal", ResultRange(164999, 165001)),
    ("E05\nP08.0\n100000\n", "Extra 5", "E05", "P08.0", "Ciertas afecciones originadas en el período perinatal", ResultRange(164999, 165001)),
    ("E06\nP09.0\n100000\n", "Extra 6", "E06", "P09.0", "Ciertas afecciones originadas en el período perinatal", ResultRange(194699, 194701)),
    ("E07\nJ10.5\n100000\n", "Extra 7", "E07", "J10.5", "Enfermedades del sistema respiratorio", ResultRange(172499, 172501))
]

BATCH_F10 = [
    # 3 Casos Base
    ("B01\nA01.5\n10000\n", "Base 1", "B01", "A01.5", "Ciertas enfermedades infecciosas y parasitarias", ResultRange(62999, 63001)),
    ("B02\nM12.0\n10000\n", "Base 2", "B02", "M12.0", "Enfermedades del sistema osteomuscular y del tejido conjuntivo", ResultRange(74999, 75001)),
    ("B03\nU07.1\n5000\n", "Base 3", "B03", "U07.1", "Códigos para propósitos especiales", ResultRange(131299, 131301)),
    # 7 Casos Extra
    ("E01\nD05.0\n10000\n", "Extra 1", "E01", "D05.0", "Tumores [neoplasias]", ResultRange(65999, 66001)),
    ("E02\nD10.0\n10000\n", "Extra 2", "E02", "D10.0", "Tumores [neoplasias]", ResultRange(59999, 60001)),
    ("E03\nD09.5\n10000\n", "Extra 3", "E03", "D09.5", "Tumores [neoplasias]", ResultRange(69299, 69301)),
    ("E04\nG05.0\n50000\n", "Extra 4", "E04", "G05.0", "Enfermedades del sistema nervioso", ResultRange(120999, 121001)),
    ("E05\nG05.0\n80000\n", "Extra 5", "E05", "G05.0", "Enfermedades del sistema nervioso", ResultRange(129999, 130001)),
    ("E06\nG04.0\n50000\n", "Extra 6", "E06", "G04.0", "Enfermedades del sistema nervioso", ResultRange(99999, 100001)),
    ("E07\nG11.5\n10000\n", "Extra 7", "E07", "G11.5", "Enfermedades del sistema nervioso", ResultRange(76229, 76231))
]


BATCHES = {
    "franja_1": BATCH_F1,
    "franja_2": BATCH_F2,
    "franja_3": BATCH_F3,
    "franja_4": BATCH_F4,
    "franja_5": BATCH_F5,
    "franja_6": BATCH_F6,
    "franja_7": BATCH_F7,
    "franja_8": BATCH_F8,
    "franja_9": BATCH_F9,
    "franja_10": BATCH_F10
}


# Muestra los valores contenidos en "text" en una línea de color rojo intenso.
def print_red(*text, end="\n"):
    for t in text:
        print(f"\033[91m{t}\033[00m", end=" ")
    print(end=end)


# Ejecuta el programa "script" y captura las salidas que sean dirigidas a la consola estándar.
def run(script):
    encoding = subprocess.run([sys.executable, '-c', "import sys; print(sys.stdout.encoding, end=None)"],
                              stdout=subprocess.PIPE,
                              shell=False)

    proc = subprocess.Popen([sys.executable, script],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    return proc, encoding.stdout.decode().strip()


def check_single_result(result, expected):
    if isinstance(expected, tuple):
        return result in expected

    if isinstance(expected, ResultRange):
        # Si es un ResultRange es porque se admite un resultado en un rango
        return expected.is_contained(result)

    return result == expected


def show_and_count(lines, results, data):
    # Índice para recorrer la lista "data" de resultados...
    # ... en esa lista, los resultados comienzan en la posición 2...
    k = 2

    # Contador de resultados correctos...
    ok = 0

    # print()
    for i in range(len(lines)):
        # ... mostrar el contexto del lote, si corresponde (líneas con número de orden divisible por 4)...
        if i % 4 == 0:
            print(f"\033[94mPrueba {data[1]}\033[00m")

        # ... mostrar el resultado tal como se mostró en el programa original...
        print("\t", lines[i], end="")

        # ... e informar correctos e incorrectos...
        if check_single_result(results[i].strip(), data[k]):
            ok += 1
            print(f"\033[92m --> Correcto\033[00m")
        else:
            print(f"\033[91m --> Incorrecto (esperado: {data[k]})\033[00m")

        if i % 4 == 3:
            print()

        k += 1

    # ...retornar el contador de respuestas correctas y salir...
    return ok


def collect_results(lines):
    # ... recolectar los resultados desde la consola estándar...
    results = []
    for i in range(len(lines)):
        # ...los resultados vienen luego de una secuencia ': '...
        r = lines[i].split(': ')
        results.append(r[1].strip())

    # ...retornar los resultados y salir...
    return results


# Procesa cada tupla "data" del lote "BATCH" con el programa "script" y analiza los resultados.
def start(script, batch):
    print_red("\n---------------------------------")
    print_red("Programa:", script.name)
    print_red("---------------------------------")

    ok = 0
    for data in batch:
        # Ejecutar el programa entregado por el estudiante...
        process, encoding = run(script.path)

        # Si hay datos tomados desde la línea de órdenes en la variable data, va esta línea...
        input_data = data[0].encode(encoding)
        output_lines, _ = process.communicate(input_data)

        # Si hay datos tomados desde la línea de órdenes en la variable data, va esta línea...
        # stdout_value = process.communicate(data[0].encode('utf-8'))[0].decode('utf-8')
        stdout_value = output_lines.decode(encoding)

        # Si NO hay datos desde la línea de órdenes, va esta otra...
        # ... para capturar lo que sea que se haya enviado a la consola de salida...
        # stdout_value = process.communicate()[0].decode('utf-8')

        # ... dividir en líneas esa salida...
        lines = stdout_value.splitlines()

        # ... eliminar los mensajes de input de la primera línea...
        r = lines[0].split(": ")[-2:]
        lines[0] = r[0] + ": " + r[1]

        # ...recolectar los resultados desde la consola estándar...
        results = collect_results(lines)

        # Mostrar las salidas del programa tal cual fueron generadas por los estudiantes...
        # ...pero indicando y contando los resultados correctos o no...
        ok += show_and_count(lines, results, data)

    ct = 4 * len(batch)
    prc = ok * 100 // ct
    print()
    print(f"\033[95mCantidad de resultados correctos: {ok}\033[00m")
    print(f"\033[95mPorcentaje de resultados correctos: {prc}%\033[00m")


# Inicia el test para todos los programas contenidos en el directorio "SOURCES".
def init():
    for a_day in BATCHES.keys():
        base_dir = f"{SOURCES}{a_day}"
        if not os.path.isdir(base_dir):
            print("Ignorando el directorio:", base_dir)
            continue

        print_red("\n\t\t*** Procesando lote", a_day.upper(), "***")
        with os.scandir(base_dir) as programs:
            for script in programs:
                if script.name.endswith(".py"):
                    try:
                        start(script, BATCHES[a_day])
                    except Exception as ex:
                        print()
                        print(f"\033[1;93;41m--> Error al ejecutar: ({ex})\033[00m")
                    print()
                    # input("Presione <Enter> para continuar con el siguiente trabajo...")


if __name__ == '__main__':
    init()
