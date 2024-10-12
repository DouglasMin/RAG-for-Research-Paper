import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf_path, output_folder):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the input PDF file
    reader = PdfReader(input_pdf_path)

    # Iterate over each page
    for page_number in range(len(reader.pages)):
        writer = PdfWriter()
        writer.add_page(reader.pages[page_number])

        # Define the output file path
        output_pdf_path = os.path.join(output_folder, f'page_{page_number + 1}.pdf')

        # Write the single page to a new PDF file
        with open(output_pdf_path, 'wb') as output_pdf_file:
            writer.write(output_pdf_file)

        print(f'Saved: {output_pdf_path}')

# Example usage
input_pdf = 'datasets/example_pdf.pdf'
output_dir = 'datasets/divided'
split_pdf(input_pdf, output_dir)