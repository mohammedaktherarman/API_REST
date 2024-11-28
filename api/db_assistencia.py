from client import db_client

def consultar_asistencia(id_alumno: int, fecha: str):
    try:
        conn = db_client()
        cur = conn.cursor()

        query = """
            SELECT a.fecha, g.nombre_grupo, s.nombre_asignatura, a.presente, a.hora_inici, a.hora_final
            FROM asistencia a
            JOIN grupo g ON a.id_grupo = g.id_grupo
            JOIN asignatura s ON a.id_asignatura = s.id_asignatura
            WHERE a.id_alumno = %s AND a.fecha = %s
        """
        cur.execute(query, (id_alumno, fecha))
        resultado = cur.fetchall()

        if not resultado:
            return None

        asistencias = []
        for fila in resultado:
            asistencias.append({
                "fecha": fila[0],
                "grupo": fila[1],
                "asignatura": fila[2],
                "presente": bool(fila[3]),
                "hora_inicio": str(fila[4]),
                "hora_final": str(fila[5])
            })
        return asistencias

    finally:
        conn.close()

def registrar_asistencia(fecha: str, grupo: str, asignatura: str, alumnos: list[int], hora_inicio: str, hora_final: str):
    try:
        conn = db_client()
        cur = conn.cursor()

        # Transformar fecha a DD-MM-YYYY
        fecha_transformada = "-".join(reversed(fecha.split("-")))

        query_grupo = "SELECT id_grupo FROM grupo WHERE nombre_grupo = %s"
        cur.execute(query_grupo, (grupo,))
        id_grupo = cur.fetchone()
        if not id_grupo:
            raise ValueError(f"Grupo '{grupo}' no encontrado.")

        query_asignatura = "SELECT id_asignatura FROM asignatura WHERE nombre_asignatura = %s"
        cur.execute(query_asignatura, (asignatura,))
        id_asignatura = cur.fetchone()
        if not id_asignatura:
            raise ValueError(f"Asignatura '{asignatura}' no encontrada.")

        for id_alumno in alumnos:
            query_asistencia = """
                INSERT INTO asistencia (id_alumno, id_grupo, id_asignatura, fecha, hora_inici, hora_final, presente)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query_asistencia, (id_alumno, id_grupo[0], id_asignatura[0], fecha_transformada, hora_inicio, hora_final, True))

        conn.commit()

    finally:
        conn.close()

