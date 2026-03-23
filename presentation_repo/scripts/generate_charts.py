#!/usr/bin/env python3
"""
Generate presentation charts from Vega-Lite specs.

Usage:
    python generate_charts.py

Requires: altair, vl-convert-python (for PNG export)

Note: Most presentation figures use the pre-generated publication PNGs
from paper/final_figures/. This script generates supplementary interactive
charts from the Vega-Lite specs in charts/chart_specs.json.
"""

import json
from pathlib import Path

try:
    import altair as alt
except ImportError:
    print("altair not installed. Install with: pip install altair vl-convert-python")
    print("Falling back to JSON spec output only.")
    alt = None


def load_specs(spec_file: str = "charts/chart_specs.json") -> list:
    """Load chart specifications from JSON."""
    repo_root = Path(__file__).parent.parent
    spec_path = repo_root / spec_file
    with open(spec_path) as f:
        data = json.load(f)
    return data["charts"]


def generate_charts(output_dir: str = "charts/output"):
    """Generate PNG charts from Vega-Lite specifications."""
    repo_root = Path(__file__).parent.parent
    out_path = repo_root / output_dir
    out_path.mkdir(parents=True, exist_ok=True)

    specs = load_specs()

    for chart_spec in specs:
        name = chart_spec["name"]
        print(f"Generating: {name}")

        if alt is not None:
            chart = alt.Chart.from_dict(chart_spec["spec"])
            # Save as HTML (interactive)
            chart.save(str(out_path / f"{name}.html"))
            # Try PNG export
            try:
                chart.save(str(out_path / f"{name}.png"), scale_factor=2)
                print(f"  Saved: {name}.png and {name}.html")
            except Exception as e:
                print(f"  PNG export failed ({e}), saved HTML only")
        else:
            # Save raw spec
            with open(out_path / f"{name}.json", "w") as f:
                json.dump(chart_spec["spec"], f, indent=2)
            print(f"  Saved: {name}.json (install altair for rendered output)")


def symlink_paper_figures(figures_dir: str = "../paper/final_figures"):
    """Create symlinks to paper figures for easy access."""
    repo_root = Path(__file__).parent.parent
    source = repo_root / figures_dir
    target = repo_root / "figures"

    if not source.exists():
        print(f"Source directory not found: {source}")
        return

    if target.exists():
        print(f"Figures directory already exists: {target}")
        return

    target.symlink_to(source.resolve())
    print(f"Created symlink: {target} -> {source}")


if __name__ == "__main__":
    print("=== QPCA-EnDCF Presentation Chart Generator ===\n")
    generate_charts()
    print("\nDone. Publication figures are in ../paper/final_figures/")
