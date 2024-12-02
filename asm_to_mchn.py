# Mapping for instructions and registers# Correct mapping for opcode based on sequence
sequence = 'AMEDOFNJBKCHPLIG'
opcode_map = {sequence[i]: format(i, '04b') for i in range(len(sequence))}

# Check the mapping for correctnes
register_map = {
    '$zero': '0000', '$t0': '0111', '$t1': '0001', '$t2': '0010',
    '$t3': '0011', '$t4': '0100', '$sp': '0110'
}

# Mapping instructions to their respective sequence IDs
instruction_ids = {
    'add': 'A', 'addi': 'B', 'sub': 'C', 'subi': 'D',
    'and': 'E', 'andi': 'F', 'or': 'G', 'ori': 'H',
    'sll': 'I', 'srl': 'J', 'nor': 'K', 'sw': 'L',
    'lw': 'M', 'beq': 'N', 'bneq': 'O', 'j': 'P'
}

def convert_to_machine_code(assembly_code):
    machine_codes = []
    for line in assembly_code:
        # Split the instruction into parts
        parts = line.replace(',', '').split()
        instruction = parts[0].lower()  # Convert instruction to lowercase
        if instruction not in instruction_ids:
            print("...................................")
            print(instruction)
            raise ValueError(f"Unknown instruction: {instruction}")
        
        opcode_id = instruction_ids[instruction]
        print(opcode_id)
        opcode = opcode_map[opcode_id]
        print(opcode)
        if opcode_id in 'ACGKE':  # R-type
            _, rd, rs, rt = parts
            rd_bin = register_map[rd]
            rs_bin = register_map[rs]
            rt_bin = register_map[rt]
            shamt = '0000'
            machine_code = f"{opcode}{rs_bin}{rt_bin}{rd_bin}{shamt}"
        elif opcode_id in 'BFHILMNDJO':  # I-type
            if opcode_id in ['B', 'F', 'H', 'I','D','J']:  # addi, andi, ori, sll,subi,srl
                _, rt, rs, imm = parts
            elif opcode_id in ['L', 'M']:  # sw, lw
                _, rt, imm_rs = parts
                rt, rs,imm = rt, imm_rs.split('(')[1][:-1], imm_rs.split('(')[0][:]
            else:  # beq, bneq
                _, rs, rt, imm = parts
            rt_bin = register_map[rt]
            rs_bin = register_map[rs]
            imm_bin = format(int(imm), '08b')
            machine_code = f"{opcode}{rs_bin}{rt_bin}{imm_bin}"
        elif opcode_id == 'P':  # J-type
            _, target = parts
            target_bin = format(int(target), '08b')# 8-bit target address
            print(target_bin)
            machine_code = f"{opcode}{target_bin}00000000"
        else:
            raise ValueError(f"Unsupported instruction ID: {opcode_id}")
        
        machine_codes.append(machine_code)
    
    return machine_codes

def write_to_file(machine_codes, file_name="machine_code.txt"):
    with open(file_name, "w") as file:
        file.write("v2.0 raw\n")
        for binary_code in machine_codes:
            hex_code = f"{int(binary_code, 2):05X}"  # Ensure 8 hexadecimal digits
            file.write(hex_code + " ")

# Sample input (list of MIPS assembly lines)
assembly_code = [
    "beq $t0, $t1, 5",
    "addi $t0, $zero, 5",
    "add $t1, $t0, $t2",
    "sub $t2, $t1, $t3",
    "subi $t1, $t2, 3",
    "and $t3, $t1, $t2",
    "addi $t4, $t3, 7",
    "or $t4, $t3, $t2",
    "ori $t4, $t3, 7",
    "sll $t4, $t4, 2",
    "srl $t4, $t4, 2",
    "nor $t4, $t3, $t2",
    "sw $t4, 4($sp)",
    "lw $t4, 4($sp)",
    "addi $t3, $t3, 125",
    "beq $t4, $t3, 1",
    "j 10",
    "bneq $t4, $t3, 1"
    

]

# Convert to machine code
machine_code_output = convert_to_machine_code(assembly_code)
write_to_file(machine_code_output)
# Display results
print("Assembly Code -> Machine Code:")
for asm, mc in zip(assembly_code, machine_code_output):
    print(f"{asm} -> {mc}")
