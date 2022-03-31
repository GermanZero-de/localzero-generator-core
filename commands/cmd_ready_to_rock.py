import subprocess


def cmd_ready_to_rock(args) -> None:
    try:
        subprocess.run(["poetry", "run", "pyright"], check=True)
        subprocess.run(["poetry", "run", "pytest"], check=True)
        subprocess.run(["poetry", "run", "pre-commit", "run", "-a"], check=True)
        rev = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip()
        print(
            f"You are ready to rock and save the climate at {rev}, but don't forget to copy paste the above into your pull request"
        )
    except Exception as e:
        print("You are NOT ready yet. Fix your errors first!")
        print(e)
