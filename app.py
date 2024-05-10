import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
        fig_histogram2 = px.histogram(data, y='actual_productivity', x='smv', title='Distribution of Actual Productivity vs SMV')
        fig_histogram2.update_traces(marker=dict(color='rgba(100, 149, 237, 0.7)', line=dict(color='rgba(0,0,0,0.5)', width=0.5)), opacity=0.75)
        fig_histogram2.update_layout(bargap=0.1)
        st.plotly_chart(fig_histogram2)# Menampilkan data dalam bentuk tabel
        # Paragraf yang akan ditampilkan menggunakan st.write
        paragraph = """
        Dari grafik tersebut, pola yang jelas dalam hubungan antara tingkat standar waktu kerja (SMV) dan produktivitas aktual tidak dapat ditemukan. Meskipun ada rentang SMV di mana produktivitas meningkat, seperti pada rentang 2 hingga 3.99, di mana produktivitas mencapai 226.9359, ada juga kasus di mana produktivitas secara drastis menurun meskipun SMV meningkat, seperti pada rentang 12 hingga 13.99, di mana produktivitas turun menjadi hanya 1.25021. Hal ini menunjukkan bahwa ada faktor-faktor kompleks lain yang memengaruhi produktivitas selain dari jumlah jam kerja yang digunakan."""

        # Menampilkan paragraf menggunakan st.write
        st.write(paragraph)


        fig_histogram3 = px.histogram(data, y='actual_productivity', x='wip', title='Distribution of Actual Productivity vs WIP')
        fig_histogram3.update_traces(marker=dict(color='rgba(100, 149, 237, 0.7)', line=dict(color='rgba(0,0,0,0.5)', width=0.5)), opacity=0.75)
        fig_histogram3.update_layout(bargap=0.1)
        st.plotly_chart(fig_histogram3)
        st.write("Grafik menunjukkan bahwa terdapat hubungan yang signifikan antara jumlah pekerjaan dalam proses (Work in Progress/WIP) dan produktivitas aktual. Saat jumlah WIP meningkat dari 0-199 menjadi 200-399, terjadi lonjakan produktivitas yang signifikan. Puncak produktivitas tercapai pada rentang WIP 1000-1199, sebelum mengalami penurunan ketika WIP terus meningkat melebihi kapasitas optimal. Hal ini menekankan pentingnya pengelolaan jumlah WIP untuk menjaga produktivitas yang optimal, dengan jumlah yang terlalu sedikit atau terlalu banyak dapat mengganggu efisiensi dalam alur kerja.")
        
        fig_histogram4 = px.histogram(data, y='actual_productivity', x='over_time', title='Distribution of Actual Productivity vs Over Time')
        fig_histogram4.update_traces(marker=dict(color='rgba(100, 149, 237, 0.7)', line=dict(color='rgba(0,0,0,0.5)', width=0.5)), opacity=0.75)
        fig_histogram4.update_layout(bargap=0.1)
        st.plotly_chart(fig_histogram4)
        st.write("""Hasil grafik menunjukkan korelasi yang signifikan antara jumlah jam lembur dan produktivitas aktual. Meskipun produktivitas cenderung meningkat saat jam lembur meningkat, terdapat titik di mana produktivitas mencapai puncaknya sebelum mengalami penurunan. Penurunan ini mungkin disebabkan oleh kelelahan atau penurunan efisiensi. Kesimpulannya, manajemen jam lembur harus dikelola dengan bijaksana untuk menjaga keseimbangan antara peningkatan produktivitas dan kesejahteraan karyawan.""")


        fig_histogram5 = px.histogram(data, y='actual_productivity', x='incentive', title='Distribution of Actual Productivity vs Incentive')
        fig_histogram5.update_traces(marker=dict(color='rgba(100, 149, 237, 0.7)', line=dict(color='rgba(0,0,0,0.5)', width=0.5)), opacity=0.75)
        fig_histogram5.update_layout(bargap=0.1)
        st.plotly_chart(fig_histogram5)
        st.write("Grafik 'Actual Productivity vs Incentive' menunjukkan bahwa pemberian insentif dapat memengaruhi produktivitas. Namun, menariknya, produktivitas cenderung menurun saat insentif diberikan, dengan titik tertinggi tercapai tanpa insentif. Ini menunjukkan bahwa insentif tidak selalu menjadi faktor utama dalam meningkatkan produktivitas, dan perlu mempertimbangkan faktor lain dalam merancang sistem insentif yang efektif.")


        fig_histogram6 = px.histogram(data, y='actual_productivity', x='no_of_workers', title='Distribution of Actual Productivity vs Number of Workers')
        fig_histogram6.update_traces(marker=dict(color='rgba(100, 149, 237, 0.7)', line=dict(color='rgba(0,0,0,0.5)', width=0.5)), opacity=0.75)
        fig_histogram6.update_layout(bargap=0.1)
        st.plotly_chart(fig_histogram6)
        st.write("Grafik tersebut memperlihatkan hubungan antara jumlah pekerja dan produktivitas aktual. Di sumbu horizontal, jumlah pekerja ditampilkan dari 0 hingga 80, sedangkan di sumbu vertikal, produktivitas aktual ditampilkan dari 0 hingga 300. Setiap batang dalam grafik mewakili jumlah produktivitas untuk setiap jumlah pekerja. Terdapat satu batang yang mencapai ketinggian yang sangat tinggi di sekitar 60 pekerja, menandakan produktivitas tertinggi yang dicapai pada jumlah pekerja ini. Ini menunjukkan bahwa jumlah pekerja optimal untuk mencapai produktivitas tertinggi adalah sekitar 60 orang.")

        fig_histogram7 = px.histogram(data, x='targeted_productivity', y='actual_productivity', title='Actual Productivity vs Targeted Productivity')
        fig_histogram7.update_traces(marker=dict(color='rgba(100, 149, 237, 0.7)', line=dict(color='rgba(0,0,0,0.5)', width=0.5)), opacity=0.75)
        fig_histogram7.update_layout(bargap=0.1)
        st.plotly_chart(fig_histogram7)
        st.write("""Grafik membandingkan Actual Productivity (Produktivitas Aktual) dengan Targeted Productivity (Produktivitas yang Ditargetkan). Setiap batang pada grafik mewakili nilai Targeted Productivity, di mana tinggi batang menunjukkan jumlah Actual Productivity untuk setiap nilai tersebut. Secara keseluruhan, grafik menunjukkan bahwa Actual Productivity mencapai puncaknya saat Targeted Productivity diatur pada 0.8. Dengan demikian, peningkatan nilai Targeted Productivity cenderung berdampak positif pada Actual Productivity.""")

        fig_scatter = px.scatter(data, x='productivity_difference', y='actual_productivity', title='Actual Productivity vs Productivity Difference')
        st.plotly_chart(fig_scatter)
        # Explanation
        explanation = """ Grafik menunjukkan bahwa ketika terjadi perbedaan antara produktivitas aktual dan target yang ditetapkan (Productivity Difference), produktivitas aktual cenderung berubah. Ketika hasil kerja aktual lebih tinggi dari target, produktivitas aktual juga cenderung meningkat, dan sebaliknya. Pola umum yang terlihat adalah semakin besar perbedaan antara hasil aktual dan target, semakin besar juga kemungkinan bahwa produktivitas aktual akan meningkat atau menurun. """

        # Display the explanation
        st.write(explanation)

    # Comparison
    elif visualization_option == "Comparison":

        # Box Plot of Actual Productivity by Department
        fig6 = px.box(data, x='department', y='actual_productivity', title='Box Plot of Actual Productivity by Department')
        st.plotly_chart(fig6, use_container_width=True)
        st.write("Departemen 1 memiliki lebih banyak data daripada Departemen 0, tetapi rata-rata produktivitas aktual di Departemen 0 sedikit lebih tinggi. Variasi dalam produktivitas di Departemen 0 lebih besar daripada di Departemen 1. Hal ini berarti di Departemen 0, kinerja karyawan bisa sangat berbeda-beda, sementara di Departemen 1, kinerja karyawan lebih stabil. Meskipun ada perbedaan dalam kinerja antara departemen, faktor lain seperti lingkungan kerja dan kebijakan perusahaan juga memengaruhi produktivitas.")
        

        # Average Productivity per Day (Stacked Bar Plot)
        avg_productivity_per_day = data.groupby('day')['actual_productivity'].mean().reset_index()
        avg_productivity_per_day['Average Productivity'] = avg_productivity_per_day['actual_productivity']
        avg_productivity_per_day.drop(columns=['actual_productivity'], inplace=True)
        fig_avg_productivity_per_day = px.bar(avg_productivity_per_day, x='day', y='Average Productivity',
                                            title='Average Productivity per Day', labels={'day': 'Day', 'Average Productivity': 'Average Productivity'},
                                            color='Average Productivity', color_continuous_scale='viridis')
        st.plotly_chart(fig_avg_productivity_per_day, use_container_width=True)
        st.write("Data menunjukkan variasi dalam rata-rata produktivitas aktual dari hari ke hari. Misalnya, hari 1 memiliki rata-rata tertinggi dengan 0.7753, sedangkan hari 3 memiliki rata-rata terendah dengan 0.7428. Hal ini menunjukkan adanya perubahan dalam kinerja produktivitas selama periode waktu yang diamati.")

        fig_box = px.box(data, x='quarter', y='actual_productivity', title='Box Plot: Actual Productivity by Quarter')
        st.plotly_chart(fig_box)
        # Explanation
        st.write("""
 Berdasarkan data, tampaknya dua kuartal pertama memiliki hasil yang hampir sama. Hal ini menunjukkan bahwa pekerjaan berjalan dengan baik pada awal tahun. Namun, di kuartal ketiga, produktivitas sedikit menurun. Di kuartal terakhir, ada perubahan besar. Mungkin ada banyak hal yang terjadi pada saat itu, baik yang baik maupun yang buruk, yang memengaruhi produktivitas. Jadi, kesimpulannya, dua kuartal pertama stabil, kuartal ketiga turun sedikit, dan kuartal terakhir memiliki perubahan besar.
        """)
    elif visualization_option == "Composition":

        # Composition Quarter
        jumlah_quarter = data['quarter'].value_counts().reset_index()
        jumlah_quarter.columns = ['quarter', 'count']
        fig_quarter = px.pie(jumlah_quarter, names='quarter', values='count', title='Composition Quarter')
        st.plotly_chart(fig_quarter)
                # Penjelasan distribusi pekerjaan di setiap kuartal
        st.write("Data komposisi pekerjaan menunjukkan variasi jumlah pekerjaan dalam setiap kuartal selama periode tertentu. Misalnya, kuartal 0 memiliki 342 pekerjaan, sementara kuartal 4 hanya memiliki 41 pekerjaan. Variasi ini dapat memengaruhi produktivitas secara langsung. Jika jumlah pekerjaan rendah, karyawan mungkin memiliki lebih sedikit tekanan, yang dapat meningkatkan efisiensi. Namun, peningkatan jumlah pekerjaan bisa menyebabkan kelelahan dan penurunan produktivitas.")

        # Composition Department
        jumlah_department = data['department'].value_counts().reset_index()
        jumlah_department.columns = ['department', 'count']
        fig_department = px.pie(jumlah_department, names='department', values='count', title='Composition Department')
        st.plotly_chart(fig_department)
        st.write("Pekerjaan lebih banyak dilakukan pada Department 1, dengan total 623 data (57.1%). Yang menunjukkan bahwa ada lebih banyak pekerjaan yang dilakukan di Department 1 dibandingkan dengan Department 0, yang memiliki total 468 data (42.9%). Meskipun kedua departemen ini memiliki aktivitas, namun Department 1 adalah yang paling sibuk dalam hal jumlah pekerjaan yang dilakukan, berdasarkan data yang tersedia.")

        # Composition Day
        jumlah_day = data['day'].value_counts().reset_index()
        jumlah_day.columns = ['day', 'count']
        fig_day = px.pie(jumlah_day, names='day', values='count', title='Composition Day')
        st.plotly_chart(fig_day)
        st.write("Perubahan jumlah pekerjaan setiap hari dapat langsung memengaruhi produktivitas. Saat beban kerja meningkat, terutama pada Hari 2, bisa menimbulkan stres dan kelelahan, berpotensi menurunkan produktivitas. Sebaliknya, pada hari dengan jumlah pekerjaan yang lebih sedikit, seperti Hari 1, karyawan memiliki lebih banyak waktu untuk fokus pada tugas mereka, meningkatkan produktivitas. Dengan memahami perubahan ini, manajemen dapat merencanakan dan mengelola sumber daya dengan lebih efektif untuk mempertahankan produktivitas yang optimal.")

        # Composition Team
        jumlah_team = data['team'].value_counts().reset_index()
        jumlah_team.columns = ['team', 'count']
        fig_team = px.pie(jumlah_team, names='team', values='count', title='Composition Team')
        st.plotly_chart(fig_team)
        st.write("Dari data tersebut, terlihat bahwa jumlah pekerjaan paling banyak dilakukan pada Tim 9 dengan total 101 data. Yang menunjukkan bahwa pekerjaan paling sibuk dilakukan oleh Tim 9 dalam dataset ini. Sedangkan jumlah pekerjaan yang paling sedikit dilakukan adalah pada Tim 11 dengan hanya 76 data. Variasi dalam beban kerja antara tim-tim dapat memengaruhi produktivitas. Tim yang lebih sibuk mungkin mengalami tekanan dan kelelahan yang dapat menurunkan produktivitas, sementara tim yang kurang sibuk dapat fokus lebih baik pada tugas-tugas mereka, meningkatkan produktivitas.")

    # Hubungan
    elif visualization_option == "Relationship":

        # Heatmap Korelasi
        st.subheader("Heatmap Korelasi")
        numeric_columns = data.select_dtypes(include=['float64', 'int64'])
        correlation_matrix = numeric_columns.corr()
        fig9 = px.imshow(correlation_matrix, color_continuous_scale='blues', labels=dict(x="Variabel", y="Variabel", color="Korelasi"))
        st.plotly_chart(fig9, use_container_width=True)
        # Penjelasan Korelasi untuk Setiap Variabel
        st.write("""
        - Korelasi adalah ukuran statistik yang menunjukkan hubungan antara dua variabel, dengan nilai dari -1 hingga 1.
        - Korelasi positif terlihat antara departemen dan tim dengan targeted_productivity, no_of_workers, dan incentive.
        - Korelasi negatif terlihat antara departemen dan tim dengan wip dan productivity_difference.
        - SMV berkorelasi positif dengan incentive, tetapi negatif dengan wip.
        - WIP berkorelasi negatif dengan variabel lain, menunjukkan semakin tinggi jumlah pekerjaan yang masih dalam proses, semakin rendah produktivitas atau insentif yang diberikan.
        - Over Time berkorelasi positif dengan insentif, menunjukkan semakin banyak waktu lembur yang digunakan, semakin tinggi kemungkinan adanya insentif.
        - Korelasi positif juga terlihat antara jumlah pekerja dengan variabel lain seperti department, team, smv, over_time, dan incentive.
        - Korelasi negatif terlihat antara productivity_difference dan actual_productivity, menunjukkan semakin besar perbedaan antara produktivitas yang ditargetkan dan aktual, semakin rendah produktivitas aktualnya.
        """)

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
