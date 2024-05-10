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
        Dari grafik tersebut, kita dapat melihat bahwa tidak terdapat pola yang konsisten yang mengindikasikan peningkatan atau penurunan linier dalam produktivitas seiring dengan peningkatan SMV. Misalnya, ketika SMV berada dalam rentang 2 hingga 3.99, produktivitas aktualnya mencapai 226.9359. Namun, ketika SMV berada dalam rentang 12 hingga 13.99, produktivitas aktualnya secara drastis menurun menjadi hanya 1.25021.

        Hal ini menunjukkan bahwa terdapat faktor-faktor kompleks lainnya yang memengaruhi produktivitas, yang tidak dapat secara langsung diatribusikan hanya pada jumlah jam kerja yang digunakan.
        """

        # Menampilkan paragraf menggunakan st.write
        st.write(paragraph)


        fig_histogram3 = px.histogram(data, y='actual_productivity', x='wip', title='Distribution of Actual Productivity vs WIP')
        fig_histogram3.update_traces(marker=dict(color='rgba(100, 149, 237, 0.7)', line=dict(color='rgba(0,0,0,0.5)', width=0.5)), opacity=0.75)
        fig_histogram3.update_layout(bargap=0.1)
        st.plotly_chart(fig_histogram3)
        import streamlit as st
        st.write("Grafik menunjukkan bahwa ada hubungan yang jelas antara jumlah pekerjaan dalam proses (Work in Progress/WIP) dan produktivitas aktual. Saat jumlah WIP naik dari 0-199 menjadi 200-399, ada lonjakan signifikan dalam produktivitas dari 7.324 menjadi 13.635. Pola ini berlanjut hingga mencapai puncaknya pada rentang WIP 1000-1199, di mana produktivitas mencapai nilai tertinggi sebesar 485.425. Namun, setelah mencapai titik ini, produktivitas menurun saat WIP meningkat menjadi 1200-1399, menunjukkan adanya kemungkinan penurunan efisiensi saat beban kerja melebihi kapasitas optimal. Penurunan ini terus terjadi ketika WIP berada dalam rentang 1400-1999, menunjukkan bahwa beban kerja yang terlalu besar dapat menurunkan produktivitas secara signifikan.")
        st.write("Kesimpulannya, data menunjukkan bahwa pengelolaan jumlah WIP sangat penting untuk menjaga produktivitas yang optimal. Jumlah WIP yang terlalu sedikit dapat menyebabkan sumber daya tidak optimal, sedangkan jumlah yang terlalu banyak dapat mengganggu alur kerja dan menurunkan efisiensi.")


        fig_histogram4 = px.histogram(data, y='actual_productivity', x='over_time', title='Distribution of Actual Productivity vs Over Time')
        fig_histogram4.update_traces(marker=dict(color='rgba(100, 149, 237, 0.7)', line=dict(color='rgba(0,0,0,0.5)', width=0.5)), opacity=0.75)
        fig_histogram4.update_layout(bargap=0.1)
        st.plotly_chart(fig_histogram4)
        st.write("""
Hasil grafik menunjukkan korelasi antara jam lembur dan produktivitas aktual. Ketika jam lembur masih sedikit, produktivitas juga rendah. Namun, lonjakan signifikan dalam produktivitas terjadi saat jam lembur meningkat. Puncak produktivitas tercapai pada rentang jam lembur tertentu, tetapi setelahnya terjadi penurunan, mungkin karena kelelahan atau penurunan efisiensi.

Kesimpulannya, meskipun jam lembur berkontribusi positif pada produktivitas, peningkatan yang berlebihan tidak selalu menghasilkan peningkatan yang proporsional. Oleh karena itu, manajemen jam lembur harus bijaksana untuk menjaga efisiensi dan kesejahteraan karyawan.
""")



        fig_histogram5 = px.histogram(data, y='actual_productivity', x='incentive', title='Distribution of Actual Productivity vs Incentive')
        fig_histogram5.update_traces(marker=dict(color='rgba(100, 149, 237, 0.7)', line=dict(color='rgba(0,0,0,0.5)', width=0.5)), opacity=0.75)
        fig_histogram5.update_layout(bargap=0.1)
        st.plotly_chart(fig_histogram5)
        st.write("Grafik batang 'Distribusi Produktivitas Sebenarnya vs Insentif' menggambarkan bagaimana pemberian insentif kepada pekerja memengaruhi produktivitas mereka. Secara menarik, terlihat bahwa ketika insentif diberikan, produktivitas sebenarnya cenderung menurun. Hal yang menarik, titik tertinggi produktivitas tercapai ketika tidak ada insentif yang diberikan. Ini menunjukkan bahwa dalam beberapa situasi, insentif mungkin tidak menjadi faktor utama dalam meningkatkan produktivitas. Secara keseluruhan, grafik tersebut menyoroti bahwa respons produktivitas terhadap insentif tidak selalu sesuai harapan. Terkadang, memberikan lebih banyak insentif tidak akan berdampak pada peningkatan produktivitas sebagaimana yang diantisipasi. Ini menegaskan perlunya mempertimbangkan faktor lain yang mungkin mempengaruhi kinerja pekerja saat merancang sistem insentif yang efektif.")


        fig_histogram6 = px.histogram(data, y='actual_productivity', x='no_of_workers', title='Distribution of Actual Productivity vs Number of Workers')
        fig_histogram6.update_traces(marker=dict(color='rgba(100, 149, 237, 0.7)', line=dict(color='rgba(0,0,0,0.5)', width=0.5)), opacity=0.75)
        fig_histogram6.update_layout(bargap=0.1)
        st.plotly_chart(fig_histogram6)
        st.write("Dalam grafik tersebut, terdapat sumbu horizontal yang menunjukkan jumlah pekerja mulai dari 0 hingga 80. Sedangkan sumbu vertikal menampilkan jumlah produktivitas aktual dari 0 hingga 300.")
        st.write("Pada grafik tersebut, terdapat batang dengan ketinggian yang berbeda-beda yang mewakili jumlah produktivitas aktual untuk setiap jumlah pekerja. Terdapat satu batang yang sangat tinggi di sekitar 60 pekerja, menunjukkan jumlah produktivitas aktual yang tinggi untuk jumlah pekerja tersebut. Sementara batang lainnya lebih pendek, menunjukkan jumlah produktivitas yang lebih rendah untuk jumlah pekerja yang berbeda.")
        st.write("Dengan demikian, grafik tersebut menunjukkan bahwa jumlah pekerja yang optimal untuk mencapai produktivitas tertinggi adalah sekitar 60 pekerja, yang menghasilkan jumlah produktivitas aktual yang paling tinggi.")

        fig_histogram7 = px.histogram(data, x='targeted_productivity', y='actual_productivity', title='Actual Productivity vs Targeted Productivity')
        fig_histogram7.update_traces(marker=dict(color='rgba(100, 149, 237, 0.7)', line=dict(color='rgba(0,0,0,0.5)', width=0.5)), opacity=0.75)
        fig_histogram7.update_layout(bargap=0.1)
        st.plotly_chart(fig_histogram7)
        st.write("""
        Grafik ini membandingkan Actual Productivity (Produktivitas Aktual) dengan Targeted Productivity (Produktivitas yang Ditargetkan). 
        Sumbu x menunjukkan nilai Targeted Productivity, seperti 0.6, 0.65, 0.7, 0.75, dan 0.8, sementara sumbu y menunjukkan jumlah Actual Productivity, berkisar dari 0 hingga 400.

        Setiap batang pada grafik mewakili nilai Targeted Productivity. Tinggi batang menunjukkan jumlah Actual Productivity untuk setiap nilai tersebut. 
        Batang yang lebih pendek, seperti untuk nilai 0.6 dan 0.65, menunjukkan Actual Productivity yang lebih rendah, sedangkan batang yang lebih tinggi, seperti untuk nilai 0.7 dan 0.75, menunjukkan Actual Productivity yang lebih tinggi. 
        Yang paling menonjol adalah batang untuk nilai 0.8, menandakan jumlah Actual Productivity tertinggi pada tingkat Targeted Productivity tersebut.

        Secara keseluruhan, grafik ini menyarankan bahwa Actual Productivity mencapai puncaknya saat Targeted Productivity diatur pada 0.8. 
        Dengan kata lain, semakin tinggi nilai Targeted Productivity, semakin tinggi kemungkinan Actual Productivity juga meningkat. 
        Ini mengindikasikan bahwa ketika Targeted Productivity yang ditetapkan lebih tinggi, Actual Productivity cenderung naik.
        """)

        fig_scatter = px.scatter(data, x='productivity_difference', y='actual_productivity', title='Actual Productivity vs Productivity Difference')
        st.plotly_chart(fig_scatter)
        # Explanation
        explanation = """
        Grafik yang menunjukkan garis naik menunjukkan bahwa ketika ada perbedaan antara produktivitas aktual dengan target yang ditetapkan (yang kita sebut sebagai "Productivity Difference"), produktivitas aktual cenderung meningkat. Misalnya, jika hasil kerja aktual lebih tinggi dari target yang ditetapkan, produktivitas aktual juga cenderung lebih tinggi. Begitu juga sebaliknya, jika hasil kerja aktual lebih rendah dari target, produktivitas aktual cenderung menurun.

        Jadi, semakin besar perbedaan antara produktivitas aktual dan target yang ditetapkan, semakin besar juga kemungkinan bahwa produktivitas aktual akan meningkat atau menurun. Dalam grafik ini, kita melihat pola umum bahwa ketika perbedaan antara hasil aktual dan target semakin besar, produktivitas aktual cenderung meningkat secara keseluruhan.
        """

        # Display the explanation
        st.write(explanation)

    # Comparison
    elif visualization_option == "Comparison":
        st.header("Comparison")

        # Box Plot of Actual Productivity by Department
        st.subheader("Comparison: Box Plot of Actual Productivity by Department")
        fig6 = px.box(data, x='department', y='actual_productivity', title='Box Plot of Actual Productivity by Department')
        st.plotly_chart(fig6, use_container_width=True)
        st.write("- **Jumlah Data**: Departemen 1 memiliki lebih banyak data (623) dibandingkan dengan Departemen 0 (468).")
        st.write("- **Rata-rata Actual Productivity**: Rata-rata produktivitas aktual di Departemen 0 (0.7619) sedikit lebih tinggi daripada di Departemen 1 (0.7524).")
        st.write("- **Standar Deviasi**: Standar deviasi Departemen 0 (0.1785) lebih tinggi dibandingkan dengan Departemen 1 (0.1202). Yang menunjukkan bahwa variasi dalam produktivitas aktual lebih besar di Departemen 0.")
        st.write("- **Kuartil**: Distribusi data antara kedua departemen ini bervariasi, yang ditunjukkan oleh perbedaan dalam nilai kuartil pertama (25%), median, dan kuartil ketiga (75%).")
        st.write("- **Nilai Minimum dan Maksimum**: Meskipun nilai minimum dan maksimum cukup serupa untuk kedua departemen, namun rentang (range) nilai actual productivity cukup bervariasi di antara keduanya.")
        st.write("Kesimpulannya, meskipun rata-rata produktivitas aktual di Departemen 0 lebih tinggi, variasi dalam kinerja karyawan lebih besar daripada di Departemen 1. Hal ini menunjukkan bahwa meskipun ada beberapa perbedaan dalam kinerja antara kedua departemen, perlu diperhatikan bahwa faktor lain juga dapat memengaruhi produktivitas, seperti faktor lingkungan kerja, sumber daya, atau kebijakan perusahaan.")

        # Average Productivity per Day (Stacked Bar Plot)
        st.subheader("Comparison: Average Productivity per Day")
        avg_productivity_per_day = data.groupby('day')['actual_productivity'].mean().reset_index()
        avg_productivity_per_day['Average Productivity'] = avg_productivity_per_day['actual_productivity']
        avg_productivity_per_day.drop(columns=['actual_productivity'], inplace=True)
        fig_avg_productivity_per_day = px.bar(avg_productivity_per_day, x='day', y='Average Productivity',
                                            title='Average Productivity per Day', labels={'day': 'Day', 'Average Productivity': 'Average Productivity'},
                                            color='Average Productivity', color_continuous_scale='viridis')
        st.plotly_chart(fig_avg_productivity_per_day, use_container_width=True)
        st.write("- **Hari 0**: Rata-rata produktivitas aktual pada hari ini adalah 0.7572.")
        st.write("- **Hari 1**: Rata-rata produktivitas aktual pada hari ini adalah 0.7753.")
        st.write("- **Hari 2**: Rata-rata produktivitas aktual pada hari ini adalah 0.7439.")
        st.write("- **Hari 3**: Rata-rata produktivitas aktual pada hari ini adalah 0.7428.")
        st.write("- **Hari 4**: Rata-rata produktivitas aktual pada hari ini adalah 0.7663.")
        st.write("- **Hari 5**: Rata-rata produktivitas aktual pada hari ini adalah 0.7548.")

        st.write("Dari data tersebut, terlihat bahwa rata-rata produktivitas aktual cenderung bervariasi setiap harinya. Misalnya, hari 1 memiliki rata-rata tertinggi dengan 0.7753, sedangkan hari 3 memiliki rata-rata terendah dengan 0.7428. Hal ini menunjukkan adanya perubahan dalam kinerja produktivitas selama periode tersebut.")

        fig_box = px.box(data, x='quarter', y='actual_productivity', title='Box Plot: Actual Productivity by Quarter')
        st.plotly_chart(fig_box)
        # Explanation
        st.write("""
        - **Kuartal 0** memiliki rata-rata (mean) tertinggi dengan nilai 0.7674, sementara **Kuartal 2** memiliki rata-rata terendah dengan 0.7307.
        - **Kuartal 0** juga memiliki median (nilai tengah) tertinggi dengan 0.8001, menunjukkan bahwa sebagian besar data cenderung berada di atas nilai ini. Sedangkan **Kuartal 2** memiliki median terendah dengan 0.7501.
        - Persebaran (25th Percentile dan 75th Percentile) dalam **Kuartal 0** dan **Kuartal 1** cukup serupa, tetapi cenderung lebih rendah di **Kuartal 2** dan **Kuartal 3**. Namun, **Kuartal 4** memiliki nilai persebaran tertinggi, menunjukkan adanya variasi yang lebih besar dalam data produktivitas aktual.
        - Rentang nilai (Min dan Max) dalam **Kuartal 4** sangat besar, dengan nilai minimum 0.4277 dan maksimum 1.0005. Hal ini menunjukkan adanya variasi yang signifikan dalam produktivitas aktual selama kuartal tersebut. Sedangkan kuartal lainnya memiliki rentang nilai yang lebih rendah.

        Dari ringkasan tersebut, dapat disimpulkan bahwa:

        1. **Kuartal 0 dan Kuartal 1** memiliki kinerja yang relatif serupa, dengan rata-rata dan median yang hampir sama tingginya. Ini menunjukkan konsistensi dalam produktivitas selama dua kuartal pertama.
        2. **Kuartal 2 dan Kuartal 3** memiliki rata-rata dan median yang sedikit lebih rendah dibandingkan dengan dua kuartal sebelumnya. Ini mungkin mengindikasikan adanya tantangan atau fluktuasi dalam kinerja selama periode ini.
        3. **Kuartal 4** menonjol dengan kinerja yang signifikan, ditandai dengan rata-rata yang jauh lebih tinggi dan rentang nilai yang sangat besar. Hal ini bisa menunjukkan adanya perubahan besar dalam faktor-faktor yang memengaruhi produktivitas selama kuartal tersebut, baik dalam hal peningkatan atau penurunan kinerja.

        Kesimpulannya, sementara kuartal pertama dan kedua menunjukkan konsistensi dalam kinerja, kuartal ketiga menunjukkan sedikit penurunan, dan kuartal keempat menonjol dengan perubahan yang signifikan, baik itu peningkatan atau penurunan, dalam produktivitas.
        """)
    elif visualization_option == "Composition":
        st.header("Composition")

        # Composition Quarter
        jumlah_quarter = data['quarter'].value_counts().reset_index()
        jumlah_quarter.columns = ['quarter', 'count']
        fig_quarter = px.pie(jumlah_quarter, names='quarter', values='count', title='Composition Quarter')
        st.plotly_chart(fig_quarter)
                # Penjelasan distribusi pekerjaan di setiap kuartal
        st.write("Komposisi pekerjaan di setiap kuartal menunjukkan jumlah pekerjaan yang dilakukan dalam rentang waktu yang berbeda-beda selama periode tertentu, yang dibagi menjadi kuartal.")
        st.write("- *Kuartal 0*: Terdapat 342 pekerjaan yang dilakukan selama kuartal ini.")
        st.write("- *Kuartal 1*: Pada kuartal ini, dilakukan sebanyak 295 pekerjaan.")
        st.write("- *Kuartal 2*: Terdapat 226 pekerjaan yang dilakukan selama kuartal ini.")
        st.write("- *Kuartal 3*: Pada kuartal ini, terdapat 187 pekerjaan yang dilakukan.")
        st.write("- *Kuartal 4*: Jumlah pekerjaan paling sedikit terjadi pada kuartal ini, hanya terdapat 41 pekerjaan.")

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
        st.write("Dari jumlah data yang diberikan, terlihat bahwa:")
        st.write("- Hari 0: Terdapat 177 data.")
        st.write("- Hari 1: Terdapat 172 data.")
        st.write("- Hari 2: Terdapat 192 data.")
        st.write("- Hari 3: Terdapat 177 data.")
        st.write("- Hari 4: Terdapat 182 data.")
        st.write("- Hari 5: Terdapat 191 data.")
        st.write("")
        st.write("Hasil ini menunjukkan bahwa jumlah pekerjaan paling banyak dilakukan pada Hari 2 dengan total 192 data, yang menandakan bahwa Hari 2 adalah saat di mana pekerjaan paling sibuk dilakukan dalam dataset. Sedangkan Hari 1 memiliki jumlah pekerjaan yang paling sedikit dilakukan, yaitu 172 data.")

        # Composition Team
        jumlah_team = data['team'].value_counts().reset_index()
        jumlah_team.columns = ['team', 'count']
        fig_team = px.pie(jumlah_team, names='team', values='count', title='Composition Team')
        st.plotly_chart(fig_team)
        st.write("Dari data tersebut, terlihat bahwa:")
        st.write("- Tim 1: Terdapat 98 data.")
        st.write("- Tim 2: Terdapat 102 data.")
        st.write("- Tim 3: Terdapat 86 data.")
        st.write("- Tim 4: Terdapat 95 data.")
        st.write("- Tim 5: Terdapat 78 data.")
        st.write("- Tim 6: Terdapat 87 data.")
        st.write("- Tim 7: Terdapat 83 data.")
        st.write("- Tim 8: Terdapat 94 data.")
        st.write("- Tim 9: Terdapat 101 data.")
        st.write("- Tim 10: Terdapat 95 data.")
        st.write("- Tim 11: Terdapat 76 data.")
        st.write("- Tim 12: Terdapat 96 data.")
        st.write("")
        st.write("Dari data tersebut, terlihat bahwa jumlah pekerjaan paling banyak dilakukan pada Tim 9 dengan total 101 data. Yang menunjukkan bahwa pekerjaan paling sibuk dilakukan oleh Tim 9 dalam dataset ini. Sedangkan jumlah pekerjaan yang paling sedikit dilakukan adalah pada Tim 11 dengan hanya 76 data.")

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
