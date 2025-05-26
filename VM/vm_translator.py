import os

class VMTranslator:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.label_count = 0  # Contador para labels temporários

    def translate(self):
        # Lê os comandos do arquivo de entrada
        with open(self.input_file, 'r') as infile:
            commands = infile.readlines()

        # Abre o arquivo de saída para gravar o código Hack
        with open(self.output_file, 'w') as outfile:
            for command in commands:
                # Remove espaços extras e comenta
                command = command.strip()  # Remove espaços no início e fim
                if "//" in command:         # Remove qualquer comentário
                    command = command.split("//")[0].strip()
                if command == "":
                    continue  # Ignora linhas vazias
                if command.startswith("push"):
                    outfile.write(self.handle_push(command) + "\n")
                elif command.startswith("pop"):
                    outfile.write(self.handle_pop(command) + "\n")
                else:
                    try:
                        outfile.write(self.handle_arithmetic(command) + "\n")
                    except ValueError as e:
                        print(f"Erro ao processar comando: {command}")
                        print(e)
                        continue  # Pula comandos inválidos

    
    def handle_push(self, command):
        """Gera o código Hack para um comando de 'push'"""
        parts = command.split()
        segment, index = parts[1], parts[2]

        if segment == "constant":
            return f"@{index}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1"
        elif segment == "local":
            return self.handle_memory_push(index, "LCL")
        elif segment == "argument":
            return self.handle_memory_push(index, "ARG")
        elif segment == "this":
            return self.handle_memory_push(index, "THIS")
        elif segment == "that":
            return self.handle_memory_push(index, "THAT")
        elif segment == "temp":
            return self.handle_temp_push(index)
        elif segment == "pointer":
            return self.handle_pointer_push(index)
        elif segment == "static":
            return self.handle_static_push(index)

    def handle_pop(self, command):
        """Gera o código Hack para um comando de 'pop'"""
        parts = command.split()
        segment, index = parts[1], parts[2]

        if segment == "local":
            return self.handle_memory_pop(index, "LCL")
        elif segment == "argument":
            return self.handle_memory_pop(index, "ARG")
        elif segment == "this":
            return self.handle_memory_pop(index, "THIS")
        elif segment == "that":
            return self.handle_memory_pop(index, "THAT")
        elif segment == "temp":
            return self.handle_temp_pop(index)
        elif segment == "pointer":
            return self.handle_pointer_pop(index)
        elif segment == "static":
            return self.handle_static_pop(index)

    def handle_arithmetic(self, command):
        """Gera o código Hack para um comando aritmético ou lógico"""
        if command == "add":
            return self.arithmetic_operation("M=D+M")
        elif command == "sub":
            return self.arithmetic_operation("M=M-D")
        elif command == "neg":
            return self.arithmetic_operation("M=-M")
        elif command == "eq":
            return self.comparison_operation("JEQ")
        elif command == "gt":
            return self.comparison_operation("JGT")
        elif command == "lt":
            return self.comparison_operation("JLT")
        elif command == "and":
            return self.arithmetic_operation("M=D&M")
        elif command == "or":
            return self.arithmetic_operation("M=D|M")
        elif command == "not":
            return self.arithmetic_operation("M=!M")
        else:
            raise ValueError(f"Comando aritmético ou lógico inválido: {command}")


    def handle_memory_push(self, index, segment):
        """Gera o código Hack para 'push' de um segmento de memória"""
        return f"@{segment}\nD=M\n@{index}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"

    def handle_temp_push(self, index):
        """Gera o código Hack para 'push' do segmento temp"""
        return f"@{5 + int(index)}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"

    def handle_pointer_push(self, index):
        """Gera o código Hack para 'push' do segmento pointer"""
        return f"@{'THIS' if index == '0' else 'THAT'}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"

    def handle_static_push(self, index):
        """Gera o código Hack para 'push' do segmento static"""
        return f"@static.{index}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"

    def handle_memory_pop(self, index, segment):
        """Gera o código Hack para 'pop' de um segmento de memória"""
        return f"@{segment}\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D"

    def handle_temp_pop(self, index):
        """Gera o código Hack para 'pop' do segmento temp"""
        return f"@SP\nAM=M-1\nD=M\n@{5 + int(index)}\nM=D"

    def handle_pointer_pop(self, index):
        """Gera o código Hack para 'pop' do segmento pointer"""
        return f"@SP\nAM=M-1\nD=M\n@{'THIS' if index == '0' else 'THAT'}\nM=D"

    def handle_static_pop(self, index):
        """Gera o código Hack para 'pop' do segmento static"""
        return f"@SP\nAM=M-1\nD=M\n@static.{index}\nM=D"

    def arithmetic_operation(self, operation):
        """Gera o código Hack para operações aritméticas"""
        return f"@SP\nAM=M-1\nD=M\nA=A-1\n{operation}"

    def comparison_operation(self, jump):
        """Gera o código Hack para operações de comparação"""
        label = self.new_label()
        return (f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@{label}\nD;{jump}\n"
                f"@SP\nA=M-1\nM=0\n@{label}_end\n0;JMP\n({label})\n@SP\nA=M-1\nM=-1\n({label}_end)")

    def new_label(self):
        """Gera um novo rótulo único"""
        self.label_count += 1
        return f"Label_{self.label_count}"

# Função principal
if __name__ == "__main__":
    input_file = "program.vm"  # Nome do arquivo de entrada VM
    output_file = "program.asm"  # Nome do arquivo de saída Hack

    translator = VMTranslator(input_file, output_file)
    translator.translate()
    print(f"Tradução completa! Código Hack salvo em '{output_file}'")
