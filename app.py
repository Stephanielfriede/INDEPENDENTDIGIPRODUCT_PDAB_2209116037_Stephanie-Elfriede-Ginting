import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

# Load the dataset
data = pd.read_csv("https://raw.githubusercontent.com/Stephanielfriede/INDEPENDENTDIGIPRODUCT_PDAB_2209116037_Stephanie-Elfriede-Ginting/main/Data%20Cleaned%20(1).csv")

# Calculate the proportions for each team
proportions_team = data['team'].value_counts(normalize=True)

# Load the model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Range of each column
value_ranges = {
    'quarter': (0, 4),
    'department': (0, 1),
    'day': (0, 31),
    'team': (1, 12),
    'targeted_productivity': (0.6, 0.8),
    'smv': (2.9, 52.615),
    'wip': (10, 23122),
    'over_time': (0, 15090),
    'incentive': (0, 119),
    'no_of_workers': (2, 89),
    'productivity_difference': (-0.3723386377500001, 0.396633333)
}

# Define a function to make predictions
def predict_productivity(quarter, department, day, team, targeted_productivity, smv, wip, over_time, incentive, no_of_workers, productivity_difference):
    input_data = [[quarter, department, day, team, targeted_productivity, smv, wip, over_time, incentive, no_of_workers, productivity_difference]]
    prediction = model.predict(input_data)
    return prediction[0]

with st.container():
    st.markdown('# Welcome to the Garment Worker Productivity Dashboard!')

with st.sidebar:
    st.title('👕 Garment Worker Productivity Dashboard')


# Sidebar navigation
nav_selection = st.sidebar.selectbox("*Select Dashboard Section*", ["Home", "Visualizations", "Predict"])


if nav_selection == "Home":
    st.image("https://oscas.co.id/artikel/files/images/20221111-garment.jpg", caption="", use_column_width=True)
    st.write("Proyek ini bertujuan untuk meningkatkan efisiensi operasional dan produktivitas di industri garmen dengan memprediksi tingkat produktivitas pekerja. Langkah-langkahnya meliputi pemahaman situasi bisnis, analisis data historis untuk mengidentifikasi pola, pengembangan model regresi berdasarkan faktor-faktor yang mempengaruhi produktivitas, evaluasi, validasi, dan implementasi model untuk pemantauan kinerja.")
    st.write("Proyek ini juga mendukung Tujuan Pembangunan Berkelanjutan (SDG) nomor 8, yaitu \"Menciptakan Pekerjaan yang Layak dan Pertumbuhan Ekonomi yang Berkelanjutan.\" Dengan meningkatkan produktivitas pekerja, perusahaan garmen dapat meningkatkan efisiensi operasional dan menciptakan lingkungan kerja yang lebih baik bagi karyawan. Hal ini berkontribusi pada penciptaan pekerjaan yang layak dan pertumbuhan ekonomi yang berkelanjutan dengan menciptakan lebih banyak peluang kerja dan meningkatkan pertumbuhan ekonomi di tingkat lokal dan nasional.")
    st.write("Berikut adalah dataset yang digunakan: [Productivity Prediction of Garment Employees](https://www.kaggle.com/datasets/ishadss/productivity-prediction-of-garment-employees)")

    if st.button("Keterangan Kolom"):
        if "show_column_description" not in st.session_state:
            st.session_state.show_column_description = False

        st.session_state.show_column_description = not st.session_state.show_column_description

        if st.session_state.show_column_description:
            st.write("1. Date: Tanggal ketika data diambil dalam format Bulan-Hari-Tahun")
            st.write("2. Day: Hari dalam seminggu (Senin, Selasa, dll.)")
            st.write("3. Quarter: Bagian dari bulan. Satu bulan dibagi menjadi empat bagian.")
            st.write("4. DepartemenT: Bagian dari pabrik yang terkait dengan data tersebut")
            st.write("5. Team No: Nomor identifikasi untuk setiap tim kerja")
            st.write("6. No Of Workers: Total jumlah pekerja dalam tim")
            st.write("7. No Of Style Change: Berapa kali gaya produk diubah")
            st.write("8. Targeted Productivity: Target produktivitas yang diharapkan untuk dicapai oleh setiap tim setiap hari.")
            st.write("9. SMV: Nilai menit standar, yaitu perkiraan waktu yang dibutuhkan untuk menyelesaikan suatu tugas")
            st.write("10. WIP: Pekerjaan yang masih dalam proses. Ini mencakup jumlah barang yang belum selesai.")
            st.write("11. Over Time: Waktu tambahan yang digunakan oleh tim melebihi jam kerja normal")
            st.write("12. Incentive: Bonus finansial yang diberikan untuk mendorong kinerja")
            st.write("13. Idle Time: Waktu ketika produksi terhenti sementara")
            st.write("14. Idle Men: Jumlah pekerja yang tidak melakukan pekerjaan karena gangguan dalam produksi")
            st.write("15. Actual Productivity: Persentase seberapa efisien pekerja dalam melakukan tugas mereka, diukur dari 0 hingga 1.")
        else:
            st.subheader("")

elif nav_selection == "Visualizations":
    # Pilihan visualisasi
    st.header("Pilih Visualisasi")
    visualization_option = st.selectbox("Visualisasi", ["Distribution", "Comparison", "Composition", "Relationship"])

    # Distribusi
    if visualization_option == "Distribution":
        st.header("Distribution")

        # Distribusi pekerjaan di masing-masing kuartal
        fig1 = px.bar(data['quarter'].value_counts(), x=data['quarter'].unique(), y=data['quarter'].value_counts().values, labels={'x': 'Kuartal', 'y': 'Jumlah'}, title='Distribusi Pekerjaan di Setiap Kuartal')
        st.plotly_chart(fig1, use_container_width=True)

        # Penjelasan distribusi pekerjaan di setiap kuartal
        st.write("Distribusi pekerjaan di setiap kuartal menunjukkan jumlah pekerjaan yang dilakukan dalam rentang waktu yang berbeda-beda selama periode tertentu, yang dibagi menjadi kuartal.")
        st.write("- *Kuartal 0*: Terdapat 342 pekerjaan yang dilakukan selama kuartal ini.")
        st.write("- *Kuartal 1*: Pada kuartal ini, dilakukan sebanyak 295 pekerjaan.")
        st.write("- *Kuartal 2*: Terdapat 226 pekerjaan yang dilakukan selama kuartal ini.")
        st.write("- *Kuartal 3*: Pada kuartal ini, terdapat 187 pekerjaan yang dilakukan.")
        st.write("- *Kuartal 4*: Jumlah pekerjaan paling sedikit terjadi pada kuartal ini, hanya terdapat 41 pekerjaan.")

        # Rata-rata Produktivitas Aktual Setiap Kuartal
        avg_productivity_per_quarter = data.groupby('quarter')['actual_productivity'].mean()
        fig4 = px.bar(x=avg_productivity_per_quarter.index, y=avg_productivity_per_quarter.values, labels={'x':'Kuartal', 'y':'Rata-rata Produktivitas Aktual'}, title='Rata-rata Produktivitas Aktual Setiap Kuartal')
        st.plotly_chart(fig4, use_container_width=True)

    # Comparison
    elif visualization_option == "Comparison":
        st.header("Comparison")

        # Box Plot of Actual Productivity by Department
        st.subheader("Comparison: Box Plot of Actual Productivity by Department")
        fig6 = px.box(data, x='department', y='actual_productivity', title='Box Plot of Actual Productivity by Department')
        st.plotly_chart(fig6, use_container_width=True)

        # Average Productivity per Day (Stacked Bar Plot)
        st.subheader("Comparison: Average Productivity per Day")
        avg_productivity_per_day = data.groupby('day')['actual_productivity'].mean().reset_index()
        avg_productivity_per_day['Average Productivity'] = avg_productivity_per_day['actual_productivity']
        avg_productivity_per_day.drop(columns=['actual_productivity'], inplace=True)
        fig_avg_productivity_per_day = px.bar(avg_productivity_per_day, x='day', y='Average Productivity',
                                            title='Average Productivity per Day', labels={'day': 'Day', 'Average Productivity': 'Average Productivity'},
                                            color='Average Productivity', color_continuous_scale='viridis')
        st.plotly_chart(fig_avg_productivity_per_day, use_container_width=True)

        # Actual vs Targeted Productivity (Bar Plot)
        st.subheader("Comparison: Actual vs Targeted Productivity (Bar Plot)")
        fig_actual_target_bar = px.bar(data, x='targeted_productivity', y='actual_productivity',
                                        labels={'targeted_productivity': 'Targeted Productivity',
                                                'actual_productivity': 'Actual Productivity'},
                                        title='Comparison: Actual vs Targeted Productivity (Bar Plot)')
        st.plotly_chart(fig_actual_target_bar)

        # Actual Productivity vs Productivity Difference (Scatter Plot)
        st.subheader("Comparison: Actual Productivity vs Productivity Difference (Scatter Plot)")
        fig_actual_difference_scatter = px.scatter(data, x='productivity_difference', y='actual_productivity',
                                                    labels={'productivity_difference': 'Productivity Difference',
                                                            'actual_productivity': 'Actual Productivity'},
                                                    title='Comparison: Actual Productivity vs Productivity Difference (Scatter Plot)')
        st.plotly_chart(fig_actual_difference_scatter)

    # Composition
    elif visualization_option == "Composition":
        st.header("Composition")

        # Composition Quarter
        st.header("Composition Quarter")
        fig_quarter = px.pie(data, names='quarter', title='Composition Quarter')
        st.plotly_chart(fig_quarter)

        # Composition Department
        st.header("Composition Department")
        fig_department = px.pie(data, names='department', title='Composition Department')
        st.plotly_chart(fig_department)

        # Composition Day
        st.header("Composition Day")
        fig_day = px.pie(data, names='day', title='Composition Day')
        st.plotly_chart(fig_day)

        # Composition Team
        st.header("Composition Team")
        fig_team = px.pie(data, names='team', title='Composition Team')
        st.plotly_chart(fig_team)

                # Kolom yang ingin diplot Compositionnya
        # Kolom yang ingin diplot Compositionnya
        columns_to_plot = ['targeted_productivity', 'smv', 'wip', 'over_time', 'incentive', 'no_of_workers', 'actual_productivity', 'productivity_difference']

        # Loop through each column
        for column in columns_to_plot:
            st.header(f"Composition {column.replace('_', ' ').title()}")
            fig = px.histogram(data, x=column, title=f"Composition {column.replace('_', ' ').title()}", labels={'count': 'Count'})
            st.plotly_chart(fig)

    # Hubungan
    elif visualization_option == "Relationship":
        st.header("Relationship")

        # Heatmap Korelasi
        st.subheader("Heatmap Korelasi")
        numeric_columns = data.select_dtypes(include=['float64', 'int64'])
        correlation_matrix = numeric_columns.corr()
        fig9 = px.imshow(correlation_matrix, color_continuous_scale='blues', labels=dict(x="Variabel", y="Variabel", color="Korelasi"))
        st.plotly_chart(fig9, use_container_width=True)
        # Penjelasan Korelasi
        st.write("Korelasi adalah ukuran statistik yang menunjukkan seberapa kuat hubungan antara dua variabel. Nilai korelasi berkisar dari -1 hingga 1.")
        st.write("Nilai 1 menunjukkan korelasi positif sempurna, sementara nilai -1 menunjukkan korelasi negatif sempurna. Nilai 0 menunjukkan tidak adanya korelasi.")
        st.write("Berikut adalah matriks korelasi antar variabel dalam dataset:")
        st.write(correlation_matrix)

        # Penjelasan Korelasi untuk Setiap Variabel
        st.write("Berikut Penjelasan Korelasi untuk Setiap Variabel:")
        st.write("1. *Department*: Ada hubungan positif yang kuat antara departemen dengan targeted_productivity, no_of_workers, dan incentive. Ada hubungan negatif yang kuat dengan wip dan productivity_difference.")
        st.write("2. *Team*: Pola korelasi di sini mirip dengan departemen, dengan hubungan positif yang kuat dengan targeted_productivity, no_of_workers, dan incentive, dan hubungan negatif yang kuat dengan wip dan productivity_difference.")
        st.write("3. *SMV*: Ada hubungan positif yang kuat antara SMV dengan incentive, yang berarti semakin tinggi nilai SMV, semakin besar kemungkinan ada insentif yang diberikan. Ada hubungan negatif yang kuat antara SMV dengan wip.")
        st.write("4. *WIP*: Korelasi negatif yang kuat antara wip dengan variabel lain menunjukkan bahwa semakin tinggi jumlah pekerjaan yang masih dalam proses, semakin rendah produktivitas atau insentif yang diberikan, dan sebaliknya.")
        st.write("5. *Over Time*: Hubungan positif yang kuat dengan over_time menunjukkan bahwa semakin banyak waktu lembur yang digunakan, semakin tinggi kemungkinan adanya insentif atau peningkatan jumlah pekerja.")
        st.write("6. *Incentive*: Hubungan positif yang kuat dengan incentive menunjukkan bahwa semakin besar insentif yang diberikan, semakin tinggi kemungkinan ada peningkatan produktivitas atau pekerjaan yang dilakukan oleh tim.")
        st.write("7. *No of Workers*: Ada hubungan positif yang kuat antara jumlah pekerja dengan variabel lain seperti department, team, smv, over_time, dan incentive.")
        st.write("8. *Productivity Difference*: Korelasi positif yang kuat dengan variabel lain menunjukkan bahwa semakin besar perbedaan antara produktivitas yang ditargetkan dan aktual, semakin besar kemungkinan adanya pekerjaan yang masih dalam proses atau waktu lembur yang digunakan.")
        st.write("9. *Actual Productivity*: Korelasi negatif yang kuat dengan productivity_difference menunjukkan bahwa semakin besar perbedaan antara produktivitas yang ditargetkan dan aktual, semakin rendah produktivitas aktualnya.")
        
elif nav_selection == "Predict":
    # Input fields
    st.header("Input Features")

    # Select box for quarter
    quarter_options = list(range(value_ranges['quarter'][0], value_ranges['quarter'][1]+1))  # Buat daftar nilai opsional
    quarter = st.selectbox("Quarter", quarter_options)

    # Select box for department
    department_options = list(range(value_ranges['department'][0], value_ranges['department'][1]+1))  # Buat daftar nilai opsional
    department = st.selectbox("Department", department_options)

    # Slider for day
    day = st.slider("Day", min_value=value_ranges['day'][0], max_value=value_ranges['day'][1], step=1)

    # Slider for team
    team = st.slider("Team", min_value=value_ranges['team'][0], max_value=value_ranges['team'][1], step=1)

    # Slider for targeted productivity
    targeted_productivity = st.slider("Targeted Productivity", min_value=value_ranges['targeted_productivity'][0], max_value=value_ranges['targeted_productivity'][1], step=0.01)

    # Slider for smv
    smv = st.slider("SMV", min_value=value_ranges['smv'][0], max_value=value_ranges['smv'][1], step=0.01)

    # Slider for incentive
    incentive = st.slider("Incentive", min_value=value_ranges['incentive'][0], max_value=value_ranges['incentive'][1], step=1)

    # Slider for productivity difference
    productivity_difference = st.slider("Productivity Difference", min_value=value_ranges['productivity_difference'][0], max_value=value_ranges['productivity_difference'][1], step=0.01)

    # Number input for WIP
    wip = st.number_input("WIP", min_value=value_ranges['wip'][0], max_value=value_ranges['wip'][1], step=1)

    # Number input for over time
    over_time = st.number_input("Over Time", min_value=value_ranges['over_time'][0], max_value=value_ranges['over_time'][1], step=1)

    # Slider for number of workers
    no_of_workers = st.slider("Number of Workers", min_value=value_ranges['no_of_workers'][0], max_value=value_ranges['no_of_workers'][1], step=1)

    # Make prediction
    if st.button("Predict"):
        prediction = predict_productivity(quarter, department, day, team, targeted_productivity, smv, wip, over_time, incentive, no_of_workers, productivity_difference)
        st.write(f"Predicted Actual Productivity: {prediction}")
