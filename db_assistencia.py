from client import db_client

def alumnes_assistir(IdAssignatura, Dia, Grup):
    try:
        conn = db_client()
        cur = conn.cursor()

        query = """
            SELECT u.usuari_id, u.nom, u.grup_id FROM usuari u WHERE u.grup_id = %s AND u.usuari_id IN ( SELECT l.professor_id FROM llista l WHERE l.assignatura_id = %s AND l.dia = %s
            )
        """
        cur.execute(query, (Grup, IdAssignatura, Dia))
        alumnes = cur.fetchall()

    finally:
        conn.close()
    
    return alumnes

def marcar_assistencia(IdAlumne, IdAssignatura, Dia, Estat):
    try:
        conn = db_client()
        cur = conn.cursor()

        query = """
            INSERT INTO assistencia (usuari_id, assignatura_id, dia, estat)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE estat = %s
        """
        values = (IdAlumne, IdAssignatura, Dia, Estat, Estat)
        cur.execute(query, values)
        conn.commit()
    except Exception as e:
        print(f"Error al marcar asistencia: {e}")
    finally:
        conn.close()

def obtenir_grups():
    try:
        conn = db_client()
        cur = conn.cursor()

        query = "SELECT grup_id, nom_grup FROM grup"
        cur.execute(query)
        grups = cur.fetchall()

    finally:
        conn.close()

    return grups