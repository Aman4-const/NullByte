import argparse
import re


def assess_password_strength(password: str) -> dict:
    length_score = len(password) >= 8
    upper_score = bool(re.search(r"[A-Z]", password))
    lower_score = bool(re.search(r"[a-z]", password))
    digit_score = bool(re.search(r"\d", password))
    special_score = bool(re.search(r"[^A-Za-z0-9]", password))

    score = sum([length_score, upper_score, lower_score, digit_score, special_score])

    if score <= 2:
        strength = "Weak"
    elif score == 3 or score == 4:
        strength = "Moderate"
    else:
        strength = "Strong"

    return {
        "length": length_score,
        "uppercase": upper_score,
        "lowercase": lower_score,
        "numbers": digit_score,
        "special_chars": special_score,
        "score": score,
        "strength": strength
    }


def main():
    parser = argparse.ArgumentParser(description="Assess the strength of a password.")
    parser.add_argument("password", help="The password to assess")
    args = parser.parse_args()

    result = assess_password_strength(args.password)

    print("Password strength assessment:")
    print(f"Length >= 8: {'✔' if result['length'] else '✘'}")
    print(f"Contains uppercase: {'✔' if result['uppercase'] else '✘'}")
    print(f"Contains lowercase: {'✔' if result['lowercase'] else '✘'}")
    print(f"Contains number: {'✔' if result['numbers'] else '✘'}")
    print(f"Contains special character: {'✔' if result['special_chars'] else '✘'}")
    print(f"Overall score: {result['score']} / 5")
    print(f"Strength: {result['strength']}")


if __name__ == "__main__":
    main()
