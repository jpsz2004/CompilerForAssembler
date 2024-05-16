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
    'type': 'R',
    'opcode': '0110011',
    'f3': '000',
    'f7': '0000000'
  },
  'sub': {
    'type': 'R',
    'opcode': '0110011',
    'f3': '000',
    'f7': '0100000'
  },
  'and': {
    'type': 'R',
    'opcode': '0110011',
    'f3': '111',
    'f7': '0000000'
  },
  'or': {
    'type': 'R',
    'opcode': '0110011',
    'f3': '110',
    'f7': '0000000'
  },
  'xor': {
    'type': 'R',
    'opcode': '0110011',
    'f3': '100',
    'f7': '0000000'
  },
  'sll': {
    'type': 'R',
    'opcode': '0110011',
    'f3': '001',
    'f7': '0000000'
  },
  'srl': {
    'type': 'R',
    'opcode': '0110011',
    'f3': '101',
    'f7': '0000000'
  },
  'sra': {
    'type': 'R',
    'opcode': '0110011',
    'f3': '101',
    'f7': '0100000'
  },
  'slt': {
    'type': 'R',
    'opcode': '0110011',
    'f3': '010',
    'f7': '0000000'
  },
  'sltu': {
    'type': 'R',
    'opcode': '0110011',
    'f3': '011',
    'f7': '0000000'
  },

  #Instrucciones tipo I
  'addi': {
    'type': 'I',
    'opcode': '0010011',
    'f3': '000',
    'f7': '0000000'
  },
  'xori': {
    'type': 'I',
    'opcode': '0010011',
    'f3': '000',
    'f7': '0000000'
  },
  'ori': {
    'type': 'I',
    'opcode': '0010011',
    'f3': '000',
    'f7': '0000000'
  },
  'andi': {
    'type': 'I',
    'opcode': '0010011',
    'f3': '000',
    'f7': '0000000'
  },
  'slli': {
    'type': 'I',
    'opcode': '0010011',
    'f3': '001',
    'f7': '0000000'
  },
  'srli': {
    'type': 'I',
    'opcode': '0010011',
    'f3': '101',
    'f7': '0000000'
  },
  'srai': {
    'type': 'I',
    'opcode': '0010011',
    'f3': '101',
    'f7': '0100000'
  },
  'slti': {
    'type': 'I',
    'opcode': '0010011',
    'f3': '010',
    'f7': '0000000'
  },
  'sltiu': {
    'type': 'I',
    'opcode': '0010011',
    'f3': '011',
    'f7': '0000000'
  },

  #Instrucciones tipo I load
  'lb': {
    'type': 'Il',
    'opcode': '0000011',
    'f3': '000',
    'f7': '0000000'
  },
  'lh': {
    'type': 'Il',
    'opcode': '0000011',
    'f3': '001',
    'f7': '0000000'
  },
  'lw': {
    'type': 'Il',
    'opcode': '0000011',
    'f3': '010',
    'f7': '0000000'
  },
  'lbu': {
    'type': 'Il',
    'opcode': '0000011',
    'f3': '100',
    'f7': '0000000'
  },
  'lhu': {
    'type': 'Il',
    'opcode': '0000011',
    'f3': '101',
    'f7': '0000000'
  },

  #Instrucciones tipo S
  'sb': {
    'type': 'S',
    'opcode': '0100011',
    'f3': '000',
    'f7': '0000000'
  },
  'sh': {
    'type': 'S',
    'opcode': '0100011',
    'f3': '001',
    'f7': '0000000'
  },
  'sw': {
    'type': 'S',
    'opcode': '0100011',
    'f3': '010',
    'f7': '0000000'
  },

  #Intrucciones tipo B
  'beq': {
    'type': 'B',
    'opcode': '1100011',
    'f3': '000',
    'f7': '0000000'
  },
  'bne': {
    'type': 'B',
    'opcode': '1100011',
    'f3': '001',
    'f7': '0000000'
  },
  'blt': {
    'type': 'B',
    'opcode': '1100011',
    'f3': '100',
    'f7': '0000000'
  },
  'bge': {
    'type': 'B',
    'opcode': '1100011',
    'f3': '101',
    'f7': '0000000'
  },
  'bltu': {
    'type': 'B',
    'opcode': '1100011',
    'f3': '110',
    'f7': '0000000'
  },
  'bgeu': {
    'type': 'B',
    'opcode': '1100011',
    'f3': '111',
    'f7': '0000000'
  },

  #Instrucciones tipo J
  'jal': {
    'type': 'J',
    'opcode': '1101111',
    'f3': '000',
    'f7': '0000000'
  },

  #Instruccion tipo I jalr
  'jalr': {
    'type': 'Ijalr',
    'opcode': '1100111',
    'f3': '000',
    'f7': '0000000'
  },

  #Instruccion tipo U
  'lui': {
    'type': 'U',
    'opcode': '0110111',
    'f3': '000',
    'f7': '0000000'
  },
  'auipc': {
    'type': 'U',
    'opcode': '0010111',
    'f3': '000',
    'f7': '0000000'
  },

  #Instrucciones tipo I adicionales
  'ecall': {
    'type': 'Iecall',
    'opcode': '1110011',
    'f3': '000',
    'f7': '0000000'
  },
  'ebreak': {
    'type': 'Iebreak',
    'opcode': '1110011',
    'f3': '000',
    'f7': '0000000'
  }
}

class HVisitor(plyplus.STransformer):
  # def __init__(self):
  #   super().__init__()
  #   self.instructionCounter = 0
  #   self.labels = {}

  # def label(self, expr):
  #   self.labels[expr.tail[0]] = self.instructionCounter + 4
  
  # def program(self, expr):
  #   print("Nodo programa")
  #   print(self.instructionCounter)
  #   print(expr)
    
  def regname(self, expr):
    val = expr.tail[0]
    regNum = regNames[val]
    regBin = format(regNum, '05b')
    return regBin
  
  def instr(self, expr):
    # Instruction name
    inst =  expr.tail[0]
    
    return {
      'type': instInfo[inst]['type'],
      'opcode': instInfo[inst]['opcode'],
      'f3': instInfo[inst]['f3'],
      'f7': instInfo[inst]['f7']
    }
    
  
  def insti(self, expr):
    inst =  expr.tail[0]
    return instInfo[inst]
    
  def imm(self, expr):
      val = int(expr.tail[0])
      immBin = format(val & 0xfff, '012b')  # Convierte a un binario de 12 bits
      return immBin

  def inst(self, expr):
    inst = expr.tail[0]
    
    if(inst['type'] == 'R'):
      print("f7({})-rs2({})-rs1({})-f3({})-rd({})-opcode({})".format(expr.tail[0]['f7'], expr.tail[3], expr.tail[2], expr.tail[0]['f3'], expr.tail[1], expr.tail[0]['opcode']))
      print("{}{}{}{}{}{}".format(expr.tail[0]['f7'], expr.tail[3], expr.tail[2], expr.tail[0]['f3'], expr.tail[1], expr.tail[0]['opcode']))
    
    elif(inst['type'] == 'I'):
      print("imm({})-rs1({})-f3({})-rd({})-opcode({})".format(expr.tail[3], expr.tail[2], expr.tail[0]['f3'], expr.tail[1], expr.tail[0]['opcode']))
      print("{}{}{}{}{}".format(expr.tail[3], expr.tail[2], expr.tail[0]['f3'], expr.tail[1], expr.tail[0]['opcode']))

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
        #print(v.labels)
