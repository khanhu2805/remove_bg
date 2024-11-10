import streamlit as st
from PIL import Image
import os
from rembg import remove  # Assuming rembg is installed (pip install rembg)

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
        col_counter = 0
        for uploaded_file in uploaded_files:
            try:
                # Read uploaded image
                image = Image.open(uploaded_file)

                # Remove background
                processed_image = remove_background(image)
                
                if processed_image is not None:
                    # Save processed image with unique filename
                    save_path = os.path.join(   
                        output_folder_path, f"{uploaded_file.name}_rmbg.png"
                    )
                    processed_image.save(save_path)
                    pic+=1
                    st.session_state.processed_image.append(processed_image)
                    with cols[col_counter]:
                        st.image(processed_image, width=200)
                    col_counter = (col_counter + 1) % len(cols)
                    my_bar.progress((pic)/len(uploaded_files), text=progress_text)
                    # Download link
                    # download_link = st.download_button(
                    #     label="Tải xuống",
                    #     data=processed_image.tobytes(),
                    #     file_name=save_path,
                    # )

                    # Success message with download link
                    # st.success(
                    #     f"Xóa phông nền thành công! "
                    #     f"[Tải xuống]({download_link})"
                    # )
                else:
                    st.warning("Xóa phông nền thất bại.")

            except Exception as e:
                st.error(f"Lỗi xử lý ảnh: {e}")
        my_bar.empty()
        st.success(
        f"Xóa phông nền thành công! "
        # f"[Tải xuống]({download_link})"
        )


# Output folder path (modify as needed)
output_folder_path = "/pic_processed"

# Create output folder if it doesn't exist
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# Streamlit app layout
st.title("Xóa Phông Nền Hình Ảnh SaigonStem")
st.session_state.uploaded_files = None
st.session_state.processed_image = []
st.session_state.uploaded_files = st.file_uploader("Chọn hình ảnh để xóa phông (jpg)", type="jpg", accept_multiple_files=True, on_change=st.session_state.uploaded_files,)
if st.session_state.uploaded_files !=[]:
    st.subheader(f'Số lượng hình ảnh đã chọn: {len(st.session_state.uploaded_files)}')
    cols = st.columns(5)
    col_counter = 0
    for f in st.session_state.uploaded_files:
        with cols[col_counter]:
            st.image(f, caption=f"Hình ảnh đã chọn: {f.name}", width=200)
        col_counter = (col_counter + 1) % len(cols)
    left, middle, right = st.columns(3)
    if middle.button('Xóa phông', use_container_width=True):
        process_image(st.session_state.uploaded_files)
   


