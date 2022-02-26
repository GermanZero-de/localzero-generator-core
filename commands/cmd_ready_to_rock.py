import subprocess


def cmd_ready_to_rock(args) -> None:
    try:
        subprocess.run(["pyright"])
        subprocess.run(["pytest"])
        subprocess.run(["pre-commit", "run", "-a"])
        rev = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True
        ).stdout.strip()
        print(
            f"You are ready to rock and save the climate at {rev}, but don't forget to copy paste the above into your pull request"
        )
    except:
        print("You are NOT ready yet. Fix your errors first!")
