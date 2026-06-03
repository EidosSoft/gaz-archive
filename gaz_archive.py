import zipfile
import os
from pathlib import Path

class GazArchive:
    def __init__(self, filename):
        self.filename = filename
        if not self.filename.lower().endswith('.gaz'):
            self.filename += '.gaz'

    def create_new(self, source_path):
        """Создаёт новый .gaz-архив из папки или файла."""
        with zipfile.ZipFile(self.filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if os.path.isfile(source_path):
                zipf.write(source_path, os.path.basename(source_path))
            elif os.path.isdir(source_path):
                for root, dirs, files in os.walk(source_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=source_path)
                        zipf.write(file_path, arcname)
        print(f"✅ Архив '{self.filename}' успешно создан!")

    def add_file_by_path(self, file_path):
        """Добавляет один файл в архив с проверкой на дубликаты."""
        if not os.path.exists(file_path):
            print(f"❌ Файл '{file_path}' не найден!")
            return False

        filename_in_archive = os.path.basename(file_path)

        # Проверяем, есть ли файл с таким именем в архиве
        try:
            with zipfile.ZipFile(self.filename, 'r') as zipf:
                if filename_in_archive in zipf.namelist():
                    print(f"⚠️  Файл '{filename_in_archive}' уже существует в архиве!")

            # Добавляем файл (если уже есть — перезаписываем)
            with zipfile.ZipFile(self.filename, 'a', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(file_path, filename_in_archive)
            print(f"✔️ Файл '{filename_in_archive}' добавлен/обновлён в '{self.filename}'")
            return True
        except Exception as e:
            print(f"❌ Ошибка при работе с архивом: {e}")
            return False

    def add_multiple_files(self, file_paths):
        """Добавляет несколько файлов в архив."""
        success_count = 0
        for file_path in file_paths:
            if self.add_file_by_path(file_path):
                success_count += 1
        print(f"✅ Всего добавлено/обновлено файлов: {success_count}/{len(file_paths)}")

    def extract_all(self, extract_to=None):
        """Извлекает все файлы из .gaz-архива."""
        if extract_to is None:
            extract_to = Path(self.filename).stem
        Path(extract_to).mkdir(exist_ok=True)

        with zipfile.ZipFile(self.filename, 'r') as zipf:
            zipf.extractall(extract_to)
        print(f"✅ Содержимое извлечено в папку: '{extract_to}'")

    def list_contents(self):
        """Показывает список файлов внутри .gaz-архива."""
        try:
            with zipfile.ZipFile(self.filename, 'r') as zipf:
                print(f"\n📁 Содержимое архива '{self.filename}':")
                for info in zipf.infolist():
                    print(f"  • {info.filename} ({info.file_size} байт)")
        except FileNotFoundError:
            print(f"❌ Архив '{self.filename}' не найден.")

def main():
    print("🎯 Менеджер .gaz-архивов")
    print("=" * 40)

    while True:
        print("\nВыберите действие:")
        print("1 — Создать новый .gaz-архив")
        print("2 — Добавить файл в существующий .gaz (указать путь)")
        print("3 — Добавить несколько файлов (пути через запятую)")
        print("4 — Извлечь содержимое .gaz-архива")
        print("5 — Посмотреть содержимое .gaz-архива")
        print("0 — Выход")

        choice = input("\nВаш выбор: ").strip()

        if choice == '0':
            print("👋 До свидания!")
            break

        elif choice == '1':
            filename = input("Введите имя архива (без расширения): ").strip()
            source_path = input("Введите полный путь к папке или файлу: ").strip()

            if not os.path.exists(source_path):
                print("❌ Указанный путь не существует!")
                continue

            archive = GazArchive(filename)
            archive.create_new(source_path)

        elif choice == '2':
            filename = input("Введите имя существующего .gaz-архива: ").strip()
            file_path = input("Введите полный путь к файлу для добавления: ").strip()

            if not filename.lower().endswith('.gaz'):
                filename += '.gaz'
            if not os.path.exists(filename):
                print(f"❌ Архив '{filename}' не найден!")
                continue

            archive = GazArchive(filename)
            archive.add_file_by_path(file_path)

        elif choice == '3':
            filename = input("Введите имя существующего .gaz-архива: ").strip()
            files_input = input("Введите пути к файлам через запятую: ").strip()
            file_paths = [p.strip() for p in files_input.split(',') if p.strip()]

            if not filename.lower().endswith('.gaz'):
                filename += '.gaz'
            if not os.path.exists(filename):
                print(f"❌ Архив '{filename}' не найден!")
                continue

            archive = GazArchive(filename)
            archive.add_multiple_files(file_paths)

        elif choice == '4':
            filename = input("Введите имя .gaz-архива для извлечения: ").strip()
            if not filename.lower().endswith('.gaz'):
                filename += '.gaz'

            if not os.path.exists(filename):
                print(f"❌ Архив '{filename}' не найден!")
                continue

            extract_to = input("Введите путь для извлечения (или оставьте пустым): ").strip()
            archive = GazArchive(filename)

            if extract_to:
                archive.extract_all(extract_to)
            else:
                archive.extract_all()

        elif choice == '5':
            filename = input("Введите имя .gaz-архива для просмотра: ").strip()
            if not filename.lower().endswith('.gaz'):
                filename += '.gaz'

            archive = GazArchive(filename)
            archive.list_contents()

        else:
            print("❌ Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
