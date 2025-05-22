
import os
import ezdxf
import streamlit as st
from tempfile import NamedTemporaryFile

# --- Web App Title ---
st.set_page_config(page_title="DWG to DXF Converter", layout="centered")
st.title("DWG to DXF Web Converter with Line & Block Analysis")

# --- Upload Section ---
uploaded_file = st.file_uploader("Upload a DXF file (converted from DWG)", type=["dxf"])

# --- Helper Functions ---
def read_dxf(file_path):
    doc = ezdxf.readfile(file_path)
    msp = doc.modelspace()
    blocks = []
    lines_with_breaks = []
    lines_without_breaks = []

    for entity in msp:
        if entity.dxftype() == 'INSERT':
            blocks.append(entity)
        elif entity.dxftype() == 'LINE':
            if is_broken(entity, msp):
                lines_with_breaks.append(entity)
            else:
                lines_without_breaks.append(entity)

    return blocks, lines_with_breaks, lines_without_breaks

def is_broken(line_entity, msp, threshold=0.1):
    # Placeholder for break detection logic (currently dummy logic)
    return False

def write_to_dxf(blocks, lines_with_breaks, lines_without_breaks):
    doc = ezdxf.new()
    msp = doc.modelspace()

    for line in lines_with_breaks + lines_without_breaks:
        msp.add_line(line.dxf.start, line.dxf.end)
    for block in blocks:
        msp.add_blockref(block.dxf.name, block.dxf.insert)

    temp_out = NamedTemporaryFile(delete=False, suffix=".dxf")
    doc.saveas(temp_out.name)
    return temp_out.name

# --- Main Logic ---
if uploaded_file:
    with NamedTemporaryFile(delete=False, suffix=".dxf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.success("File uploaded. Processing...")
    blocks, lwb, lwob = read_dxf(tmp_path)
    st.write(f"✅ Blocks found: {len(blocks)}")
    st.write(f"🔹 Lines without breaks: {len(lwob)}")
    st.write(f"🔸 Lines with breaks (assumed): {len(lwb)}")

    output_path = write_to_dxf(blocks, lwb, lwob)
    with open(output_path, "rb") as f:
        st.download_button("Download Processed DXF", f, file_name="converted_output.dxf")
