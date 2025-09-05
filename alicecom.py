# тестовая cli допилить автоматическую настройку pip в global и сами команды

import typer
import subprocess

app = typer.Typer()

COMPOSE_FILE = "docker-compose.yml"


def run(cmd):
    subprocess.run(cmd, shell=True, check=True)


@app.command()
def start():
    run(f"docker compose -f {COMPOSE_FILE} up -d")


@app.command()
def stop():
    run(f"docker compose -f {COMPOSE_FILE} down")


@app.command()
def restart():
    run(f"docker compose -f {COMPOSE_FILE} down")
    run(f"docker compose -f {COMPOSE_FILE} up -d")


@app.command()
def build(clean: bool = False):
    cmd = "docker compose -f docker-compose.build-images.yml build --push"
    if clean:
        cmd += " --no-cache"
    run(cmd)


if __name__ == "__main__":
    app()
