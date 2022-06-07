from dataclasses import asdict
import typer

from cfpg.core import resolve_contest
import yaml

app = typer.Typer()


@app.command()
def contest_info(
    contest_str: str = typer.Argument(
        ...,
        help=(
            "Contest Identifier of form:\n"
            "- <global-id>: for any contest\n"
            "- CF-<relative-id>: for codeforces rounds\n"
            "- CF-<relative-id>(-DIV)?-<div>: for codeforces rounds with seperate divs\n"
            "- ECF-<relative-id>: for educational codeforces rounds\n"
            "- ECF-<relative-id>(-DIV)?-<div>: for educational codeforces rounds with seperate divs\n"
        ),
    )
):
    obj = asdict(resolve_contest(contest_str))
    del obj["durationSeconds"]
    del obj["startTimeSeconds"]
    del obj["relativeTimeSeconds"]
    print(yaml.safe_dump(obj))
