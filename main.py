import sys
from dice import roll_from_string


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <dice_input>")
        print("Example: python main.py '2ca,2pe,3di,1be,2co'")
        sys.exit(1)

    dice_input = sys.argv[1]
    results, individual_rolls = roll_from_string(dice_input)

    print("Individual Rolls:")
    for roll in individual_rolls:
        print(f"{roll['dice_type']}: {roll['result']}")

    print("\nFinal Results:")
    for symbol, count in results.items():
        print(f"{symbol}: {count}")


if __name__ == "__main__":
    main()
