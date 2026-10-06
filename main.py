import streamlit as st
import chromadb
from pypdf import PdfReader
from ollama import chat


# =========================
# PAGE SETUP
# =========================

st.set_page_config(
    page_title="AI Personal Knowledge Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Personal Knowledge Assistant")
st.write("Upload your PDFs and ask questions about your documents.")


# =========================
# CHROMA DATABASE
# =========================

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="knowledge"
)


# =========================
# PDF TEXT EXTRACTION
# =========================

def read_pdf(pdf):

    reader = PdfReader(pdf)

    pages = []

    for page_number, page in enumerate(reader.pages, 1):

        text = page.extract_text()

        if text:
            pages.append({
                "page": page_number,
                "text": text
            })

    return pages


# =========================
# CREATE CHUNKS
# =========================

def make_chunks(pages):

    chunks = []

    for page in pages:

        words = page["text"].split()

        chunk_size = 300

        for i in range(0, len(words), chunk_size):

            chunk = " ".join(
                words[i:i + chunk_size]
            )

            if chunk.strip():

                chunks.append({
                    "text": chunk,
                    "page": page["page"]
                })

    return chunks


# =========================
# ADD PDF TO KNOWLEDGE BASE
# =========================

def add_pdf(pdf):

    pages = read_pdf(pdf)

    chunks = make_chunks(pages)

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        ids.append(
            f"{pdf.name}_{i}"
        )

        documents.append(
            chunk["text"]
        )

        metadatas.append({
            "file": pdf.name,
            "page": chunk["page"]
        })

    if documents:

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    return len(documents)


# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.header("📂 Documents")

    pdfs = st.file_uploader(
        "Upload PDF files",
        type="pdf",
        accept_multiple_files=True
    )

    if pdfs:

        if st.button(
            "➕ Add to Knowledge Base",
            use_container_width=True
        ):

            total = 0

            for pdf in pdfs:

                try:

                    count = add_pdf(pdf)

                    total += count

                except Exception as e:

                    st.error(
                        f"{pdf.name}: {e}"
                    )

            st.success(
                f"Added {total} document sections."
            )

    st.divider()

    st.metric(
        "Knowledge Sections",
        collection.count()
    )

    if st.button(
        "🗑️ Clear Knowledge Base",
        use_container_width=True
    ):

        try:

            client.delete_collection("knowledge")

            collection = client.get_or_create_collection(
                name="knowledge"
            )

            st.success("Knowledge base cleared.")

        except Exception as e:

            st.error(str(e))


# =========================
# QUESTION AREA
# =========================

st.subheader("💬 Ask Your Documents")

with st.form(
    "question_form",
    clear_on_submit=True
):

    question = st.text_input(
        "Your question",
        placeholder="Example: What is the main topic of this document?"
    )

    ask = st.form_submit_button(
        "🔍 Ask AI",
        use_container_width=True
    )


# =========================
# ASK AI
# =========================

if ask:

    if not question.strip():

        st.warning("Please enter a question.")

    elif collection.count() == 0:

        st.warning(
            "Please upload a PDF and add it to the knowledge base first."
        )

    else:

        with st.spinner("Thinking..."):

            # Search relevant information
            results = collection.query(
                query_texts=[question],
                n_results=3
            )

            documents = results["documents"][0]
            metadatas = results["metadatas"][0]

            # Create context
            context = ""

            for document, metadata in zip(
                documents,
                metadatas
            ):

                context += f"""
File: {metadata['file']}
Page: {metadata['page']}

{document}

"""


            # Ask local AI
            response = chat(

                model="llama3.2",

                messages=[

                    {
                        "role": "system",

                        "content": """
You are an AI Personal Knowledge Assistant.

Answer the user's question using ONLY the
information provided from the uploaded documents.

Rules:

- Answer like ChatGPT.
- Keep the answer short and clear.
- Give 1 to 3 sentences.
- Do not copy large paragraphs.
- Do not invent information.
- Do not mention embeddings, chunks, retrieval,
  or internal processing.
- If the answer is not available, say:

"I couldn't find the answer in the uploaded documents."
"""
                    },

                    {
                        "role": "user",

                        "content": f"""
DOCUMENT INFORMATION:

{context}

QUESTION:

{question}

Give a short and direct answer.
"""
                    }

                ]
            )

            answer = response[
                "message"
            ][
                "content"
            ].strip()


        # =========================
        # SHOW ANSWER
        # =========================

        st.subheader("🤖 Answer")

        st.success(answer)


        # =========================
        # SHOW SOURCES
        # =========================

        with st.expander(
            "📑 View Sources"
        ):

            for document, metadata in zip(
                documents,
                metadatas
            ):

                st.write(
                    f"📄 **{metadata['file']}**"
                )

                st.write(
                    f"📑 Page **{metadata['page']}**"
                )

                st.caption(
                    document[:300] + "..."
                )

                st.divider()


# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "🔒 Local AI • Your documents stay on your computer • "
    "Powered by Ollama + Llama 3.2"
)