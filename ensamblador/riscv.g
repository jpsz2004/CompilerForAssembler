start: program;

program:
  inst+;

inst: 
    instr  regname ',' regname ',' regname 
  | insti  regname ',' regname ',' imm12
  | instis regname ',' regname ',' imm5     
  | instil regname ',' offset
  | insts regname ',' offset
  | instb regname ',' regname ',' imm12
  | instj  regname ',' imm21
  | instu regname ',' imm20
  | instiecall | instiebreak;

offset: imm12 '\(' regname '\)';

instr: 'add' | 'sub' | 'xor' | 'or' | 'and'
       | 'sll' | 'srl' | 'sra' | 'slt' | 'sltu';

insti: 'addi' | 'xori' | 'ori' | 'andi'
       | 'slti' | 'sltiu' ;

instis: 'slli' | 'srli' | 'srai';

instil: 'lw' | 'lh' | 'lb' | 'lbu' | 'lhu' | 'jalr';

insts: 'sb' | 'sh' | 'sw';

instb: 'beq' | 'bne' | 'blt' | 'bge' | 'bltu' | 'bgeu';

instj: 'jal';

instu: 'lui' | 'auipc';

instiecall: 'ecall';
instiebreak: 'ebreak';

imm12 : VAL;
imm5 : VAL;
imm21 : VAL;
imm20: VAL;

VAL: '[0]|(\-|\+)?[1-9][0-9]*';

regname: 
   'x0'  | 'zero'
  | 'x1' | 'ra'
  | 'x2' | 'sp' 
  | 'x3' | 'gp' 
  | 'x4' | 'tp' 
  | 'x5' | 't0' 
  | 'x6' | 't1' 
  | 'x7' | 't2' 
  | 'x8' | 's0' | 'fp' 
  | 'x9' | 's1' 
  | 'x10' | 'a0'
  | 'x11' | 'a1'
  | 'x12' | 'a2'
  | 'x13' | 'a3' 
  | 'x14' | 'a4'
  | 'x15' | 'a5'
  | 'x16' | 'a6'
  | 'x17' | 'a7'
  | 'x18' | 's2'
  | 'x19' | 's3'
  | 'x20' | 's4'
  | 'x21' | 's5'
  | 'x22' | 's6'
  | 'x23' | 's7'
  | 'x24' | 's8'
  | 'x25' | 's9'
  | 'x26' | 's10'
  | 'x27' | 's11'
  | 'x28' | 't3'
  | 'x29' | 't4'
  | 'x30' | 't5'
  | 'x31' | 't6';

COMMENT: ';' '.*' (%ignore);
WS: '[ \t\r\n]+' (%ignore);
