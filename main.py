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

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.")
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as f:
        input_text = f.read()

    log_output = []
    log_output.append(f"--- Compiling {input_file} ---")

    try:
        # 1. Analisis lexico
        log_output.append("\n[Phase 1: Lexical Analysis]")
        input_stream = InputStream(input_text)
        lexer = gramaticaLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(BailErrorListener("Lexical"))
        token_stream = CommonTokenStream(lexer)
        token_stream.fill()
        log_output.append(f"Successfully generated {len(token_stream.tokens)} tokens.")

        # 2. Analisis sintactico
        log_output.append("\n[Phase 2: Syntactic Analysis]")
        parser = gramaticaParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(BailErrorListener("Syntactic"))
        tree = parser.program()
        log_output.append("Successfully built Parse Tree.")

        # 3. Analisis semantico
        log_output.append("\n[Phase 3: Semantic Analysis]")
        semantic_visitor = SemanticVisitor()
        semantic_visitor.visit(tree)
        log_output.append("Successfully validated semantics and symbol table.")

        # 4. Generacion de codigo intermedio (IR)
        log_output.append("\n[Phase 4: Intermediate Code Generation]")
        ir_generator = IRGenerator()
        ir_code = ir_generator.generate(tree)
        log_output.append("Successfully generated 3-Address Code.")

        # 5. Generacion de codigo destino (Python)
        log_output.append("\n[Phase 5: Python Code Generation]")
        code_generator = PythonGenerator()
        output_code = code_generator.generate(tree)
        log_output.append("Successfully generated executable Python script.")

        # Escribir resultados
        with open('output_program.py', 'w', encoding='utf-8') as f:
            f.write(output_code)

        # 6. Ejecutar codigo Python generado
        log_output.append("\n[Phase 6: Generated Python Execution]")
        execution = subprocess.run(
            [sys.executable, 'output_program.py'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if execution.returncode != 0:
            raise Exception(f"Generated Python execution failed:\n{execution.stderr}")

        log_output.append("Successfully executed generated Python script.")
        program_output = execution.stdout.strip()
        
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write("\n".join(log_output))
            f.write("\n\n--- Intermediate Code (TAC) ---\n")
            f.write(ir_code)
            f.write("\n\n--- Generated Python Output ---\n")
            f.write(program_output if program_output else "(no output)")

        print("Compilation successful.")
        print("- Detailed log and IR written to output.txt")
        print("- Python executable written to output_program.py")
        print("- Generated Python script executed successfully.")

    except Exception as e:
        error_msg = str(e)
        print(f"Error during compilation: {error_msg}")
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(f"Compilation Failed:\n{error_msg}")
        sys.exit(1)

if __name__ == "__main__":
    main()
