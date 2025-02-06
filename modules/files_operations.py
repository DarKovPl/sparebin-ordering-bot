from configuration.settings import (
    SPARE_BIN_ORDER_CSV_URL,
    IN_CSV_DATA_FILE_PATH,
    SCREENSHOTS_FOLDER_PATH,
    OUTPUT_DATA_FOLDER_PATH,
    OUT_PDF_FILE_PATH,
    FILES_DATE,
    ZIP_FILE_PATH
)

from RPA.HTTP import HTTP
from RPA.Tables import Tables
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import shutil
import zipfile
import os


def download_file():
    print("Downloading the CSV file with the orders")

    http = HTTP()
    http.download(
        SPARE_BIN_ORDER_CSV_URL, 
        overwrite=True, 
        target_file=IN_CSV_DATA_FILE_PATH
    )

def get_csv_data():
    print("Getting the csv data from the business file")

    lib = Tables()
    csv_data = lib.read_table_from_csv(path=IN_CSV_DATA_FILE_PATH, header=True)
    return csv_data

def store_receipt_as_pdf(image_size, image_path, receipt_data, row, transaction_no):
    print("Storing the receipt with an image as a PDF file")

    pdf_filename = OUT_PDF_FILE_PATH.replace('$placeholder', f"{transaction_no}_{row['Order number']}_{FILES_DATE}")
    pdf = SimpleDocTemplate(pdf_filename, pagesize=A4)

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']

    elements = []

    elements.append(Paragraph("Robot Order Receipt", title_style))
    elements.append(Spacer(1, 12))

    img_width = image_size["width"]
    img_height = image_size["height"]
    max_width = 220
    scale_factor = max_width / img_width
    scaled_width = int(img_width * scale_factor)
    scaled_height = int(img_height * scale_factor)

    robot_image = Image(image_path, width=scaled_width, height=scaled_height)
    elements.append(robot_image)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"<b>Order Number:</b> {receipt_data['order_number']}", normal_style))
    elements.append(Paragraph(f"<b>Timestamp:</b> {receipt_data['timestamp']}", normal_style))
    elements.append(Spacer(1, 12))

    parts_data = [["Part", "Selected Option"]]
    for key, value in receipt_data["parts"].items():
        parts_data.append([key, value])

    table = Table(parts_data, colWidths=[150, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"<b>Confirmation:</b> {receipt_data['confirmation_message']}", normal_style))
    elements.append(Spacer(1, 20))

    pdf.build(elements)
    print(f"PDF saved as {pdf_filename}")


def zip_folders():
    print("Creating ZIP archive of the receipts and the images")

    results_pdfs_folders = next(
        (f for f in os.listdir(OUTPUT_DATA_FOLDER_PATH) if f.startswith("results_pdfs_")), 
        None
    )
    folders_to_zip = [SCREENSHOTS_FOLDER_PATH, os.path.join(OUTPUT_DATA_FOLDER_PATH, results_pdfs_folders)]
    
    with zipfile.ZipFile(ZIP_FILE_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder in folders_to_zip:
            for root, _, files in os.walk(folder):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, start=os.path.dirname(folder))
                    zipf.write(full_path, arcname=arcname)

    print(f"ZIP file created: {ZIP_FILE_PATH}")

    return folders_to_zip

def delete_after_zip_folders(folders_to_delete):
    print("Deleting folders after zip...")

    for folder in folders_to_delete:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Deleted: {folder}")
        else:
            print(f"Folder not found: {folder}")

    print("Cleanup completed.")
    