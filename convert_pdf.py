from pathlib import Path
from PIL import Image
import fitz  # PyMuPDF


def clean_filename(filename):
    """Очищает имя файла, заменяя пробелы и специальные символы на '_'."""
    return ''.join([char if char.isalnum() else '_' for char in filename])


def convert_pdf_to_png(input_pdf_path, output_folder='сertificates_png'):
    print(f"Обработка файла: {pdf_file.name}")

    input_pdf_path = Path(input_pdf_path)
    output_folder = Path(output_folder)

    # Создаем папку для вывода, если она еще не существует
    output_folder.mkdir(parents=True, exist_ok=True)

    # Чистим имя файла
    cleaned_filename = clean_filename(input_pdf_path.stem)

    try:
        doc = fitz.open(str(input_pdf_path))
    except Exception as e:
        print(f"Ошибка открытия PDF: {e}")
        return

    for page_number, page in enumerate(doc.pages(), start=1):
        zoom_x = 2.0  # Масштаб по горизонтали
        zoom_y = 2.0  # Масштаб по вертикали

        # Извлекаем картинку из страницы PDF
        matrix = fitz.Matrix(zoom_x, zoom_y)
        pix = page.get_pixmap(matrix=matrix)

        # Формируем название выходного PNG-файла
        output_png_name = f"{cleaned_filename}.png"
        output_png_path = output_folder / output_png_name

        # Сохраняем изображение
        pix.save(str(output_png_path))

        print(f"Создано изображение: {output_png_path.name}\n")


if __name__ == "__main__":
    # Указываем путь к папке с сертификатами
    certificates_dir = Path("certificates")

    # Перебираем все PDF-файлы в папке
    for pdf_file in certificates_dir.glob('*.pdf'):
        convert_pdf_to_png(pdf_file)