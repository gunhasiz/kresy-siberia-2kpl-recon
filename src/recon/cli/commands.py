import typer

app = typer.Typer(help="Kresy-Siberia 2KPL Recon Tool")

@app.command()
def start(pages: int = 5):
    """Run the recon download process."""
    typer.echo(f"Rozpoczynam pobieranie danych.")

if __name__ == "__main__":
    app()