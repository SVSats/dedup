import sys
from .core import find_duplicates, delete_duplicates

def main():
    if len(sys.argv) < 2:
        print("Uso: dedup-cli <ruta1> [ruta2 ...] [--delete] [--keep oldest|newest] [--report archivo] [--dry-run]")
        sys.exit(1)

    # Análisis simple de argumentos (sin argparse para mantenerlo liviano si se prefiere)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("rutas", nargs="+")
    parser.add_argument("--delete", action="store_true")
    parser.add_argument("--keep", choices=["newest", "oldest"], default="newest")
    parser.add_argument("--report")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    duplicates = find_duplicates(args.rutas)
    if not duplicates:
        print("✅ No se encontraron duplicados.")
        return

    report_lines = []
    for h, paths in duplicates.items():
        report_lines.append(f"\nHash: {h[:16]}...")
        for p in paths:
            report_lines.append(f"  {p}")
        keep = choose_to_keep(paths, args.keep)
        report_lines.append(f"  → Conservar: {keep}")

    report_text = "\n".join(report_lines)
    print(report_text)

    if args.report:
        with open(args.report, "w") as f:
            f.write(report_text)
        print(f"\n📄 Informe guardado en: {args.report}")

    if args.delete or args.dry_run:
        delete_duplicates(duplicates, strategy=args.keep, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
