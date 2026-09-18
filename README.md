# Dashboard-BPJS — SI-HIS Health & Epidemiology Intelligence

Dashboard prototype untuk perspektif BPJS/JKN:
- 10 besar penyakit rawat jalan
- 10 besar penyakit rawat inap
- epidemiologi regional provinsi/kabupaten/kecamatan/FKTP
- FKTP preventive-care intelligence
- utilization, cost dan quality signals
- EWS dampak JKN
- Download Resume Analisis SI-HIS
- Download Data Sheet Analisis dengan Analysis ID

## Prinsip
SI-HIS menjadi intelligence layer; dashboard tidak membuat keputusan KLB sendiri.
Signal epidemiologi, utilisasi, biaya, mutu dan preventive-care opportunity harus dapat ditelusuri ke data yang menjadi dasar analisis.

## Demo
`streamlit run app.py`

Data pada `data/demo` hanya fixture demonstrasi dan bukan data BPJS nyata.

## Produksi
Hubungkan dashboard ke Intelligence API SI-HIS dengan authority scope dan data contract yang disepakati. Data individual harus mengikuti hak akses, perjanjian pertukaran data, keamanan, dan ketentuan perlindungan data yang berlaku.
