import tempfile
import os
import zipfile
import streamlit as st
from nanoloop_mobile_sample_tools import commands

st.title("Nanoloop Mobile Sample Tools")

st.header("Audio Options")

concatenate = st.checkbox("Concatenate")
reverse = st.checkbox("Reverse")

mono = st.checkbox("Mono")
mono_channel = None
if mono:
    mono_channel = st.selectbox("Mono Channel", ['left', 'right'])

compress = st.checkbox("Compress")
compress_type = None
if compress:
    compress_type = st.selectbox("Compress Type", ['soft', 'hard'])

normalize = st.checkbox("Normalize")
sample_rate = st.select_slider("Sample Rate", [44100.0, 22050.0, 11025.0, 8000.0])
bit_rate = st.selectbox("Bit Rate", [16, 8])
speed_multiplier = st.select_slider("Speed Multiplier", list(range(1, 11)))

st.header("Process Audio Files")

st.config.set_option("server.maxUploadSize", 10)
bytes_to_download = None
with st.form("uploader-form", clear_on_submit=True):
    uploaded_files = st.file_uploader(
        "Files to Process",
        type=['.wav'],
        accept_multiple_files=True
    )

    # Read the binary output of the zip archive
    # Make download button to download in memory zip archive        
    run = st.form_submit_button("Run")
    if run and uploaded_files:
        st.write("Processing {} uploaded files".format(len(uploaded_files)))
        # Save all the uploaded binary data to uploaded temp dir
        with tempfile.TemporaryDirectory() as uploaded_tempdir:
            audio_inputs = []
            file_names = []
            for uploaded_file in uploaded_files:
                file_names.append(uploaded_file.name)
                audio_input = os.path.join(uploaded_tempdir, uploaded_file.name)

                with open(audio_input, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                audio_inputs.append(audio_input)

            # Process all the files with the package and kwargs
            audio_arrays = commands.process(
                audio_inputs,
                sample_rate,
                speed_multiplier,
                concatenate,
                mono_channel,
                compress_type,
                normalize,
                reverse
            )

            st.write("Processed {} audio inputs.".format(len(audio_arrays)))

            # Save all the processed files to the processed temp dir
            with tempfile.TemporaryDirectory() as processed_tempdir:
                
                audio_outputs = []
                for file_name, audio_array in zip(file_names, audio_arrays):
                    audio_output = os.path.join(
                        processed_tempdir, "processed_{}".format(file_name)
                    )

                    if concatenate and len(audio_arrays) == 1:
                        audio_output =  os.path.join(processed_tempdir, "processed.wav")

                    commands.save(
                        audio_array,
                        sample_rate,
                        bit_rate,
                        audio_output
                    )

                    audio_outputs.append(audio_output)

                st.write("Saved {} audio outputs.".format(len(audio_outputs)))
            
                # Add all processed files in the processed temp dir to a ZIP archive
                zip_file_name = "processed.zip"
                zip_file_path = os.path.join(processed_tempdir, zip_file_name)
                with zipfile.ZipFile(zip_file_path, "w") as archive:
                    for audio_output in audio_outputs:
                        _, arcname = os.path.split(audio_output)
                        archive.write(audio_output, arcname)
                
                with open(zip_file_path, 'rb') as zf:
                    bytes_to_download = zf.read()

                st.write(
                    "Wrote {} bytes in compresed archive for download; {}".format(
                        len(bytes_to_download),
                        zip_file_name
                    )
                )

# Give dialog for archive download
download = False
if run and bytes_to_download:
    download = st.download_button("Download", data=bytes_to_download, file_name=zip_file_name, mime='application/zip')

# Reset the variables
if download:
    run = False
    bytes_to_download = None
    download = False
    uploaded_files = []
