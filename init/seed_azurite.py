import datetime

import psycopg2
import pydicom
from azure.storage.blob import BlobServiceClient
from fpdf import FPDF
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import generate_uid, ExplicitVRLittleEndian, EncapsulatedPDFStorage


DATABASE_CONNECTION_STRING = "postgresql://db_admin:testpassword123@postgres:5432/dicom_db"
# This is the standard, hardcoded connection string for the Azurite emulator
AZURITE_CONNECTION_STRING = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://azurite:10000/devstoreaccount1;"

def create_minimal_pdf():
    # Initialize a PDF object
    pdf = FPDF()

    # Add a single page
    pdf.add_page()

    # Set font (Arial or Helvetica are standard and don't require external font files)
    pdf.set_font("helvetica", size=12)

    # Add a single cell of text
    pdf.cell(text="This is a dummy PDF for ML testing.")

    # Return bytes
    return bytes(pdf.output())


def create_encapsulated_pdf_dicom(pdf_bytes):
    # 2. Set up the File Meta Information
    file_meta = FileMetaDataset()
    # SOP Class UID for Encapsulated PDF Storage
    file_meta.MediaStorageSOPClassUID = EncapsulatedPDFStorage
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.ImplementationClassUID = generate_uid()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    # 3. Create the main Dataset
    ds = Dataset()
    ds.file_meta = file_meta

    # Set endianness and VR types
    ds.is_little_endian = True
    ds.is_implicit_VR = False

    # 4. Populate required DICOM tags (Minimal set)

    # Patient Module
    ds.PatientName = "Test^Patient"
    ds.PatientID = "PAT-123"
    ds.PatientSex = "O"
    ds.PatientBirthDate = "19900101"

    # Study Module
    dt = datetime.datetime.now()
    ds.StudyDate = dt.strftime('%Y%m%d')
    ds.StudyTime = dt.strftime('%H%M%S.%f')
    ds.StudyInstanceUID = generate_uid()
    ds.StudyID = "STUDY-1"
    ds.AccessionNumber = ""

    # Series Module
    ds.SeriesInstanceUID = generate_uid()
    ds.SeriesNumber = "1"
    ds.Modality = "DOC"  # DOC stands for Document

    # Equipment Module
    ds.ConversionType = "WSD"  # Workstation

    # Encapsulated Document Module
    ds.InstanceNumber = "1"
    ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
    ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
    ds.DocumentTitle = "Minimal Encapsulated PDF Report"
    ds.MIMETypeOfEncapsulatedDocument = "application/pdf"
    ds.BurnedInAnnotation = "YES"  # Often required by strict viewers

    # 5. Inject the PDF bytes
    # VR 'OB' means Other Byte String
    ds.add_new((0x0042, 0x0011), 'OB', pdf_bytes)

    # 6. Save the file
    bytes_io = pydicom.filewriter.DicomBytesIO()
    pydicom.dcmwrite(bytes_io, ds, write_like_original=False)
    print(f"Successfully created Encapsulated PDF DICOM")
    return bytes_io.getvalue()


def fetch_container_and_file_names():
    # Connection to the local DB.
    db = psycopg2.connect(DATABASE_CONNECTION_STRING)
    db_cursor = db.cursor()
    db_cursor.execute("SELECT dicom_report.container_name, dicom_report.file_name FROM dicom_report;")
    rows = db_cursor.fetchall()
    db_cursor.close()

    containers = {}
    for row in rows:
        containers.setdefault(row[0], []).append(row[1])

    return containers


def get_container_client(blob_service_client, container_name):
    # Create the container if it doesn't exist.
    try:
        container_client = blob_service_client.create_container(container_name)
        print(f"Container '{container_name}' created.")
    except Exception as e:
        print(f"Container might already exist: {e}")
        container_client = blob_service_client.get_container_client(container_name)

    return container_client


def seed_storage():
    print("Connecting to Azurite...")
    blob_service_client = BlobServiceClient.from_connection_string(AZURITE_CONNECTION_STRING)

    pdf_bytes = create_minimal_pdf()
    dicom_file_data = create_encapsulated_pdf_dicom(pdf_bytes)
    container_and_file_names = fetch_container_and_file_names()

    # Generate and upload fake DICOM data
    for container_name, file_names in container_and_file_names.items():
        container_client = get_container_client(blob_service_client, container_name)

        for file_name in file_names:
            blob_client = container_client.get_blob_client(file_name)

            blob_client.upload_blob(dicom_file_data, overwrite=True)
            print(f"Uploaded {file_name} to {container_name}/{file_name}")


if __name__ == "__main__":
    seed_storage()
    print("Azurite seeding complete!")
