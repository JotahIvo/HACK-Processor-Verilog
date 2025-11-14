# Processador Hack em Verilog

![Verilog](https://img.shields.io/badge/Verilog-8E007B?style=for-the-badge&logo=verilog&logoColor=white)
![Nand2Tetris](https://img.shields.io/badge/Nand2Tetris-Curso-orange?style=for-the-badge)

## 📖 Visão Geral

Este projeto é uma implementação do processador "Hack" de 16 bits, proposto no famoso curso **"The Elements of Computing Systems"** (também conhecido como "Nand to Tetris"). A arquitetura da CPU é implementada inteiramente em Verilog (HDL).

O Processador Hack é uma arquitetura Von Neumann simples, projetada para fins educacionais. Ele possui uma memória de instruções (ROM) e uma memória de dados (RAM) separadas (embora o acesso a ambas seja feito através do mesmo barramento de endereço na CPU). Ele é capaz de executar programas escritos na linguagem de montagem Hack.

Este projeto foi desenvolvido como [Parte da disciplina de Arquitetura de Computadores na Universidade XXX / um projeto de estudo pessoal].

## ⚙️ Arquitetura e Funcionalidades

A implementação segue estritamente o design proposto no "Nand to Tetris", capítulo 5.

- **Arquitetura de 16 bits:** Todos os registradores, barramentos de dados e a ALU operam com 16 bits.
- **Instruções Tipo-A:** Instruções de carregamento de valor (`@valor`), que carregam um valor de 15 bits no Registrador A.
- **Instruções Tipo-C:** Instruções de computação (`dest=comp;jump`), que realizam operações na ALU e gerenciam o fluxo do programa.
- **Design Modular:** O processador é construído hierarquicamente, conectando módulos menores e reutilizáveis.

### Componentes Principais (Módulos Verilog)

1.  **CPU (cpu.v):** O módulo principal que integra todos os outros componentes. Ele decodifica as instruções e gerencia o fluxo de dados e controle.
2.  **ALU (alu.v):** Unidade Lógica e Aritmética. Realiza operações como `x+y`, `x-y`, `x&y`, `x|y`, `!x`, `-1`, `0`, etc., com base em 6 bits de controle.
3.  **Registradores (register.v):** Módulo genérico de registrador de 16 bits com uma entrada de `load`. Usado para implementar os Registradores A e D.
4.  **PC (pc.v):** Program Counter (Contador de Programa). Um registrador de 16 bits com lógica para `load` (salto), `inc` (incremento) e `reset`.
5.  **Memória (memory.v):** (Opcional, pode estar no testbench) Módulo que simula a RAM.
6.  **ROM (rom.v):** (Opcional, pode estar no testbench) Módulo que simula a Memória de Instruções (ROM), geralmente lendo um arquivo `.mem` ou `.hex`.

## 🚀 Como Simular

Para compilar e simular este projeto, você precisará de um simulador Verilog. As instruções abaixo usam **Icarus Verilog (iverilog)** e **GTKWave**, que são ferramentas de código aberto.

### Pré-requisitos

- [Icarus Verilog](http://iverilog.icarus.com/) (para compilação e simulação)
- [GTKWave](http://gtkwave.sourceforge.net/) (para visualização das formas de onda)

### Passos para Simulação

1.  **Clone o repositório:**

    ```bash
    git clone [URL_DO_SEU_REPOSITORIO]
    cd [NOME_DO_DIRETORIO]
    ```

2.  **Compile os arquivos Verilog:**
    Navegue até o diretório do projeto e execute o comando `iverilog`. Você deve incluir o testbench principal e _todos_ os módulos Verilog que ele instancia.

    ```bash
    iverilog -o cpu_sim testbench/tb_cpu.v src/*.v
    ```

    _(Isso compila todos os arquivos em `src/` e o `tb_cpu.v`, e gera um arquivo executável chamado `cpu_sim`)_

3.  **Execute a simulação:**
    Execute o arquivo compilado com o `vvp`.

    ```bash
    vvp cpu_sim
    ```

4.  **Visualize as Formas de Onda (Waveforms):**
    Se o seu testbench (`tb_cpu.v`) foi configurado para gerar um arquivo de "dump" (geralmente `.vcd`), você pode visualizá-lo com o GTKWave.

    _Exemplo de código para adicionar ao seu testbench para gerar o .vcd:_

    ```verilog
    initial begin
      $dumpfile("waves.vcd"); // Nome do arquivo de saída
      $dumpvars(0, tb_cpu);   // "tb_cpu" é o nome do seu módulo testbench
    end
    ```

    Após a execução do `vvp`, abra o arquivo gerado:

    ```bash
    gtkwave waves.vcd
    ```

## Synthesis (Síntese)

O código foi escrito de forma a ser sintetizável e pode ser portado para uma FPGA (como Xilinx Vivado ou Intel Quartus) com modificações mínimas (principalmente na implementação da ROM e RAM usando blocos de memória da FPGA).

teste15

teste de pr 2: commit 1
teste de pr 2: commit 2
