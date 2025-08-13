import math

def log_base(value, base):
    return math.log(value) / math.log(base)

def run_calculator():
    value = int(input("Enter the value: "))
    base = int(input("Enter the base: "))
    answer = log_base(value, base)
    print(f"log{base}({value}) = {answer}")

def main():
    run_calculator()

if __name__ == "__main__":
    main()
