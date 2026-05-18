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


def format_trace_value(value):
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    return str(value)


def format_source_code(input_text):
    lines = input_text.splitlines()
    if not lines:
        return "(archivo vacio)"
    return "\n".join(f"{index:02d}: {line}" for index, line in enumerate(lines, 1))


def format_tokens(token_stream):
    token_lines = []
    for index, token in enumerate(token_stream.tokens, 1):
        if token.type == Token.EOF:
            token_name = "EOF"
            token_text = "<EOF>"
        else:
            token_name = gramaticaLexer.symbolicNames[token.type]
            token_text = token.text
        token_lines.append(
            f"{index:02d}. {token_name:<12} texto='{token_text}' "
            f"linea={token.line}, columna={token.column}"
        )
    return "\n".join(token_lines)


def format_symbol_table(symbol_table):
    if not symbol_table.symbols:
        return "(sin variables declaradas)"
    return "\n".join(
        f"- {name}: {type_name}"
        for name, type_name in symbol_table.symbols.items()
    )


def format_numbered_block(text):
    if not text:
        return "(sin contenido)"
    return "\n".join(f"{index:02d}: {line}" for index, line in enumerate(text.splitlines(), 1))


def describe_lexical_decisions(token_stream):
    descriptions = {
        gramaticaLexer.T_PRINT: "coincide con palabra reservada 'print'",
        gramaticaLexer.T_TRUE: "coincide con literal booleano TRUE",
        gramaticaLexer.T_FALSE: "coincide con literal booleano FALSE",
        gramaticaLexer.T_AND: "coincide con operador logico AND",
        gramaticaLexer.T_OR: "coincide con operador logico OR",
        gramaticaLexer.T_NOT: "coincide con operador logico NOT",
        gramaticaLexer.T_LPAREN: "coincide con parentesis de apertura '('",
        gramaticaLexer.T_RPAREN: "coincide con parentesis de cierre ')'",
        gramaticaLexer.T_SEMICOLON: "coincide con fin de sentencia ';'",
        gramaticaLexer.T_ASSIGN: "coincide con operador de asignacion '='",
        gramaticaLexer.ID: "coincide con ID: letra o '_' seguida de letras, numeros o '_'",
        gramaticaLexer.NUMBER: "coincide con NUMBER: uno o mas digitos",
    }
    lines = []
    for index, token in enumerate(token_stream.tokens, 1):
        if token.type == Token.EOF:
            lines.append(f"  {index:02d}. <EOF> => fin de la entrada")
            continue
        token_name = gramaticaLexer.symbolicNames[token.type]
        decision = descriptions.get(token.type, "token reconocido por la gramatica lexica")
        lines.append(f"  {index:02d}. '{token.text}' => {token_name}: {decision}")
    return lines


def describe_bool_term(ctx):
    prefix = "T_NOT " if ctx.T_NOT() else ""
    if ctx.ID():
        return f"boolTerm -> {prefix}ID usando '{ctx.ID().getText()}'"
    if ctx.T_TRUE():
        return f"boolTerm -> {prefix}T_TRUE usando 'TRUE'"
    if ctx.T_FALSE():
        return f"boolTerm -> {prefix}T_FALSE usando 'FALSE'"
    if ctx.NUMBER():
        return f"boolTerm -> {prefix}NUMBER usando '{ctx.NUMBER().getText()}'"
    if ctx.boolExpr():
        return f"boolTerm -> {prefix}'(' boolExpr ')' usando '{ctx.getText()}'"
    return f"boolTerm -> alternativa no reconocida usando '{ctx.getText()}'"


def describe_bool_expr(ctx):
    lines = [f"      boolExpr analiza '{ctx.getText()}'"]
    terms = ctx.boolTerm()
    if terms:
        lines.append(f"      - {describe_bool_term(terms[0])}")

    term_index = 1
    for child_index in range(1, ctx.getChildCount(), 2):
        operator = ctx.getChild(child_index).getText()
        lines.append(f"      - boolExpr encuentra operador '{operator}' y exige otro boolTerm")
        lines.append(f"      - {describe_bool_term(terms[term_index])}")
        term_index += 1

    if len(terms) == 1:
        lines.append("      - boolExpr termina porque no hay AND/OR adicional")
    else:
        lines.append("      - boolExpr termina despues de consumir todos los AND/OR")
    return lines


def describe_syntax_decisions(tree):
    lines = ["  program -> statement+ EOF"]
    statements = tree.statement()
    lines.append(f"  program detecta {len(statements)} statement(s) antes de EOF")

    for index, statement in enumerate(statements, 1):
        lines.append(f"  Statement {index}: texto '{statement.getText()}'")
        assignment = statement.assignment()
        print_stmt = statement.printStmt()
        if assignment:
            var_name = assignment.ID().getText()
            lines.append("    statement -> assignment porque inicia con ID y luego '='")
            lines.append(f"    assignment -> ID '=' boolExpr ';' para variable '{var_name}'")
            lines.extend(describe_bool_expr(assignment.boolExpr()))
        elif print_stmt:
            var_name = print_stmt.ID().getText()
            lines.append("    statement -> printStmt porque inicia con palabra reservada 'print'")
            lines.append(f"    printStmt -> 'print' '(' ID ')' ';' para variable '{var_name}'")
        else:
            lines.append("    statement no coincide con assignment ni printStmt")

    lines.append("  program consume EOF: no quedan tokens por analizar")
    return lines


def describe_ir_generation(ir_code):
    lines = []
    for index, instruction in enumerate(ir_code.splitlines(), 1):
        if instruction.startswith("PRINT "):
            lines.append(f"  {index:02d}. printStmt se convierte en TAC: {instruction}")
        elif " = NOT " in instruction:
            lines.append(f"  {index:02d}. operador NOT genera temporal/asignacion: {instruction}")
        elif " AND " in instruction or " OR " in instruction:
            lines.append(f"  {index:02d}. boolExpr compuesta genera operacion TAC: {instruction}")
        elif instruction.startswith("t"):
            lines.append(f"  {index:02d}. subexpresion genera temporal: {instruction}")
        else:
            lines.append(f"  {index:02d}. assignment genera TAC: {instruction}")
    return lines


def describe_python_generation(output_code):
    lines = []
    for index, line in enumerate(output_code.splitlines(), 1):
        if line.startswith("print("):
            lines.append(f"  {index:02d}. printStmt -> {line}")
        elif " not " in line or line.startswith("(not"):
            lines.append(f"  {index:02d}. T_NOT se traduce como 'not': {line}")
        elif " and " in line or " or " in line:
            lines.append(f"  {index:02d}. AND/OR se traducen como 'and'/'or': {line}")
        elif "True" in line or "False" in line:
            lines.append(f"  {index:02d}. TRUE/FALSE se traducen como True/False: {line}")
        else:
            lines.append(f"  {index:02d}. sentencia Python generada: {line}")
    return lines


def evaluate_ir_trace(ir_code):
    env = {}
    trace = []

    def resolve(token):
        if token == "TRUE":
            return True
        if token == "FALSE":
            return False
        if token in env:
            return env[token]
        raise Exception(f"Trace Error: No se encontro el valor de '{token}'.")

    def describe_env():
        if not env:
            return "{}"
        values = [f"{name}={format_trace_value(value)}" for name, value in env.items()]
        return "{ " + ", ".join(values) + " }"

    for index, raw_instruction in enumerate(ir_code.splitlines(), 1):
        instruction = raw_instruction.strip()
        if not instruction:
            continue

        trace.append(f"{index}. Ejecutando: {instruction}")

        if instruction.startswith("PRINT "):
            var_name = instruction.split(" ", 1)[1]
            value = resolve(var_name)
            trace.append(f"   => print({var_name}) muestra {format_trace_value(value)}")
            trace.append(f"   Estado: {describe_env()}")
            continue

        if " = " not in instruction:
            raise Exception(f"Trace Error: Instruccion TAC no reconocida: {instruction}")

        target, expression = instruction.split(" = ", 1)
        parts = expression.split()

        if len(parts) == 1:
            value = resolve(parts[0])
            explanation = f"{parts[0]} vale {format_trace_value(value)}"
        elif len(parts) == 2 and parts[0] == "NOT":
            operand = resolve(parts[1])
            value = not operand
            explanation = f"NOT {format_trace_value(operand)} = {format_trace_value(value)}"
        elif len(parts) == 3:
            left_token, operator, right_token = parts
            left = resolve(left_token)
            right = resolve(right_token)
            if operator == "AND":
                value = left and right
            elif operator == "OR":
                value = left or right
            else:
                raise Exception(f"Trace Error: Operador TAC no reconocido: {operator}")
            explanation = (
                f"{format_trace_value(left)} {operator} "
                f"{format_trace_value(right)} = {format_trace_value(value)}"
            )
        else:
            raise Exception(f"Trace Error: Expresion TAC no reconocida: {expression}")

        env[target] = value
        trace.append(f"   => {explanation}; se guarda {target} = {format_trace_value(value)}")
        trace.append(f"   Estado: {describe_env()}")

    return "\n".join(trace)

def compile_and_run(input_file, silent=False):
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.")
        return False

    with open(input_file, 'r', encoding='utf-8') as f:
        input_text = f.read()

    log_output = []
    log_output.append(f"--- Compiling {input_file} ---")
    phase_details = []
    phase_details.append("[Entrada]")
    phase_details.append("Codigo fuente recibido:")
    phase_details.append(format_source_code(input_text))

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
        log_output.append("  - Secuencia evaluada por las reglas lexicas:")
        log_output.extend(describe_lexical_decisions(token_stream))
        phase_details.append("\n[Fase 1: Analisis Lexico]")
        phase_details.append("Entrada: codigo fuente.")
        phase_details.append("Salida: secuencia de tokens que entiende el parser.")
        phase_details.append(format_tokens(token_stream))
        log_output.append(f"  - Éxito: Se generaron {len(token_stream.tokens)} tokens correctamente.")

        # 2. Analisis sintactico
        log_output.append("\n[Fase 2: Análisis Sintáctico]")
        log_output.append("  - Verificando la estructura gramatical y construyendo el Árbol de Derivación...")
        parser = gramaticaParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(BailErrorListener("Syntactic"))
        tree = parser.program()
        log_output.append("  - Secuencia evaluada por las reglas sintacticas:")
        log_output.extend(describe_syntax_decisions(tree))
        phase_details.append("\n[Fase 2: Analisis Sintactico]")
        phase_details.append("Entrada: tokens de la fase lexica.")
        phase_details.append("Salida: arbol de analisis construido con la gramatica.")
        phase_details.append(tree.toStringTree(recog=parser))
        log_output.append("  - Éxito: Estructura sintáctica válida. Árbol de Análisis construido.")

        # 3. Analisis semantico
        log_output.append("\n[Fase 3: Análisis Semántico]")
        log_output.append("  - Validando tipos de datos y consistencia de variables...")
        semantic_visitor = SemanticVisitor()
        semantic_visitor.visit(tree)
        log_output.extend(semantic_visitor.logs)
        log_output.append("  - Tabla de simbolos despues de validar la gramatica:")
        for symbol_line in format_symbol_table(semantic_visitor.symbol_table).splitlines():
            log_output.append(f"    {symbol_line}")
        phase_details.append("\n[Fase 3: Analisis Semantico]")
        phase_details.append("Entrada: arbol sintactico.")
        phase_details.append("Salida: variables validadas y tabla de simbolos.")
        phase_details.append("Validaciones realizadas:")
        phase_details.append("\n".join(semantic_visitor.logs))
        phase_details.append("Tabla de simbolos final:")
        phase_details.append(format_symbol_table(semantic_visitor.symbol_table))
        log_output.append("  - Éxito: Validación semántica completada sin errores.")

        # 4. Generacion de codigo intermedio (IR)
        log_output.append("\n[Fase 4: Generación de Código Intermedio (TAC)]")
        log_output.append("  - Transformando el árbol en instrucciones de Código de Tres Direcciones...")
        ir_generator = IRGenerator()
        ir_code = ir_generator.generate(tree)
        evaluation_trace = evaluate_ir_trace(ir_code)
        log_output.append("  - Secuencia de transformacion a TAC:")
        log_output.extend(describe_ir_generation(ir_code))
        phase_details.append("\n[Fase 4: Generacion de Codigo Intermedio TAC]")
        phase_details.append("Entrada: arbol sintactico validado semanticamente.")
        phase_details.append("Salida: instrucciones simples de tres direcciones.")
        phase_details.append(format_numbered_block(ir_code))
        log_output.append("  - Éxito: Código intermedio (TAC) generado.")

        # 5. Generacion de codigo destino (Python)
        log_output.append("\n[Fase 5: Generación de Código Python]")
        log_output.append("  - Traduciendo el programa a un script ejecutable de Python...")
        code_generator = PythonGenerator()
        output_code = code_generator.generate(tree)
        log_output.append("  - Secuencia de traduccion a Python:")
        log_output.extend(describe_python_generation(output_code))
        phase_details.append("\n[Fase 5: Generacion de Codigo Python Ejecutable]")
        phase_details.append("Entrada: arbol sintactico validado.")
        phase_details.append("Salida: codigo Python escrito en output_program.py.")
        phase_details.append(format_numbered_block(output_code))
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
        log_output.append("  - Secuencia de ejecucion evaluada desde el TAC:")
        for trace_line in evaluation_trace.splitlines():
            log_output.append(f"    {trace_line}")
        phase_details.append("\n[Fase 6: Ejecucion del Python Generado]")
        phase_details.append("Entrada: archivo output_program.py.")
        phase_details.append("Salida final producida por el programa:")
        phase_details.append(f"> {program_output}" if program_output else "(sin salida)")
        
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write("\n".join(log_output))
            f.write("\n\n" + "="*40 + "\n")
            f.write("SECUENCIA COMPLETA PARA LLEGAR AL EJECUTABLE PYTHON\n")
            f.write("="*40 + "\n")
            f.write("\n".join(phase_details))
            f.write("\n\n" + "="*40 + "\n")
            f.write("RESUMEN DE RESULTADOS\n")
            f.write("="*40 + "\n")
            f.write("\n--- Código Intermedio (TAC) ---\n")
            f.write(ir_code)
            f.write("\n\n--- Secuencia de Evaluacion Paso a Paso ---\n")
            f.write(evaluation_trace)
            f.write("\n\n--- Código Python Generado ---\n")
            f.write("Archivo creado: output_program.py\n\n")
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
        success = compile_and_run(sys.argv[1])
        sys.exit(0 if success else 1)
    else:
        show_menu()

if __name__ == "__main__":
    main()
