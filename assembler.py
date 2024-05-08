import plyplus
import sys

regNames = {
  'zero': 0,
  'ra': 1,
  'x0': 0, 
  'x1': 1,
  'x2': 2,
  'x2': 2,
  'x3': 3,
  'x4': 4,
  'x5': 5,
  'x6': 6,
  'x7': 7,
  'x8': 8,
  'x9': 9,
  'x10': 10, 
  'x11': 11,
  'x12': 12,
  'x12': 12,
  'x13': 13,
  'x14': 14,
  'x15': 15,
  'x16': 16,
  'x17': 17,
  'x18': 18,
  'x19': 19,
  'x20': 20, 
  'x21': 21,
  'x22': 22,
  'x22': 22,
  'x23': 23,
  'x24': 24,
  'x25': 25,
  'x26': 26,
  'x27': 27,
  'x28': 28,
  'x29': 29,
  'x30': 30,
  'x31': 31
}

instInfo = {
  'add': {
    'opcode': '0110011',
    'f3': '000',
    'f7': '0000000'
  }
}

class HVisitor(plyplus.STransformer):
  def __init__(self):
    super().__init__()
    self.instructionCounter = 0
    self.labels = {}
  def label(self, expr):
    self.labels[expr.tail[0]] = self.instructionCounter + 4
  def program(self, expr):
    print("Nodo programa")
    print(self.instructionCounter)
    print(expr)
    
  def regname(self, expr):
    val = expr.tail[0]
    regNum = regNames[val]
    regBin = format(int(regNum),'05b')
    return regBin
  
  def instr(self, expr):
    # Instruction name
    inst =  expr.tail[0]
  
    return {
      'opcode': instInfo[inst]['opcode'],
      'f3': instInfo[inst]['f3'],
      'f7': instInfo[inst]['f7']
    }
    
  def imm(self, expr):
    val = expr.tail[0]
    print("sextend(" + val +")", end='')

  def inst(self, expr):
    print("Expresion en inst: ", expr)
    print("-{}--".format(self.instructionCounter))
    self.instructionCounter = self.instructionCounter + 4
    
    #print("opcode({})-rd({})-f3({})-rs1({})-rs2({})-f7({})".format(expr.tail[0]['opcode'], expr.tail[1],expr.tail[0]['f3'] ,expr.tail[2],expr.tail[3],expr.tail[0]['f7']))
    print("-xxx-")
    

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print("Example call: {} input.asm output.asm".format(sys.argv[0]))
  else:
    sourceFile = sys.argv[1]
    targetFile = sys.argv[2]
    with open('riscv.g', 'r') as grm:
      with open(sourceFile, 'r') as scode:
        parser = plyplus.Grammar(grm)
        source = scode.read();
        t = parser.parse(source)
        t.to_png_with_pydot(r"tree.png")
        v = HVisitor()
        v.transform(t)
        print(v.labels)