from src.analyzer import OrderAnalyzer


def main():
    analyzer = OrderAnalyzer()

    analyzer.process_all_files()

    print(f"Обработано файлов: {analyzer.successful_files}")
    print(f"Файлов с ошибками: {analyzer.failed_files}")


if __name__ == "__main__":
    main()
