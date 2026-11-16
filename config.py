
"""
BASE_DIR	Корневая папка проекта
DATA_DIR	Папка с исходными CSV
REPORTS_DIR	Папка с результатами
LOGS_DIR	Папка с логами
REPORT_FILE	Имя итогового CSV
LOG_FILE	Имя файла ошибок
CSV_PATTERN	Поиск всех CSV-файлов
STATUS_COLUMN	Колонка со статусом
DELIVERED_STATUS	Статус доставленного заказа
AMOUNT_COLUMN	Колонка с суммой заказа
REQUIRED_COLUMNS	Колонки, необходимые для расчётов
"""

from pathlib import Path

# Корневая директория проекта
BASE_DIR = Path(__file__).resolve().parent

# Пути к папкам
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"

# Выходные файлы
REPORT_FILE = REPORTS_DIR / "summary_report.csv"
LOG_FILE = LOGS_DIR / "errors.log"

# Поиск CSV-файлов
CSV_PATTERN = "*.csv"

# Параметры фильтрации
STATUS_COLUMN = "status"
DELIVERED_STATUS = "Delivered"
AMOUNT_COLUMN = "total_amount"

# Ожидаемая структура CSV
REQUIRED_COLUMNS = [
    "order_id",
    "person_id",
    "order_date",
    "status",
    "total_amount",
    "currency",
    "payment_method",
    "shipping_method",
    "notes"
]
