import typer
import asyncio

from recon.core.scraper.engine import main as scraper_main

app = typer.Typer(help="Kresy-Siberia 2KPL Recon Tool")

@app.command()
def start(pages: int = 5):
    """Run the recon download process."""
    typer.echo(f"Starting data collection.")
    asyncio.run(scraper_main())

if __name__ == "__main__":
    app()