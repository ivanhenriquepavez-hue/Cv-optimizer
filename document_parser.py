import PyPDF2
import docx

def extract_text(uploaded_file) -> str:
    """
    Extrae el texto de un archivo PDF o DOCX cargado mediante st.file_uploader.
    Incluye manejo de errores si el archivo es ilegible.
    """
    text = ""
    try:
        filename = uploaded_file.name.lower()
        
        if filename.endswith(".pdf"):
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                    
        elif filename.endswith(".docx"):
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            raise ValueError("Formato no soportado. Usa PDF o DOCX.")
            
        return text.strip()
        
    except Exception as e:
        raise Exception(f"Error al leer el archivo: {str(e)}")
