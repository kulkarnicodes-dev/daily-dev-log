import re


def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))


if __name__ == "__main__":
    email = input("Enter your email: ")

    if is_valid_email(email):
        print("✅ Valid email address")
    else:
        print("❌ Invalid email address")
