from dataclasses import dataclass
from datetime import datetime


@dataclass
class PDFReportMetadata:
    """
    Metadata for a single DICOM PDF (Encapsulated PDF) report.
    """
    container_name: str
    file_name: str


def get_dicom_pdf_metadata(from_: datetime, to: datetime) -> list[PDFReportMetadata]:
    """
    This function should retrieve a list of DICOM PDF report metadata (from our DB)
    that were created between `from_` and `to`.

    Metadata for each DICOM PDF report are stored in a `dicom_report` table.
    """


def download_dicom_pdf_from_azure(pdf_report_metadata: PDFReportMetadata) -> bytes:
    """
    This function should download a DICOM PDF report from the Azure Blob Storage.

    Return the downloaded DICOM PDF report as bytes.
    """


def convert_dicom_pdf_to_normal_pdf(dicom_pdf: bytes) -> bytes:
    """
    This function should convert a DICOM PDF report to a normal PDF.
    """


def store_pdf_on_disk(pdf: bytes) -> str:
    """
    Store the PDF report (received as bytes) on local file system.
    The target destination should be configurable via an environment variable
    `PDF_TARGET_DIR`.
    """


def join_pdfs(pdf_paths: list[str]) -> None:
    """
    This function should join multiple PDF files into a single PDF file. The target
    destination of the aggregated PDF file should be configurable via an environment
    variable `JOINED_PDF_TARGET_DIR`.
    """


if __name__ == '__main__':
    pdf_reports_metadata = get_dicom_pdf_metadata(
        from_=...,
        to=...,
    )

    pdf_paths = []
    for pdf_report_metadata in pdf_reports_metadata:
        dicom_pdf = download_dicom_pdf_from_azure(pdf_report_metadata)
        pdf = convert_dicom_pdf_to_normal_pdf(dicom_pdf)
        pdf_path = store_pdf_on_disk(pdf)
        pdf_paths.append(pdf_path)

    join_pdfs(pdf_paths)
