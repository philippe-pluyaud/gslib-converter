import streamlit as st
from pathlib import Path
from ConvertGsLibFileForJoints import modify_gslib

st.set_page_config(page_title="GsLib Converter for Joints", layout="centered")

st.title("Filter to Convert GsLib File for Joints")
st.markdown("---")

# File upload section
st.subheader("📁 Files")
col1, col2 = st.columns(2)

with col1:
    input_file = st.file_uploader("Select input GsLib file", type=["gslib", "txt"])

with col2:
    output_filename = st.text_input("Output filename", value="output.gslib", placeholder="output.gslib")

st.markdown("---")

# Parameters section
st.subheader("⚙️ Parameters")

col1, col2, col3 = st.columns(3)
with col1:
    i_offset = st.number_input("I offset", value=0, min_value=0, step=1)
with col2:
    j_offset = st.number_input("J offset", value=0, min_value=0, step=1)
with col3:
    k_offset = st.number_input("K offset", value=0, min_value=0, step=1)

col1, col2 = st.columns(2)
with col1:
    dip_angle = st.number_input("Dip angle (°)", value=0.0, min_value=0.0, max_value=90.0, step=0.1)
with col2:
    strike_angle = st.number_input("Strike angle (°)", value=0.0, min_value=0.0, max_value=360.0, step=0.1)

col1, col2 = st.columns(2)
with col1:
    KN = st.number_input("KN (Normal stiffness)", value=8000000.0, step=100000.0, format="%.0f")
with col2:
    KS = st.number_input("KS (Shear stiffness)", value=4000000.0, step=100000.0, format="%.0f")

st.markdown("---")

# Submit button
if st.button("🚀 Launch Conversion", use_container_width=True, type="primary"):
    if not input_file:
        st.error("❌ Please select an input file")
    elif not output_filename:
        st.error("❌ Please enter an output filename")
    else:
        try:
            # Save uploaded file temporarily
            temp_input_path = f"temp_{input_file.name}"
            with open(temp_input_path, "wb") as f:
                f.write(input_file.getbuffer())
            
            with st.spinner("Converting file..."):
                # Run the conversion
                modify_gslib(
                    temp_input_path, 
                    output_filename,
                    int(i_offset), 
                    int(j_offset), 
                    int(k_offset),
                    float(dip_angle), 
                    float(strike_angle), 
                    float(KN), 
                    float(KS)
                )
            
            st.success("✅ File conversion completed successfully!")
            
            # Allow download of the output file
            if Path(output_filename).exists():
                with open(output_filename, "rb") as f:
                    st.download_button(
                        label="📥 Download converted file",
                        data=f.read(),
                        file_name=output_filename,
                        mime="application/octet-stream",
                        use_container_width=True
                    )
            
            # Display parameters summary
            st.info(
                f"""
                **Conversion Summary:**
                - Input: {input_file.name}
                - Output: {output_filename}
                - Offsets: I={int(i_offset)}, J={int(j_offset)}, K={int(k_offset)}
                - Angles: Dip={dip_angle}°, Strike={strike_angle}°
                - Stiffness: KN={KN:.0f}, KS={KS:.0f}
                """
            )
            
            # Clean up temp file
            Path(temp_input_path).unlink()
            
        except FileNotFoundError:
            st.error(f"❌ File not found: {output_filename}")
        except Exception as e:
            st.error(f"❌ Error during conversion: {str(e)}")
            st.write("Please check your inputs and try again.")