import streamlit as st
import requests
import uvicorn
import argparse

# Function to upload file and call FastAPI endpoint
def predict_by_file(file):
    url = 'http://localhost:8000/ocr/predict-by-file'  # Replace with your FastAPI endpoint URL
    files = {'file': ('image.jpg', file, 'image/jpeg')}
    response = requests.post(url, files=files)
    return response.json()

# Streamlit app
def main():
    st.title('Upload Image for OCR Prediction')
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
        if st.button('Predict'):
            try:
                # Convert uploaded file to bytes
                image_bytes = uploaded_file.read()
                # Call FastAPI endpoint
                response = predict_by_file(image_bytes)
                # Display result
                st.write('Prediction Result:')
                result = [] if response['data'][0] is None else [i[1][0] for i in response['data'][0]]
                st.write(str(result))
            except Exception as e:
                st.error(f'Error: {e}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Streamlit app')
    parser.add_argument('--api_port', type=str, default='', help='Parameter for the model')
    args = parser.parse_args()
    main()
    uvicorn.run("main:app", host="127.0.0.1", port=args.api_port)