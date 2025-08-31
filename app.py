import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# =======================
# Đọc & chuẩn hóa dữ liệu
# =======================
@st.cache_data
def load_data():
    file = "Book1(3).xlsx"
    ports = ["基隆", "台中", "高雄", "花蓮"]
    all_data = []
    
    for port in ports:
        df = pd.read_excel(file, sheet_name=port)
        df = df.rename(columns={
            "Unnamed: 0": "Date",
            "Unnamed: 1": "Hour",
            "波高\ncm": "WaveHeight_cm",
            "流速\ncm/s": "CurrentSpeed_cmps",
            "風速\nm/s": "WindSpeed_mps"
        })
        df["Port"] = port
        all_data.append(df)
    
    return pd.concat(all_data, ignore_index=True)

df = load_data()

# =======================
# Giao diện Streamlit
# =======================
st.title("🌊 Dữ liệu cảng biển Đài Loan (風速 / 波高 / 流速)")

# Chọn cảng
ports = df["Port"].unique()
selected_ports = st.multiselect("Chọn cảng", ports, default=[ports[0]])

# Chọn chỉ số
metrics = {
    "風速 (m/s)": "WindSpeed_mps",
    "波高 (cm)": "WaveHeight_cm",
    "流速 (cm/s)": "CurrentSpeed_cmps"
}
selected_metrics = st.multiselect("Chọn chỉ số", list(metrics.keys()), default=list(metrics.keys())[0:1])

# Lọc dữ liệu
filtered_df = df[df["Port"].isin(selected_ports)]

# Hiển thị bảng dữ liệu
st.subheader("Bảng dữ liệu")
st.dataframe(filtered_df[["Port", "Date", "Hour", "WindSpeed_mps", "WaveHeight_cm", "CurrentSpeed_cmps"]])

# Vẽ biểu đồ
for metric in selected_metrics:
    col_name = metrics[metric]
    plt.figure(figsize=(10, 5))
    for port in selected_ports:
        port_data = filtered_df[filtered_df["Port"] == port]
        # Dùng (Date + Hour) làm trục X
        x_axis = port_data["Date"].astype(str) + " " + port_data["Hour"].astype(str)
        plt.plot(x_axis, port_data[col_name], marker="o", label=port)
    plt.title(metric)
    plt.xlabel("Ngày - Giờ")
    plt.ylabel(metric)
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(plt)
