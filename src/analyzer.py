import logging
import pandas as pd

from config import (
    DATA_DIR,
    REPORTS_DIR,
    LOGS_DIR,
    REPORT_FILE,
    LOG_FILE,
    CSV_PATTERN,
    STATUS_COLUMN,
    DELIVERED_STATUS,
    AMOUNT_COLUMN,
    REQUIRED_COLUMNS
)


class OrderAnalyzer:

    def __init__(self):
        self.successful_files = 0
        self.failed_files = 0
        self.total_files = 0
        self.results = []

        self.setup_logging()

    def setup_logging(self):
        """Настраивает запись ошибок в лог-файл."""

        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger("OrderAnalyzer")
        self.logger.setLevel(logging.ERROR)
        self.logger.propagate = False

        if not self.logger.handlers:
            file_handler = logging.FileHandler(
                LOG_FILE,
                encoding="utf-8"
            )

            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )

            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def load_file(self, file_path):
        """Загружает CSV-файл и проверяет его структуру."""

        df = pd.read_csv(
            file_path,
            on_bad_lines="error"
        )

        if df.empty:
            raise ValueError("Файл пуст или не содержит записей")

        # Проверяем соответствие структуры CSV
        actual_columns = set(df.columns)
        required_columns = set(REQUIRED_COLUMNS)

        if actual_columns != required_columns:
            missing_columns = required_columns - actual_columns
            extra_columns = actual_columns - required_columns

            error_message = []

            if missing_columns:
                error_message.append(
                    f"Отсутствуют колонки: {sorted(missing_columns)}"
                )

            if extra_columns:
                error_message.append(
                    f"Лишние колонки: {sorted(extra_columns)}"
                )

            raise ValueError("; ".join(error_message))

        # Проверяем числовые значения суммы заказа
        amounts = pd.to_numeric(
            df[AMOUNT_COLUMN],
            errors="coerce"
        )

        if amounts.isna().any():
            raise ValueError(
                f"Колонка {AMOUNT_COLUMN} содержит нечисловые значения"
            )

        df[AMOUNT_COLUMN] = amounts

        return df

    def filter_delivered_orders(self, df):
        """Оставляет только доставленные заказы."""

        delivered_orders = df[
            df[STATUS_COLUMN] == DELIVERED_STATUS
        ]

        return delivered_orders

    def calculate_metrics(self, df):
        """Рассчитывает метрики доставленных заказов."""

        order_count = len(df)

        total_revenue = df[AMOUNT_COLUMN].sum()

        average_check = (
            df[AMOUNT_COLUMN].mean()
            if order_count > 0
            else 0
        )

        return {
            "total_revenue": total_revenue,
            "average_check": average_check,
            "order_count": order_count
        }

    def process_file(self, file_path):
        """Обрабатывает один CSV-файл."""

        try:
            # Загружаем данные
            df = self.load_file(file_path)

            # Фильтруем доставленные заказы
            delivered_orders = self.filter_delivered_orders(df)

            # Рассчитываем метрики
            metrics = self.calculate_metrics(delivered_orders)

            # Добавляем название файла
            result = {
                "file_name": file_path.name,
                **metrics
            }

            self.successful_files += 1

            return result

        except Exception as error:
            self.logger.error(
                "Ошибка обработки файла %s: %s",
                file_path.name,
                error
            )

            self.failed_files += 1

            return None

    def process_all_files(self):
        """Обрабатывает все CSV-файлы в папке data."""

        # Создаём необходимые папки
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        # Находим все CSV-файлы
        csv_files = sorted(DATA_DIR.glob(CSV_PATTERN))

        self.total_files = len(csv_files)
        self.successful_files = 0
        self.failed_files = 0
        self.results = []

        # Обрабатываем файлы по очереди
        for file_path in csv_files:
            result = self.process_file(file_path)

            if result is not None:
                self.results.append(result)

        # Формируем общий отчёт
        report_columns = [
            "file_name",
            "total_revenue",
            "average_check",
            "order_count"
        ]

        report = pd.DataFrame(
            self.results,
            columns=report_columns
        )

        # Сохраняем отчёт
        report.to_csv(
            REPORT_FILE,
            index=False
        )

        return report
