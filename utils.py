import subprocess
import platform

def convert_to_pdfa(input_path, output_path):
    gs_cmd = "gswin64c.exe" if platform.system() == "Windows" else "gs"
    args = [
        gs_cmd,
        "-dPDFA=2",
        "-dBATCH",
        "-dNOPAUSE",
        "-dNOOUTERSAVE",
        "-sColorConversionStrategy=RGB",
        "-sProcessColorModel=DeviceRGB",
        "-dPDFACompatibilityPolicy=1",
        "-sDEVICE=pdfwrite",
        f"-sOutputFile={output_path}",
        input_path
    ]
    result = subprocess.run(args, capture_output=True, text=True)
    return result