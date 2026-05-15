#!/usr/bin/env python3
import sys
import os
import subprocess
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from generated.gramaticaLexer import gramaticaLexer
from generated.gramaticaParser import gramaticaParser
from semantic_analyzer.SemanticVisitor import SemanticVisitor
from codegen.python_generator import PythonGenerator
from codegen.ir_generator import IRGenerator

class BailErrorListener(ErrorListener):
    def __init__(self, phase):
        self.phase = phase

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception(f"[{self.phase} Error] at {line}:{column}: {msg}")

def compile_and_run(input_file, silent=False):
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.")
        return False

    with open(input_file, 'r', encoding='utf-8') as f:
        input_text = f.read()

    log_output = []
    log_output.append(f"--- Compiling {input_file} ---")

    try:
        # 1. Analisis lexico
        log_output.append("\n[Fase 1: Análisis Léxico]")
        log_output.append("  - Convirtiendo el texto fuente en una secuencia de tokens...")
        input_stream = InputStream(input_text)
        lexer = gramaticaLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(BailErrorListener("Lexical"))
        token_stream = CommonTokenStream(lexer)
        token_stream.fill()
        log_output.append(f"  - Éxito: Se generaron {len(token_stream.tokens)} tokens correctamente.")

        # 2. Analisis sintactico
        log_output.append("\n[Fase 2: Análisis Sintáctico]")
        log_output.append("  - Verificando la estructura gramatical y construyendo el Árbol de Derivación...")
        parser = gramaticaParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(BailErrorListener("Syntactic"))
        tree = parser.program()
        log_output.append("  - Éxito: Estructura sintáctica válida. Árbol de Análisis construido.")

        # 3. Analisis semantico
        log_output.append("\n[Fase 3: Análisis Semántico]")
        log_output.append("  - Validando tipos de datos y consistencia de variables...")
        semantic_visitor = SemanticVisitor()
        semantic_visitor.visit(tree)
        log_output.extend(semantic_visitor.logs)
        log_output.append("  - Éxito: Validación semántica completada sin errores.")

        # 4. Generacion de codigo intermedio (IR)
        log_output.append("\n[Fase 4: Generación de Código Intermedio (TAC)]")
        log_output.append("  - Transformando el árbol en instrucciones de Código de Tres Direcciones...")
        ir_generator = IRGenerator()
        ir_code = ir_generator.generate(tree)
        log_output.append("  - Éxito: Código intermedio (TAC) generado.")

        # 5. Generacion de codigo destino (Python)
        log_output.append("\n[Fase 5: Generación de Código Python]")
        log_output.append("  - Traduciendo el programa a un script ejecutable de Python...")
        code_generator = PythonGenerator()
        output_code = code_generator.generate(tree)
        log_output.append("  - Éxito: Script de Python generado.")

        # Escribir resultados
        with open('output_program.py', 'w', encoding='utf-8') as f:
            f.write(output_code)

        # 6. Ejecutar codigo Python generado
        log_output.append("\n[Fase 6: Ejecución del Código Generado]")
        log_output.append("  - Iniciando la ejecución del script Python resultante...")
        execution = subprocess.run(
            [sys.executable, 'output_program.py'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if execution.returncode != 0:
            raise Exception(f"La ejecución del código Python falló:\n{execution.stderr}")

        log_output.append("  - Éxito: El programa se ejecutó correctamente.")
        program_output = execution.stdout.strip()
        
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write("\n".join(log_output))
            f.write("\n\n" + "="*40 + "\n")
            f.write("RESUMEN DE RESULTADOS\n")
            f.write("="*40 + "\n")
            f.write("\n--- Código Intermedio (TAC) ---\n")
            f.write(ir_code)
            f.write("\n\n--- Código Python Generado ---\n")
            f.write(output_code)
            f.write("\n\n--- Salida Final del Programa ---\n")
            f.write(f"> {program_output}" if program_output else "(sin salida)")
            f.write("\n" + "="*40 + "\n")

        if not silent:
            print(f"\nCompilación exitosa de: {input_file}")
            print("="*50)
            print(" DETALLES DEL PROCESO DE COMPILACIÓN")
            print("="*50)
            print("\n".join(log_output))
            print("\n" + "="*50)
            print(f" RESULTADO FINAL: {program_output if program_output else '(sin salida)'}")
            print("="*50)
        return True

    except Exception as e:
        error_msg = str(e)
        if not silent:
            print(f"\nError durante la compilación de {input_file}: {error_msg}")
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(f"Compilation Failed:\n{error_msg}")
        return False

def show_menu():
    while True:
        print("\n" + "╔" + "═"*48 + "╗")
        print("║" + " MENU DEL MINI-COMPILADOR ".center(48) + "║")
        print("╠" + "═"*48 + "╣")
        print("║ 1. Seleccionar y compilar un archivo VÁLIDO      ║")
        print("║ 2. Seleccionar y compilar un archivo INVÁLIDO    ║")
        print("║ 3. Ejecutar todas las pruebas VÁLIDAS (Batch)    ║")
        print("║ 4. Ejecutar todas las pruebas INVÁLIDAS (Batch)  ║")
        print("║ 5. Ejecutar batería completa de pruebas          ║")
        print("║ 6. Salir                                         ║")
        print("╚" + "═"*48 + "╝")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            select_and_compile('tests/valid')
        elif opcion == '2':
            select_and_compile('tests/invalid')
        elif opcion == '3':
            run_test_batch('tests/valid', expected_success=True)
        elif opcion == '4':
            run_test_batch('tests/invalid', expected_success=False)
        elif opcion == '5':
            print("\n--- Ejecutando Batería Completa ---")
            v = run_test_batch('tests/valid', expected_success=True)
            i = run_test_batch('tests/invalid', expected_success=False)
            print(f"\nResumen Final: {v + i} pruebas pasadas con éxito.")
        elif opcion == '6':
            print("Saliendo del compilador. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def select_and_compile(directory):
    if not os.path.exists(directory):
        print(f"Error: Directorio {directory} no encontrado.")
        return

    files = sorted([f for f in os.listdir(directory) if f.endswith('.wf')])
    if not files:
        print(f"No se encontraron archivos .wf en {directory}")
        return

    print(f"\n--- Archivos en {directory} ---")
    for idx, f in enumerate(files, 1):
        print(f"{idx}. {f}")
    print(f"{len(files) + 1}. Volver al menú principal")

    try:
        choice = int(input("\nSeleccione el número del archivo a compilar: "))
        if 1 <= choice <= len(files):
            compile_and_run(os.path.join(directory, files[choice-1]))
        elif choice == len(files) + 1:
            return
        else:
            print("Opción fuera de rango.")
    except ValueError:
        print("Entrada no válida. Por favor ingrese un número.")

def run_test_batch(directory, expected_success):
    if not os.path.exists(directory):
        print(f"Error: Directorio {directory} no encontrado.")
        return 0
    
    files = sorted([f for f in os.listdir(directory) if f.endswith('.wf')])
    passed = 0
    print(f"\n--- Ejecutando pruebas en {directory} ---")
    for f in files:
        path = os.path.join(directory, f)
        success = compile_and_run(path, silent=True)
        if success == expected_success:
            print(f"  [PASS] {f}")
            passed += 1
        else:
            print(f"  [FAIL] {f} (Esperaba {'éxito' if expected_success else 'error'})")
    
    print(f"Subtotal: {passed}/{len(files)} pruebas pasadas.")
    return passed

def main():
    if len(sys.argv) == 2:
        compile_and_run(sys.argv[1])
    else:
        show_menu()

if __name__ == "__main__":
    main()
