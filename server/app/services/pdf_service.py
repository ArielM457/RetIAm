from pathlib import Path


def generate_simple_pdf(output_path: Path, title: str, lines: list[str]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    safe_lines = [title, ""] + [line.replace("(", "").replace(")", "") for line in lines]
    content_stream = ["BT", "/F1 18 Tf", "50 780 Td"]
    content_stream.append(f"({safe_lines[0]}) Tj")

    y_offset = 28
    for line in safe_lines[1:]:
        escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        content_stream.append(f"0 -{y_offset} Td")
        content_stream.append("/F1 11 Tf")
        content_stream.append(f"({escaped}) Tj")
        y_offset = 18
    content_stream.append("ET")
    stream = "\n".join(content_stream).encode("latin-1", errors="replace")

    objects: list[bytes] = []
    objects.append(b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n")
    objects.append(b"2 0 obj << /Type /Pages /Count 1 /Kids [3 0 R] >> endobj\n")
    objects.append(
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n"
    )
    objects.append(b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n")
    objects.append(
        f"5 0 obj << /Length {len(stream)} >> stream\n".encode("latin-1")
        + stream
        + b"\nendstream endobj\n"
    )

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for item in objects:
        offsets.append(len(pdf))
        pdf.extend(item)
    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets)}\n".encode("latin-1"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))
    pdf.extend(
        f"trailer << /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF".encode("latin-1")
    )
    output_path.write_bytes(pdf)
