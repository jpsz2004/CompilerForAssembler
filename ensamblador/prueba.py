import plyplus 
import sys

regNames = {
  'zero': 0,'x0': 0,
  'x1': 1, 'ra': 1, 
  'x2': 2, 'sp': 2,
  'x3': 3, 'gp': 3,
  'x4': 4, 'tp': 4,
  'x5': 5, 't0': 5,
  'x6': 6, 't1': 6,
  'x7': 7, 't2': 7,
  'x8': 8, 's0': 8, 'fp': 8,
  'x9': 9, 's1': 9,
  'x10': 10, 'a0': 10,
  'x11': 11, 'a1': 11,
  'x12': 12, 'a2': 12,
  'x13': 13, 'a3': 13,
  'x14': 14, 'a4': 14,
  'x15': 15, 'a5': 15,
  'x16': 16, 'a6': 16,
  'x17': 17, 'a7': 17,
  'x18': 18, 's2': 18,
  'x19': 19, 's3': 19,
  'x20': 20, 's4': 20,
  'x21': 21, 's5': 21,
  'x22': 22, 's6': 22,
  'x23': 23, 's7': 23,
  'x24': 24, 's8': 24,
  'x25': 25, 's9': 25,
  'x26': 26, 's10': 26,
  'x27': 27, 's11': 27,
  'x28': 28, 't3': 28,
  'x29': 29, 't4': 29,
  'x30': 30, 't5': 30,
  'x31': 31, 't6': 31
}

instInfo = {
  #Instrucciones tipo R
  'add': {
    'opcode': '0110011',
    'f3': '000',
    'f7': '0000000'
  },
  'sub': {
    'opcode': '0110011',
    'f3': '000',
    'f7': '0100000'
  },
  'and': {
    'opcode': '0110011',
    'f3': '111',
    'f7': '0000000'
  },
  'or': {
    'opcode': '0110011',
    'f3': '110',
    'f7': '0000000'
  },
  'xor': {
    'opcode': '0110011',
    'f3': '100',
    'f7': '0000000'
  },
  'sll': {
    'opcode': '0110011',
    'f3': '001',
    'f7': '0000000'
  },
  'srl': {
    'opcode': '0110011',
    'f3': '101',
    'f7': '0000000'
  },
  'sra': {
    'opcode': '0110011',
    'f3': '101',
    'f7': '0100000'
  },
  'slt': {
    'opcode': '0110011',
    'f3': '010',
    'f7': '0000000'
  },
  'sltu': {
    'opcode': '0110011',
    'f3': '011',
    'f7': '0000000'
  },

  #Instrucciones tipo I
  'addi': {
    'opcode': '0010011',
    'f3': '000',
    'f7': '0000000'
  },
  'xori': {
    'opcode': '0010011',
    'f3': '000',
    'f7': '0000000'
  },
  'ori': {
    'opcode': '0010011',
    'f3': '000',
    'f7': '0000000'
  },
  'andi': {
    'opcode': '0010011',
    'f3': '000',
    'f7': '0000000'
  },
  'slli': {
    'opcode': '0010011',
    'f3': '001',
    'f7': '0000000'
  },
  'srli': {
    'opcode': '0010011',
    'f3': '101',
    'f7': '0000000'
  },
  'srai': {
    'opcode': '0010011',
    'f3': '101',
    'f7': '0100000'
  },
  'slti': {
    'opcode': '0010011',
    'f3': '010',
    'f7': '0000000'
  },
  'sltiu': {
    'opcode': '0010011',
    'f3': '011',
    'f7': '0000000'
  },

  #Instrucciones tipo I load
  'lb': {
    'opcode': '0000011',
    'f3': '000',
    'f7': '0000000'
  },
  'lh': {
    'opcode': '0000011',
    'f3': '001',
    'f7': '0000000'
  },
  'lw': {
    'opcode': '0000011',
    'f3': '010',
    'f7': '0000000'
  },
  'lbu': {
    'opcode': '0000011',
    'f3': '100',
    'f7': '0000000'
  },
  'lhu': {
    'opcode': '0000011',
    'f3': '101',
    'f7': '0000000'
  },

  #Instrucciones tipo S
  'sb': {
    'opcode': '0100011',
    'f3': '000',
    'f7': '0000000'
  },
  'sh': {
    'opcode': '0100011',
    'f3': '001',
    'f7': '0000000'
  },
  'sw': {
    'opcode': '0100011',
    'f3': '010',
    'f7': '0000000'
  },

  #Intrucciones tipo B
  'beq': {
    'opcode': '1100011',
    'f3': '000',
    'f7': '0000000'
  },
  'bne': {
    'opcode': '1100011',
    'f3': '001',
    'f7': '0000000'
  },
  'blt': {
    'opcode': '1100011',
    'f3': '100',
    'f7': '0000000'
  },
  'bge': {
    'opcode': '1100011',
    'f3': '101',
    'f7': '0000000'
  },
  'bltu': {
    'opcode': '1100011',
    'f3': '110',
    'f7': '0000000'
  },
  'bgeu': {
    'opcode': '1100011',
    'f3': '111',
    'f7': '0000000'
  },

  #Instrucciones tipo J
  'jal': {
    'opcode': '1101111',
    'f3': '000',
    'f7': '0000000'
  },

  #Instruccion tipo I jalr
  'jalr': {
    'opcode': '1100111',
    'f3': '000',
    'f7': '0000000'
  },

  #Instruccion tipo U
  'lui': {
    'opcode': '0110111',
    'f3': '000',
    'f7': '0000000'
  },
  'auipc': {
    'opcode': '0010111',
    'f3': '000',
    'f7': '0000000'
  },

  #Instrucciones tipo I adicionales
  'ecall': {
    'opcode': '1110011',
    'f3': '000',
    'f7': '0000000'
  },
  'ebreak': {
    'opcode': '1110011',
    'f3': '000',
    'f7': '0000000'
  }
}

class HVisitor(plyplus.STransformer):
    def __init__(self):
        super().__init__()
        self.instructionCounter = 0

    def regname(self, expr):
        val = expr.tail[0]
        regNum = regNames[val]
        regBin = format(int(regNum), '05b')
        return regBin

    def instr(self, expr):
        inst = expr.tail[0]
        return instInfo[inst]['opcode']

    def insti(self, expr):
        inst = expr.tail[0]
        return instInfo[inst]

    def imm(self, expr):
        val = expr.tail[0]
        return val

    def inst(self, expr):
        # Descomponer la instrucción en sus componentes
        opcode = expr.tail[0]
        operands = expr.tail[1:]

        print(f"Instrucción: {opcode}")

        if opcode in instInfo:
            info = instInfo[opcode]
            print(f"Opcode: {info['opcode']}")
            if 'f3' in info:
                print(f"Funct3: {info['f3']}")
            if 'f7' in info:
                print(f"Funct7: {info['f7']}")

        # Imprimir cada operando por separado
        for operand in operands:
            if isinstance(operand, str) and operand in regNames:
                print(f"Registro: {operand} -> {regNames[operand]}")
            elif operand.isdigit():
                print(f"Inmediato: {operand}")
            else:
                print(f"Otro operando: {operand}")

        print("\n---\n")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Example call: {} input.asm output.asm".format(sys.argv[0]))
    else:
        sourceFile = sys.argv[1]
        targetFile = sys.argv[2]
        with open('riscv.g', 'r') as grm:
            with open(sourceFile, 'r') as scode:
                parser = plyplus.Grammar(grm)
                source = scode.read()
                t = parser.parse(source)
                t.to_png_with_pydot(r"tree.png")
                v = HVisitor()
                v.transform(t)

