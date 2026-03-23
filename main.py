import polars as pl
#importo el archivo process
import process
route = r"C:\Users\Usuario\Desktop\project_icfes\data_raw\Examen_Saber_11_20201.csv"
scaner_route = pl.scan_csv(route, separator= ";", encoding="utf8-lossy")
send_route = process.filter_colums(scaner_route)
send_group = process.group_colums(send_route, "cole_depto_ubicacion")
result_end = send_group.collect()
print(result_end)