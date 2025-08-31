import pandas as pd
import streamlit as st

# =======================
# Đọc & chuẩn hóa dữ liệu
# =======================
@st.cache_data
def load_data():
    file = "Book1(3).xlsx"
    ports = ["基隆", "台中", "高雄", "花蓮"]   # tên sheet chính là tên cảng
    all_data = []
    
    for port in ports:
        df = pd.read_excel(file, sheet_name=port)
        df = df.rename(columns={
            "Unnamed: 0": "Date",
            "Unnamed: 1": "Hour",
            "風速\nm/s": "WindSpeed_mps",
            "波高\ncm": "WaveHeight_cm",
            "流速\ncm/s": "CurrentSpeed_cmps"
        })
        df["Port"] = port   # thêm cột cảng
        # tạo datetime (ngày + giờ)
        df["Datetime"] = pd.to_datetime(df["Date"]) + pd.to_timedelta(df["Hour"].astype(int), unit="h")
        all_data.append(df)
    
    return pd.concat(all_data, ignore_index=True)

df = load_data()

# =======================
# Giao diện Streamlit
# =======================
st.title("Dữ liệu cảng biển Đài Loan (風速 / 波高 / 流速)")

# Chọn cảng
ports = df["Port"].unique()
selected_ports = st.multiselect("Chọn cảng", ports, default=list(ports))

# Chọn chỉ số
metrics = {
    "風速 (m/s)": "WindSpeed_mps",
    "波高 (cm)": "WaveHeight_cm",
    "流速 (cm/s)": "CurrentSpeed_cmps"
}
selected_metrics = st.multiselect("Chọn chỉ số", list(metrics.keys()), default=[list(metrics.keys())[0]])

# Lọc dữ liệu
filtered_df = df[df["Port"].isin(selected_ports)]

# Hiển thị bảng dữ liệu
st.subheader("Bảng dữ liệu")
st.dataframe(filtered_df[["Port", "Date", "Hour", "WindSpeed_mps", "WaveHeight_cm", "CurrentSpeed_cmps"]])

# Vẽ biểu đồ
for metric in selected_metrics:
    col_name = metrics[metric]
    st.subheader(f"Biểu đồ: {metric}")
    chart_data = filtered_df.pivot(index="Datetime", columns="Port", values=col_name)
    st.line_chart(chart_data)
