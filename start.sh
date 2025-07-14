#!/bin/bash
python app.py &  # Backend en segundo plano
streamlit run st.py --server.port=8501
