import csv
import json
from django.core.management.base import BaseCommand
from onlysands.models import Beach

class Command(BaseCommand):
    help = "Import beaches from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        with open(csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Convert string fields that should be lists
                row["beach_type"] = row["beach_type"].split(', ')
                row["tags"] = row["tags"].split(', ')
                row["vibe"] = row["vibe"].split(', ')
                row["related_walks"] = row["related_walks"].split(', ')
                row["other_names"] = row["other_names"].split(', ')

                Beach.objects.create(
                    name=row["\ufeffname"],
                    location=row.get("location") or None,
                    suburb=row.get("suburb") or None,
                    beach_type=row["beach_type"],
                    rating=int(row["rating"]) if row["rating"] else None,
                    return_visit=row["return_visit"].lower() == "yes",
                    tags=row["tags"],
                    vibe=row["vibe"],
                    review=row.get("review") or None,
                    related_walks=row["related_walks"],
                    visited=row["visited"].lower() == "visited",
                    other_names=row.get("other_names"),
                    latitude=float(row["latitude"]),
                    longitude=float(row["longitude"]),
                )

        self.stdout.write(self.style.SUCCESS("Successfully imported beaches!"))
