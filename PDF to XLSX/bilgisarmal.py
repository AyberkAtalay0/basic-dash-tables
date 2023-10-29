import pandas as pd
import pdftables_api

def read_pdf(pdfname):
    # pdftables_api_key = "tl3ruxm1wnpl"
    # pdftables_api.Client(pdftables_api_key).xlsx_single(pdfname, "bilgisarmalraw")
    # xlsx = pd.ExcelFile("bilgisarmalraw.xlsx")
    # raw_df = None
    # for sheet_name in xlsx.sheet_names[:7]:
    #     page_df = pd.read_excel(xlsx, sheet_name)
    #     if type(raw_df) == type(None): raw_df = page_df.iloc[2:]
    #     else: raw_df = pd.concat([raw_df, page_df.iloc[2:]])
    # df = raw_df.iloc[:198] # MAX ROW
    # df.dropna(subset=[raw_df.columns[3], raw_df.columns[4], raw_df.columns[5], raw_df.columns[6]], inplace=True)
    raw_df = pd.read_excel("bilgisarmaltg1raw.xlsx").fillna(0)

    df = pd.DataFrame.from_dict({"Index": raw_df[raw_df.columns[1]]}).set_index("Index")
    df["Numara"] = [int(float(str(i).replace(" ","").split("-")[0])) for i in raw_df[raw_df.columns[2]]]
    df["İsim"] = [str(i).strip() for i in raw_df[raw_df.columns[3]]]
    df["Sınıf"] = [str(i).strip().replace(str(i).strip()[-1]," / "+str(i).strip()[-1]) for i in raw_df[raw_df.columns[4]]]
    df["D (Toplam)"] = [int(float(i)) for i in raw_df[raw_df.columns[-8]]]
    df["Y (Toplam)"] = [int(float(i)) for i in raw_df[raw_df.columns[-7]]]
    df["N (Toplam)"] = [float(str(i).replace(",",".")) for i in raw_df[raw_df.columns[-8]]]
    df["D (Türkçe)"] = [int(float(i)) for i in raw_df[raw_df.columns[5]]]
    df["Y (Türkçe)"] = [int(float(i)) for i in raw_df[raw_df.columns[6]]]
    df["N (Türkçe)"] = [float(str(i).replace(",",".")) for i in raw_df[raw_df.columns[7]]]
    df["D (Sosyal)"] = [int(float(t))+int(float(c))+int(float(f))+int(float(d)) for t, c, f, d in zip(raw_df[raw_df.columns[8]], raw_df[raw_df.columns[11]], raw_df[raw_df.columns[14]], raw_df[raw_df.columns[17]])]
    df["Y (Sosyal)"] = [int(float(t))+int(float(c))+int(float(f))+int(float(d)) for t, c, f, d in zip(raw_df[raw_df.columns[9]], raw_df[raw_df.columns[12]], raw_df[raw_df.columns[15]], raw_df[raw_df.columns[18]])]
    df["N (Sosyal)"] = [float(str(t).replace(",","."))+float(str(c).replace(",","."))+float(str(f).replace(",","."))+float(str(d).replace(",",".")) for t, c, f, d in zip(raw_df[raw_df.columns[10]], raw_df[raw_df.columns[13]], raw_df[raw_df.columns[16]], raw_df[raw_df.columns[19]])]
    df["D (Matematik)"] = [int(float(m))+int(float(g)) for m, g in zip(raw_df[raw_df.columns[23]], raw_df[raw_df.columns[26]])]
    df["Y (Matematik)"] = [int(float(m))+int(float(g)) for m, g in zip(raw_df[raw_df.columns[24]], raw_df[raw_df.columns[27]])]
    df["N (Matematik)"] = [float(str(m).replace(",","."))+float(str(g).replace(",",".")) for m, g in zip(raw_df[raw_df.columns[25]], raw_df[raw_df.columns[28]])]
    df["D (Fen)"] = [int(float(f))+int(float(k))+int(float(b)) for f, k, b in zip(raw_df[raw_df.columns[29]], raw_df[raw_df.columns[32]], raw_df[raw_df.columns[35]])]
    df["Y (Fen)"] = [int(float(f))+int(float(k))+int(float(b)) for f, k, b in zip(raw_df[raw_df.columns[30]], raw_df[raw_df.columns[33]], raw_df[raw_df.columns[36]])]
    df["N (Fen)"] = [float(str(f).replace(",","."))+float(str(k).replace(",","."))+float(str(b).replace(",",".")) for f, k, b in zip(raw_df[raw_df.columns[31]], raw_df[raw_df.columns[34]], raw_df[raw_df.columns[37]])]
    df["Kurum"] = df.index.tolist()
    df["İlçe"] = 0
    df["İl"] = 0
    df["Genel"] = [int(float(str(i).replace(",",""))) for i in raw_df[raw_df.columns[42]]]
    return df

if __name__ == "__main__":
    d = read_pdf("bilgisarmal tg1.pdf")
    d.to_excel("bilgisarmal tg1.xlsx")