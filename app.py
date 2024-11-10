import streamlit as st
from PIL import Image
import os
from rembg import remove  # Assuming rembg is installed (pip install rembg)
import io
import zipfile

# Streamlit page configuration (title, icon, layout)
st.set_page_config(
    page_title="Xóa Phông Nền Hình Ảnh SaigonStem",
    page_icon="🐣",
    layout="wide",
)


def remove_background(image):
    try:
        output = remove(image)
        return output
    except Exception as e:
        st.error(f"Lỗi xóa phông nền: {e}")
        return None


def process_image(uploaded_files):
    if uploaded_files is not None:
        progress_text = "Đang xóa phông. Vui lòng chờ đợi ..."
        my_bar = st.progress(0, text=progress_text)
        pic = 0
        c= st.columns(5)
        col_counter = 0
        processed_images = []
        for uploaded_file in uploaded_files:
            try:
                # Read uploaded image
                image = Image.open(uploaded_file)

                # Remove background
                processed_image = remove_background(image)
                
                if processed_image is not None:
                    # Save processed image with unique filename
                    img_io = io.BytesIO()
                    processed_image.save(img_io, format="PNG")
                    pic+=1
                    processed_images.append((uploaded_file.name, img_io))
                    with c[col_counter]:
                        st.image(processed_image, caption=f"Hình ảnh đã xử lý: {uploaded_file.name}",width=200)
                    col_counter = (col_counter + 1) % len(c)
                    my_bar.progress((pic)/len(uploaded_files), text=progress_text)
            except Exception as e:
                st.error(f"Lỗi xử lý ảnh: {e}")
        my_bar.empty()
        if processed_images:
            # Create a ZIP file in memory
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zipf:
                for filename, img_io in processed_images:
                    zipf.writestr(f"{filename}_rmbg.png", img_io.getvalue())

            # Download the ZIP file
            st.download_button(
                label="Tải xuống tất cả ảnh đã xử lý",
                data=zip_buffer.getvalue(),
                file_name="images_rmbg.zip",
                mime="application/zip",
                use_container_width=True
            )
            st.success(f"Xóa phông nền thành công! Tải xuống ZIP file để lấy ảnh đã xử lý.")
        else:
            st.warning("Không có ảnh nào được xử lý.")

# Streamlit app layout
st.title("Xóa Phông Nền Hình Ảnh SaigonStem")
st.session_state.uploaded_files = None
st.session_state.uploaded_files = st.file_uploader("Chọn hình ảnh để xóa phông (jpg)", type="jpg", accept_multiple_files=True, on_change=st.session_state.uploaded_files,)
if st.session_state.uploaded_files !=[]:
    st.subheader(f'Số lượng hình ảnh đã chọn: {len(st.session_state.uploaded_files)}')
    cols = st.columns(5)
    col_counter = 0
    for f in st.session_state.uploaded_files:
        with cols[col_counter]:
            st.image(f, caption=f"Hình ảnh đã chọn: {f.name}", width=200)
        col_counter = (col_counter + 1) % len(cols)
    middle = st.empty()
    if middle.button('Xóa phông', use_container_width=True,):
        middle.empty()
        process_image(st.session_state.uploaded_files)
   


