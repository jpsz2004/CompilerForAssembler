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
    'type': 'Is',
    'opcode': '0010011',
    'f3': '001',
    'imm7': '0000000'
  },
  'srli': {
    'type': 'Is',
    'opcode': '0010011',
    'f3': '101',
    'imm7': '0000000'
  },
  'srai': {
    'type': 'Is',
    'opcode': '0010011',
    'f3': '101',
    'imm7': '0100000'
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

class ImmediateOutOfRangeError(Exception):
    """Exception raised for immediates that do not fit in 12 bits."""
    pass

class HVisitor(plyplus.STransformer):
    
  def regname(self, expr):
    val = expr.tail[0]
    regNum = regNames[val]
    regBin = format(regNum, '05b')
    return regBin
  
  def instr(self, expr):
    inst =  expr.tail[0]
    return instInfo[inst]
    
  
  def insti(self, expr):
    inst =  expr.tail[0]
    return instInfo[inst]
  
  def instis(self, expr):
    inst =  expr.tail[0]
    return instInfo[inst]
    
  def imm12(self, expr):
    val = int(expr.tail[0])
    # Verifica que el inmediato quepa en 12 bits con signo
    if val < -2048 or val > 2047:
      raise ImmediateOutOfRangeError(f"Immediate value {val} out of range for 12-bit signed integer")
        
    # Convierte el inmediato a complemento a dos de 12 bits si es negativo
    if val < 0:
      val = (1 << 12) + val
        
    imm12Bin = format(val & 0xfff, '012b')  # Asegura que esté en 12 bits
    return imm12Bin
  
  def imm5(self, expr):
    val = int(expr.tail[0])
    if val < 0 or val > 31:
      raise ImmediateOutOfRangeError(f"Immediate value {val} out of range for 5-bit non-signed integer")
    
    imm5Bin = format(val & 0x1f, '05b')  # Asegura que esté en 5 bits
    return imm5Bin

  def printRInstructionBIN(self, expr):
    inst = expr.tail[0]
    f7 = inst['f7']
    rs2 = expr.tail[3]
    rs1 = expr.tail[2]
    f3 = inst['f3']
    rd = expr.tail[1]
    opcode = inst['opcode']
    return f7 + rs2 + rs1 + f3 + rd + opcode
  
  def printRInstructionHEXA(self, expr):
    inst = expr.tail[0]
    f7 = inst['f7']
    rs2 = expr.tail[3]
    rs1 = expr.tail[2]
    f3 = inst['f3']
    rd = expr.tail[1]
    opcode = inst['opcode']
    return hex(int(f7 + rs2 + rs1 + f3 + rd + opcode, 2))
  
  def printIInstructionBIN(self, expr):
    inst = expr.tail[0]
    imm12 = expr.tail[3]
    rs1 = expr.tail[2]
    f3 = inst['f3']
    rd = expr.tail[1]
    opcode = inst['opcode']
    return imm12 + rs1 + f3 + rd + opcode
  
  def printIInstructionHEXA(self, expr):
    inst = expr.tail[0]
    imm12 = expr.tail[3]
    rs1 = expr.tail[2]
    f3 = inst['f3']
    rd = expr.tail[1]
    opcode = inst['opcode']
    return hex(int(imm12 + rs1 + f3 + rd + opcode, 2))
  
  def printIsInstructionBIN(self, expr):
    inst = expr.tail[0]
    imm7 = inst['imm7']
    shamt = expr.tail[3]
    rs1 = expr.tail[2]
    f3 = inst['f3']
    rd = expr.tail[1]
    opcode = inst['opcode']
    return imm7 + shamt + rs1 + f3 + rd + opcode
  
  def printIsInstructionHEXA(self, expr):
    inst = expr.tail[0]
    imm7 = inst['imm7']
    shamt = expr.tail[3]
    rs1 = expr.tail[2]
    f3 = inst['f3']
    rd = expr.tail[1]
    opcode = inst['opcode']
    return hex(int(imm7 + shamt + rs1 + f3 + rd + opcode, 2))

  #Metodo para imprimir el codigo maquina segun cada instruccion
  def inst(self, expr):
    inst = expr.tail[0]
        
    if inst['type'] == 'R':
      print("f7({})-rs2({})-rs1({})-f3({})-rd({})-opcode({})".format(inst['f7'], expr.tail[3], expr.tail[2], inst['f3'], expr.tail[1], inst['opcode']))
      print(self.printRInstructionBIN(expr))
      print(self.printRInstructionHEXA(expr))
        
    elif inst['type'] == 'I':
      print("imm12({})-rs1({})-f3({})-rd({})-opcode({})".format(expr.tail[3], expr.tail[2], inst['f3'], expr.tail[1], inst['opcode']))
      print(self.printIInstructionBIN(expr))
      print(self.printIInstructionHEXA(expr))

    elif inst['type'] == 'Is':
      print("imm7({})-shamt({})-rs1({})-f3({})-rd({})-opcode({})".format(inst['imm7'], expr.tail[3], expr.tail[2], inst['f3'], expr.tail[1], inst['opcode']))
      print(self.printIsInstructionBIN(expr))
      print(self.printIsInstructionHEXA(expr))
          


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
        try:
          v.transform(t)
        except ImmediateOutOfRangeError as e:
          print(f"Error: {e}")