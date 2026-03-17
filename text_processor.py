def read_and_split_text(raw_text: str) -> list:
    # Split by blank lines first
    paragraphs = [p.strip() for p in raw_text.split('\n\n') if p.strip()]

    slides = []
    for para in paragraphs:
        # Clean up internal newlines
        clean = ' '.join(para.split())

        # If paragraph is too long, chunk it
        words = clean.split()
        if len(words) > 30:
            chunks = chunk_text(words, chunk_size=25)
            slides.extend(chunks)
        else:
            slides.append(clean)

    # Remove empty slides
    slides = [s for s in slides if s.strip()]

    return slides


def chunk_text(words: list, chunk_size: int = 25) -> list:
    """Split a list of words into chunks of chunk_size"""
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks