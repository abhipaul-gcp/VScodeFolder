import os
import argparse
from pypdf import PdfReader, PdfWriter

def get_file_size(filepath):
    """Returns the file size in a human-readable format."""
    # Check if the file exists before attempting to get its size
    if not os.path.exists(filepath):
        return "N/A"
        
    size_bytes = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def compress_pdf(input_path: str, output_path: str, compression_level: int = 9):
    """
    Reads a PDF, applies lossless content stream compression, and saves the new PDF.

    :param input_path: Path to the original PDF file.
    :param output_path: Path to save the compressed PDF file.
    :param compression_level: Zlib compression level (0=none, 9=max). Default is 9.
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at '{input_path}'")
        return

    # Check initial file size
    initial_size = os.path.getsize(input_path)
    initial_size_str = get_file_size(input_path)
    print(f"\nOriginal file size: {initial_size_str}")
    print(f"Applying compression with level: {compression_level}...")

    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        # Add all pages from the reader to the writer
        for page in reader.pages:
            writer.add_page(page)

        # Now, iterate through the pages in the writer and compress them
        for page in writer.pages:
            page.compress_content_streams(level=compression_level)
            
        # Optional: Optimize by removing duplicate objects (can further reduce size)
        # This should be called before writing the file.
        writer.compress_identical_objects()

        # Write the compressed PDF to the output file
        with open(output_path, "wb") as f:
            writer.write(f)

        # Check final file size
        final_size = os.path.getsize(output_path)
        final_size_str = get_file_size(output_path)
        reduction_percent = 100 * (initial_size - final_size) / initial_size

        print(f"Compressed PDF saved to: **{output_path}**")
        print(f"Final file size: {final_size_str}")
        print(f"**Size Reduction: {reduction_percent:.2f}%**")
        
    except Exception as e:
        print(f"An error occurred during compression: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="A Python script to reduce PDF file size using pypdf's compression."
    )
    parser.add_argument("input_file", type=str, help="Path to the input PDF file.")
    parser.add_argument("output_file", type=str, help="Path for the output (compressed) PDF file.")
    parser.add_argument(
        "-c", "--compression", 
        type=int, 
        default=9, 
        nargs='?', # Makes the argument optional
        const=9,   # If -c is used without a value, use 9
        choices=range(10), # Only allow levels 0 to 9
        metavar='LEVEL',
        help="**Optional** compression level (0-9). 9 is maximum compression (default: 9). Set to 0 to disable compression."
    )

    args = parser.parse_args()
    
    compress_pdf(args.input_file, args.output_file, args.compression)

if __name__ == "__main__":
    main()
