
import io, json, os
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

st.set_page_config(page_title="SI-HIS BPJS Health Intelligence", page_icon="🏥", layout="wide")

@st.cache_data(ttl=30)
def load_demo():
    p = Path("data/demo/bpjs_intelligence.json")
    return json.loads(p.read_text(encoding="utf-8"))

from pathlib import Path

data = load_demo()

st.title("SI-HIS BPJS Health Intelligence")
st.caption("JKN Population Health • Epidemiology • Utilization • Cost • Quality • Preventive Care")

with st.sidebar:
    st.header("Scope & Period")
    level = st.selectbox("Level wilayah", ["Nasional", "Provinsi", "Kabupaten/Kota", "Kecamatan", "FKTP"])
    period = st.selectbox("Periode", ["7 Hari", "30 Hari", "90 Hari"])
    province = st.selectbox("Provinsi", ["Semua", "DI Yogyakarta", "Jawa Barat", "Jawa Timur"])
    service = st.selectbox("Jenis pelayanan", ["Semua", "Rawat Jalan", "Rawat Inap"])
    st.divider()
    st.info("Dashboard mengikuti authority scope BPJS. Data individual harus mengikuti hak akses, perjanjian data, dan ketentuan perlindungan data.")

scope = f"{level} • {province}"
st.success(f"Scope aktif: {scope} | Periode: {period}")

k = data["summary"]
c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("Peserta JKN", f"{k['participants']:,}")
c2.metric("Rawat Jalan", f"{k['outpatient_visits']:,}", k["outpatient_delta"])
c3.metric("Rawat Inap", f"{k['inpatient_episodes']:,}", k["inpatient_delta"])
c4.metric("Klaim", f"Rp {k['claims_trillion']:.2f} T", k["claims_delta"])
c5.metric("Alert Epidemiologi", k["alerts"])
c6.metric("FKTP Terpantau", f"{k['fktp']:,}")

st.divider()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🦠 Epidemiologi", "🏥 Rawat Jalan", "🏨 Rawat Inap",
    "🩺 FKTP Preventif", "💰 Cost & Quality", "📥 Download & Evidence"
])

with tab1:
    st.subheader("10 Besar Penyakit — Rawat Jalan & Rawat Inap")
    left,right = st.columns(2)
    out = pd.DataFrame(data["top_outpatient"])
    inp = pd.DataFrame(data["top_inpatient"])
    with left:
        st.markdown("### Rawat Jalan")
        st.dataframe(out, use_container_width=True, hide_index=True)
        st.bar_chart(out.set_index("Penyakit")["Kunjungan"])
    with right:
        st.markdown("### Rawat Inap")
        st.dataframe(inp, use_container_width=True, hide_index=True)
        st.bar_chart(inp.set_index("Penyakit")["Episode"])

    st.subheader("Epidemiologi Regional")
    regional = pd.DataFrame(data["regional"])
    st.dataframe(regional, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Rawat Jalan Intelligence")
    out = pd.DataFrame(data["top_outpatient"])
    st.dataframe(out, use_container_width=True, hide_index=True)
    st.markdown("**Interpretasi:** pola diagnosis rawat jalan digunakan sebagai sinyal beban penyakit pada pintu depan layanan. Analisis preventif harus mempertimbangkan tren, populasi, continuity of care, dan konteks klinis; bukan hanya volume kunjungan.")

with tab3:
    st.subheader("Rawat Inap Intelligence")
    inp = pd.DataFrame(data["top_inpatient"])
    st.dataframe(inp, use_container_width=True, hide_index=True)
    st.markdown("**Clinical journey:** FKTP → referral → FKRTL → rawat inap → outcome → pembiayaan. Hubungan tersebut perlu dianalisis berdasarkan data episode yang benar-benar tersedia.")

with tab4:
    st.subheader("FKTP Preventive Care Intelligence")
    fktp = pd.DataFrame(data["fktp"])
    st.dataframe(fktp, use_container_width=True, hide_index=True)
    st.markdown("### Preventive-care signals")
    for x in data["preventive_signals"]:
        st.info(x)
    st.caption("Signal preventif bukan klaim bahwa rawat inap tertentu pasti dapat dicegah. Validasi klinis, definisi indikator, dan konteks populasi diperlukan.")

with tab5:
    st.subheader("Cost, Utilization & Quality")
    cost = pd.DataFrame(data["cost_quality"])
    st.dataframe(cost, use_container_width=True, hide_index=True)
    st.subheader("EWS Dampak JKN")
    for a in data["alerts"]:
        st.warning(a)

with tab6:
    st.subheader("Download & Evidence")
    analysis_id = data["analysis_id"]
    st.code(analysis_id)
    resume = {
        "analysis_id": analysis_id,
        "generated_at": data["generated_at"],
        "scope": scope,
        "period": period,
        "purpose": "JKN Health & Epidemiology Intelligence",
        "key_findings": data["key_findings"],
        "top_outpatient": data["top_outpatient"],
        "top_inpatient": data["top_inpatient"],
        "regional": data["regional"],
        "fktp_preventive_signals": data["preventive_signals"],
        "provenance": data["provenance"],
    }
    rjson = json.dumps(resume, ensure_ascii=False, indent=2).encode("utf-8")
    ds = pd.DataFrame(data["analysis_dataset"])
    csv = ds.to_csv(index=False).encode("utf-8-sig")
    st.download_button("📄 Download Resume Analisis SI-HIS", rjson, f"{analysis_id}_resume.json", "application/json")
    st.download_button("📊 Download Data Sheet Analisis", csv, f"{analysis_id}_data_sheet.csv", "text/csv")
    st.caption("Data Sheet adalah dataset analisis pada prototype. Produksi harus mengisinya dari episode pelayanan yang benar-benar digunakan oleh Intelligence API.")

st.divider()
st.caption(f"Analysis ID: {data['analysis_id']} • Generated: {data['generated_at']} • Engine: {data['provenance']['engine_version']}")
