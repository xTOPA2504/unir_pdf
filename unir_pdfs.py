import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog
import PyPDF2

class PDFMergerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Configuración de la interfaz gráfica
        self.setWindowTitle('Unir PDFs')
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        # Botón para seleccionar archivos PDF
        self.button_select_files = QPushButton('Seleccionar archivos PDF', self)
        self.button_select_files.clicked.connect(self.select_files)
        self.layout.addWidget(self.button_select_files)

        # Botón para unir los archivos PDF seleccionados
        self.button_merge = QPushButton('Unir PDFs', self)
        self.button_merge.clicked.connect(self.merge_pdfs)
        self.layout.addWidget(self.button_merge)

        self.setLayout(self.layout)

    def select_files(self):
        # Abre el cuadro de diálogo para seleccionar múltiples archivos PDF
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Archivos PDF (*.pdf)")
        file_dialog.setViewMode(QFileDialog.Detail)
        if file_dialog.exec_():
            self.selected_files = file_dialog.selectedFiles()

    def merge_pdfs(self):
        # Verifica si se han seleccionado al menos dos archivos PDF
        if hasattr(self, 'selected_files') and len(self.selected_files) > 1:
            # Crea un objeto PDFMerger de PyPDF2
            pdf_merger = PyPDF2.PdfMerger()

            # Agrega cada archivo PDF seleccionado al objeto PDFMerger
            for pdf_file in self.selected_files:
                pdf_merger.append(pdf_file)

            # Abre un cuadro de diálogo para seleccionar la ubicación y el nombre del archivo de salida
            output_filename, _ = QFileDialog.getSaveFileName(self, 'Guardar archivo', filter='PDF (*.pdf)')

            if output_filename:
                # Escribe el archivo PDF fusionado en la ubicación especificada
                with open(output_filename, 'wb') as output_file:
                    pdf_merger.write(output_file)

                print(f'PDFs unidos con éxito en: {output_filename}')
            else:
                print('Operación cancelada.')
        else:
            print('Seleccione al menos dos archivos PDF.')

if __name__ == '__main__':
    # Configura y muestra la aplicación PyQt
    app = QApplication(sys.argv)
    pdf_merger_app = PDFMergerApp()
    pdf_merger_app.show()
    sys.exit(app.exec_())
