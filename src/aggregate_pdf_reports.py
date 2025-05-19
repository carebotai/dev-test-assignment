from datetime import datetime, timedelta


def get_pdf_file_names(from_: datetime, to: datetime) -> list[str]:
    """
    This function should retrieve a list of PDF report file names (from our DB)
    that were created between `from_` and `to`.
    Metadata for each PDF report are stored in a `dicom_report` table, where
    you will find also the filename column.
    """


def download_pdf_from_azure(pdf_file_name: str) -> bytes:
    """
    This function should download a PDF report from the Azure Blob Storage stored
    under the `pdf_file_name`. Use the `pdf-reports` container.
    Return the downloaded PDF report as bytes.
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
    pdf_file_names = get_pdf_file_names(
        from_=datetime.now() - timedelta(days=14),
        to=datetime.now(),
    )

    pdf_paths = []
    for pdf_file_name in pdf_file_names:
        pdf = download_pdf_from_azure(pdf_file_name)
        pdf_path = store_pdf_on_disk(pdf)
        pdf_paths.append(pdf_path)

    join_pdfs(pdf_paths)
