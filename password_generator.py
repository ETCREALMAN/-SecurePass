import random
import string
import pyperclip

def generate_password(length=12, use_upper=True, use_digits=True, use_symbols=True):
    characters = string.ascii_lowercase
    guaranteed = []

    if use_upper:
        characters += string.ascii_uppercase
        guaranteed.append(random.choice(string.ascii_uppercase))
    if use_digits:
        characters += string.digits
        guaranteed.append(random.choice(string.digits))
    if use_symbols:
        characters += string.punctuation
        guaranteed.append(random.choice(string.punctuation))

    remaining = length - len(guaranteed)
    password_list = guaranteed + [random.choice(characters) for _ in range(remaining)]
    random.shuffle(password_list)
    return ''.join(password_list)

def check_strength(password):
    score = 0
    tips = []

    if len(password) >= 12:
        score += 1
    else:
        tips.append("Use at least 12 characters")

    if any(c.isupper() for c in password):
        score += 1
    else:
        tips.append("Add uppercase letters")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        tips.append("Add numbers")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        tips.append("Add special symbols (!@#$...)")

    labels = {4: "💪 Very Strong", 3: "✅ Strong", 2: "⚠️  Medium", 1: "❌ Weak", 0: "❌ Very Weak"}
    return labels.get(score, "❌ Very Weak"), tips

def get_yes_no(prompt):
    while True:
        answer = input(prompt + " (y/n): ").strip().lower()
        if answer in ('y', 'n'):
            return answer == 'y'
        print("Please enter y or n.")

def main():
    print("=" * 50)
    print("       🔐 SecurePass — Password Generator")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("  1. Generate a new password")
        print("  2. Check strength of your own password")
        print("  3. Exit")

        choice = input("\nChoose (1/2/3): ").strip()

        if choice == "1":
            try:
                length = int(input("Password length (min 8, recommended 16): ") or 16)
                length = max(8, min(length, 128))
            except ValueError:
                length = 16

            use_upper   = get_yes_no("Include uppercase letters?")
            use_digits  = get_yes_no("Include numbers?")
            use_symbols = get_yes_no("Include symbols (!@#$...)?")

            password = generate_password(length, use_upper, use_digits, use_symbols)
            strength, tips = check_strength(password)

            print(f"\n✨ Generated Password: {password}")
            print(f"   Strength: {strength}")

            if tips:
                print("   Tips to improve:", ", ".join(tips))

            try:
                pyperclip.copy(password)
                print("   📋 Copied to clipboard!")
            except Exception:
                print("   (Install pyperclip to enable clipboard copy)")

            save = get_yes_no("\nSave this password to a file?")
            if save:
                label = input("Label for this password (e.g. Gmail): ").strip() or "Unnamed"
                with open("saved_passwords.txt", "a") as f:
                    f.write(f"{label}: {password}\n")
                print("   💾 Saved to saved_passwords.txt")

        elif choice == "2":
            pwd = input("Enter your password to check: ")
            strength, tips = check_strength(pwd)
            print(f"\n   Strength: {strength}")
            if tips:
                print("   Suggestions:")
                for tip in tips:
                    print(f"     • {tip}")

        elif choice == "3":
            print("\n👋 Stay secure, Radin!\n")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
