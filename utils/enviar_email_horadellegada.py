import pandas as pd
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def enviar_email(destinatario, asunto, cuerpo):
    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = EMAIL_USER
    msg["To"] = destinatario
    msg.set_content(cuerpo)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

def enviar_notificaciones_email(csv_path):
    df = pd.read_csv(csv_path)

    # Coordenadas a excluir (inicio y fin)
    coord_excluir = (-68.33957, -34.641042)

    # Filtrar filas válidas
    df_filtrado = df[
        ~((df["longitud"] == coord_excluir[0]) & (df["latitud"] == coord_excluir[1]))
    ]

    # Iterar por cada grupo y enviar correos
    for grupo, sub_df in df_filtrado.groupby("grupo"):
        for _, row in sub_df.iterrows():
            hora = row["hora_estimada_llegada"]
            enviar_email(
                destinatario="p.balastegui@alumno.um.edu.ar",
                asunto=f"Notificación para destino del grupo {grupo}",
                cuerpo=f"Tu técnico ya comenzó el recorrido, estará en tu domicilio aproximadamente a las {hora}."
            )

# Ejecutar si se corre directamente
if __name__ == "__main__":
    enviar_notificaciones_email("data/resultados_con_tiempos.csv")
