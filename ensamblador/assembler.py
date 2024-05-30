import plyplus 
import sys
import json

#Carga de los archivos JSON con la informacion de los registros y las instrucciones
with open('registers.json') as f:
  regNames = json.load(f)

with open('instInfo.json') as f:
  instInfo = json.load(f)


#Clase para reportar errores de inmediatos fuera de rango
class ImmediateOutOfRangeError(Exception):
    pass

#Clase para visitar el arbol de parseo
class HVisitor(plyplus.STransformer):
    
  #Metodo para obtener los nombres de los registros y convertir sus valores a binarios
  def regname(self, expr):
    val = expr.tail[0]
    regNum = regNames[val]
    regBin = format(regNum, '05b')
    return regBin
  
  #Metodo para parsear las instrucciones tipo R
  def instr(self, expr):
    inst =  expr.tail[0]
    return instInfo[inst]
    
  #Metodo para parsear las instrucciones tipo I
  def insti(self, expr):
    inst =  expr.tail[0]
    return instInfo[inst]
  
  #Metodo para parsear las instrucciones tipo I de corrimiento
  def instis(self, expr):
    inst =  expr.tail[0]
    return instInfo[inst]
  
  #Metodo para parsear las instrucciones tipo I de carga
  def instil(self, expr):
    inst =  expr.tail[0]
    return instInfo[inst]
  
  #Metodo para parsear las instrucciones tipo S
  def insts(self, expr):
    inst = expr.tail[0]
    return instInfo[inst]
  
  def instj(self, expr):
    inst = expr.tail[0]
    return instInfo[inst]

  def instu(self, expr):
    inst = expr.tail[0]
    return instInfo[inst]
  
  def instiecall(self, expr):
    inst = expr.tail[0]
    return instInfo[inst]

  def instiebreak(self, expr):
    inst = expr.tail[0]
    return instInfo[inst]
  
  #Metodo para convertir los inmediatos de 12 bits a binario con signo
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
  
  #Metodo para convertir los inmediatos de 5 bits a binario sin signo
  def imm5(self, expr):
    val = int(expr.tail[0])
    if val < 0 or val > 31:
      raise ImmediateOutOfRangeError(f"Immediate value {val} out of range for 5-bit non-signed integer")
    
    imm5Bin = format(val & 0x1f, '05b')  # Asegura que esté en 5 bits
    return imm5Bin

  #Método para convertir los inmediatos de 21 bits a binario con signo
  def imm21(self, expr):
    val = int(expr.tail[0])
    if val < -1048576 or val > 1048575:
      raise ImmediateOutOfRangeError(f"Immediate value {val} out of range for 21-bit signed integer")
    
    if val < 0:
      val = (1 << 21) + val

    imm21Bin = format(val & 0x1fffff, '021b')  # Asegura que esté en 21 bits
    return imm21Bin
  
  #Método para convertir los inmediatos de 20 bits a binario sin signo
  def imm20(self, expr):
    val = int(expr.tail[0])
    if val < -524288 or val > 524287:
      raise ImmediateOutOfRangeError(f"Immediate value {val} out of range for 20-bit signed integer")
    
    if val < 0:
      val = (1 << 20) + val
    
    imm20Bin = format(val & 0xfffff, '020b')  # Asegura que esté en 20 bits
    return imm20Bin
  
  #Metodo para dividir el inmediato en 2 partes [4:0] y [11:5]
  def splitImmediate(self, expr):
    offset = expr.tail[2]
    imm = offset.tail[0]
    imm = imm.zfill(12)
    lsbImm = imm[-5:]
    msbImm = imm[:7]

    return lsbImm, msbImm
  
  #Metodo para dividir el inmediato de las instrucciones tipo J
  def immJ(self, expr):
    imm = expr.tail[2]
    imm = imm.zfill(21)
    imm20 = imm[0]
    imm10to1 = imm[10:20]
    imm11 = imm[9]
    imm19to12 = imm[1:9]

    return imm20, imm10to1, imm11, imm19to12
    

  #Imprime las instrucciones tipo R en binario
  def printRInstructionBIN(self, expr):
    inst = expr.tail[0]
    f7 = inst['f7']
    rs2 = expr.tail[3]
    rs1 = expr.tail[2]
    f3 = inst['f3']
    rd = expr.tail[1]
    opcode = inst['opcode']
    return f7 + rs2 + rs1 + f3 + rd + opcode
  
  #Imprime las instrucciones tipo R en hexadecimal
  def printRInstructionHEXA(self, expr):
    inst = expr.tail[0]
    f7 = inst['f7']
    rs2 = expr.tail[3]
    rs1 = expr.tail[2]
    f3 = inst['f3']
    rd = expr.tail[1]
    opcode = inst['opcode']
    return hex(int(f7 + rs2 + rs1 + f3 + rd + opcode, 2))
  
  #Imprime las intrucciones tipo I en binario
  def printIInstructionBIN(self, expr):
    inst = expr.tail[0]
    imm12 = expr.tail[3]
    rs1 = expr.tail[2]
    f3 = inst['f3']
    rd = expr.tail[1]
    opcode = inst['opcode']
    return imm12 + rs1 + f3 + rd + opcode
  
  #Imprime las instrucciones tipo I en hexadecimal
  def printIInstructionHEXA(self, expr):
    inst = expr.tail[0]
    imm12 = expr.tail[3]
    rs1 = expr.tail[2]
    f3 = inst['f3']
    rd = expr.tail[1]
    opcode = inst['opcode']
    return hex(int(imm12 + rs1 + f3 + rd + opcode, 2))
  
  #Imprime las intrucciones tipo I de corrimiento en binario
  def printIsInstructionBIN(self, expr):
    inst = expr.tail[0]
    imm7 = inst['imm7']
    shamt = expr.tail[3]
    rs1 = expr.tail[2]
    f3 = inst['f3']
    rd = expr.tail[1]
    opcode = inst['opcode']
    return imm7 + shamt + rs1 + f3 + rd + opcode
  
  #Imprime las instrucciones tipo I de corrimiento en hexadecimal
  def printIsInstructionHEXA(self, expr):
    inst = expr.tail[0]
    imm7 = inst['imm7']
    shamt = expr.tail[3]
    rs1 = expr.tail[2]
    f3 = inst['f3']
    rd = expr.tail[1]
    opcode = inst['opcode']
    return hex(int(imm7 + shamt + rs1 + f3 + rd + opcode, 2))
  
  #Imprime las instrucciones tipo I de carga en binario
  def printIlInstructionBIN(self, expr):
    inst = expr.tail[0]
    offset = expr.tail[2]
    imm = offset.tail[0]
    rs1 = offset.tail[1]
    f3 = inst['f3']
    rd = expr.tail[1]
    opcode = inst['opcode']
    return imm + rs1 + f3 + rd + opcode
  
  #Imprime las instrucciones tipo I de carga en hexadecimal
  def printIlInstructionHEXA(self, expr):
    inst = expr.tail[0]
    offset = expr.tail[2]
    imm = offset.tail[0]
    rs1 = offset.tail[1]
    f3 = inst['f3']
    rd = expr.tail[1]
    opcode = inst['opcode']
    return hex(int(imm + rs1 + f3 + rd + opcode, 2))

  #Imprime las instrucciones tipo S en binario
  def printSInstructionBIN(self, expr):
    inst = expr.tail[0]
    rs2 = expr.tail[1]
    offset = expr.tail[2]
    imm5, imm7 = self.splitImmediate(expr)
    rs1 = offset.tail[1]
    f3 = inst['f3']
    opcode = inst['opcode']

    return imm7 + rs2 + rs1 + f3 + imm5 + opcode

  #Imprime las instrucciones tipo S en hexadecimal
  def printSInstructionHEXA(self, expr):
    inst = expr.tail[0]
    rs2 = expr.tail[1]
    offset = expr.tail[2]
    imm5, imm7 = self.splitImmediate(expr)
    rs1 = offset.tail[1]
    f3 = inst['f3']
    opcode = inst['opcode']

    return hex(int(imm7 + rs2 + rs1 + f3 + imm5 + opcode, 2)) 

  #Imprime las instrucciones tipo J en binario
  def printJInstructionBIN(self, expr):
    inst = expr.tail[0]
    imm20, imm10to1, imm11, imm19to12 = self.immJ(expr)
    rd = expr.tail[1]
    opcode = inst['opcode']

    return imm20 + imm10to1 + imm11 + imm19to12 + rd + opcode

  #Imprime las instrucciones tipo J en hexadecimal
  def printJInstructionHEXA(self, expr):
    inst = expr.tail[0]
    imm20, imm10to1, imm11, imm19to12 = self.immJ(expr)
    rd = expr.tail[1]
    opcode = inst['opcode']

    return hex(int(imm20 + imm10to1 + imm11 + imm19to12 + rd + opcode, 2))

  #Imprime las instrucciones tipo U en binario
  def printUInstructionBIN(self, expr):
    inst = expr.tail[0]
    imm20 = expr.tail[2]
    rd = expr.tail[1]
    opcode = inst['opcode']

    return imm20 + rd + opcode
  
  #Imprime las instrucciones tipo U en hexadecimal
  def printUInstructionHEXA(self, expr):
    inst = expr.tail[0]
    imm20 = expr.tail[2]
    rd = expr.tail[1]
    opcode = inst['opcode']

    return hex(int(imm20 + rd + opcode, 2))
  
  def printIEcallInstructionBIN(self, expr):
    inst = expr.tail[0]
    opcode = inst['opcode']
    opcode = opcode.zfill(32)
    return opcode

  def printIEcallInstructionHEXA(self, expr):
    inst = expr.tail[0]
    opcode = inst['opcode']
    opcode = opcode.zfill(32)
    return hex(int(opcode, 2))
  
  def printIEbreakInstructionBIN(self, expr):
    inst = expr.tail[0]
    opcode = inst['opcode']
    opcode = opcode.zfill(20)
    f12 = inst['f12']

    return f12 + opcode
  
  def printIEbreakInstructionHEXA(self, expr):
    inst = expr.tail[0]
    opcode = inst['opcode']
    opcode = opcode.zfill(20)
    f12 = inst['f12']

    return hex(int(f12 + opcode, 2))

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

    elif inst['type'] == 'Il':
      print("imm12({})-rs1({})-f3({})-rd({})-opcode({})".format(expr.tail[2].tail[0], expr.tail[2].tail[1], inst['f3'], expr.tail[1], inst['opcode']))
      print(self.printIlInstructionBIN(expr))
      print(self.printIlInstructionHEXA(expr))

    elif inst['type'] == 'S':
      print("imm7({})-rs2({})-rs1({})-f3({})-imm5({})-opcode({})".format(self.splitImmediate(expr)[1], expr.tail[1], expr.tail[2].tail[1], inst['f3'], self.splitImmediate(expr)[0], inst['opcode']))
      print(self.printSInstructionBIN(expr))
      print(self.printSInstructionHEXA(expr))
    
    elif inst['type'] == 'J':
      print("imm21({})-rd({})-opcode({})".format(self.immJ(expr)[0] + self.immJ(expr)[1] + self.immJ(expr)[2] + self.immJ(expr)[3], expr.tail[1], inst['opcode']))
      print(self.printJInstructionBIN(expr))
      print(self.printJInstructionHEXA(expr))
    
    elif inst['type'] == 'U':
      print("imm20({})-rd({})-opcode({})".format(expr.tail[2], expr.tail[1], inst['opcode']))
      print(self.printUInstructionBIN(expr))
      print(self.printUInstructionHEXA(expr)) 

    elif inst['type'] == 'IEcall':
      print("opcode({})".format(inst['opcode']))
      print(self.printIEcallInstructionBIN(expr))
      print(self.printIEcallInstructionHEXA(expr))
    
    elif inst['type'] == 'IEbreak':
      print("f12({})-opcode({})".format(inst['f12'], inst['opcode']))
      print(self.printIEbreakInstructionBIN(expr))
      print(self.printIEbreakInstructionHEXA(expr))
  
          

# LLamada principal a la gramatica y al visitante
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