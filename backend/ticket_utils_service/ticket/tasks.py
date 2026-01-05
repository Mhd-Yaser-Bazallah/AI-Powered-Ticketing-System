import logging
import subprocess
import sys
from pathlib import Path

import pandas as pd
from celery import shared_task
from django.conf import settings
from django.db import transaction

from ticket.models import AnalyzeCounter, Ticket


logger = logging.getLogger(__name__)


@shared_task(bind=True)
def export_tickets_and_retrain(self):
    export_path = Path(settings.TRAINING_EXPORT_PATH)
    training_dir = Path(settings.TRAINING_DATA_DIR)
    sheet_name = settings.TRAINING_EXPORT_SHEET_NAME

    try:
        export_path.parent.mkdir(parents=True, exist_ok=True)
        if export_path.exists():
            export_path.unlink()

        tickets = list(Ticket.objects.all().values_list("document", "topic_group"))
        df = pd.DataFrame(tickets, columns=["Document", "Topic_group"])
        df.to_excel(export_path, index=False, sheet_name=sheet_name)
        logger.info("Exported %s tickets to %s", len(df), export_path)

        training_dir.mkdir(parents=True, exist_ok=True)
        df = df.dropna(subset=["Document", "Topic_group"])
        if df.empty:
            raise ValueError("No tickets available for training after filtering.")

        full_csv_path = training_dir / "all_tickets_processed_improved_v3.csv"
        df.to_csv(full_csv_path, index=False)
        logger.info("Wrote full training CSV: %s (rows=%s)", full_csv_path, len(df))

        logger.info("Splitting training data: %s", training_dir)
        subprocess.run([sys.executable, "Splitting.py"], cwd=training_dir, check=True)

        logger.info("Starting training pipeline: %s", training_dir)
        subprocess.run([sys.executable, "train_bert.py"], cwd=training_dir, check=True)
        logger.info("Training pipeline finished successfully.")

        with transaction.atomic():
            counter, _ = AnalyzeCounter.objects.select_for_update().get_or_create(pk=1)
            counter.is_training = False
            counter.last_error = None
            counter.save(update_fields=["is_training", "last_error", "updated_at"])
    except Exception as exc:
        logger.exception("Training pipeline failed: %s", exc)
        with transaction.atomic():
            counter, _ = AnalyzeCounter.objects.select_for_update().get_or_create(pk=1)
            counter.is_training = False
            counter.last_error = str(exc)
            counter.save(update_fields=["is_training", "last_error", "updated_at"])
        raise
