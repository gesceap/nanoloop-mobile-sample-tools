import streamlit as st
from nanoloop_mobile_sample_tools import commands

st.title("Nanoloop Mobile Sample Tools")

st.text("Options")
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

uploaded_files = st.file_uploader("Files to Process", type=['.wav', '.mp3', '.ogg'], accept_multiple_files=True)

import os
for uploaded_file in uploaded_files:
    st.write(uploaded_file)
    st.write(os.path.isfile(uploaded_file.name))

st.write(uploaded_files)

run = st.button("Run")