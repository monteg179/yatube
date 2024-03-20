import csv
import os

from django.db import (
    models,
)


class CustomManager(models.Manager):

    def load_from_csv(self, file_name: str) -> None:
        if not os.path.exists(file_name):
            return
        with open(file_name) as file:
            reader = csv.DictReader(file)
            data = [self.model(**row) for row in reader]
            self.bulk_create(data)

    def save_to_csv(self, file_name: str) -> None:
        if hasattr(self.model, 'to_dict'):
            data = [instance.to_dict() for instance in self.all()]
        else:
            data = [element for element in self.all().values()]
        if not data:
            return
        with open(file_name, mode='w') as file:
            writer = csv.DictWriter(file, data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def clear(self) -> None:
        self.all().delete()
