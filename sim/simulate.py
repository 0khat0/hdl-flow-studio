import json
import argparse
import re
import os

def parse_vhdl_logic(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    match = re.search(r'(?P<target>\w+)\s*<=\s*(.+?);', content)
    if not match:
        raise ValueError("No logic assignment found in VHDL.")

    target = match.group("target")
    expression = match.group(2).strip()
    return target, expression


def simulate_logic(expression, inputs):
    expr = expression
    for k, v in inputs.items():
        expr = re.sub(r'\b{}\b'.format(k), v, expr)

    expr = expr.replace("and", " and ")
    expr = expr.replace("or", " or ")
    expr = expr.replace("not", " not ")
    expr = expr.replace("xor", "^")

    try:
        result = str(int(eval(expr)))
    except Exception as e:
        result = "error"
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    args = parser.parse_args()

    base_name = os.path.splitext(os.path.basename(args.file))[0]
    vhdl_path = args.file
    test_path = f'tests/{base_name}_tests.json'
    output_path = f'reports/simulation_output.txt'

    target, expression = parse_vhdl_logic(vhdl_path)

    with open(test_path, 'r') as f:
        test_vectors = json.load(f)

    results = []
    for vec in test_vectors:
        sim_out = simulate_logic(expression, vec)
        expected = vec.get(f"expected_{target}", "X")  # Updated here
        status = "PASS" if sim_out == expected else "FAIL"
        results.append(f"a={vec['a']} b={vec['b']} -> {target}={sim_out} (expected: {expected}) {status}")

    pass_count = sum(1 for line in results if "PASS" in line)
    total = len(results)
    results.append(f"{pass_count}/{total} tests passed")

    with open(output_path, 'a', encoding='utf-8') as f:
        f.write(f"\n===== Simulation: {base_name} =====\n")
        for line in results:
            f.write(line + '\n')

    print(f"Simulation complete. Results saved to {output_path}")

if __name__ == "__main__":
    main()
