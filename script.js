document.getElementById("consultarBtn").addEventListener("click", async () => {
    const fecha = document.getElementById("fecha").value;
    const idAlumno = document.getElementById("id_alumno").value;

    try {
        const response = await fetch("http://127.0.0.1:8000/asistencia/alumno", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ fecha, id_alumno: parseInt(idAlumno) })
        });

        if (!response.ok) {
            document.getElementById("result").innerHTML = `<p>Error</p>`;
            return;
        }

        const data = await response.json();
        
        let table = `<table>
            <tr>
                <th>Fecha</th>
                <th>Grupo</th>
                <th>Asignatura</th>
                <th>Presente</th>
                <th>Hora Inicio</th>
                <th>Hora Final</th>
            </tr>`;
        data.forEach(asistencia => {
            table = table + `
            <tr>
                <td>${asistencia.fecha}</td>
                <td>${asistencia.grupo}</td>
                <td>${asistencia.asignatura}</td>
                <td>${asistencia.presente ? "Sí" : "No"}</td>
                <td>${asistencia.hora_inicio}</td>
                <td>${asistencia.hora_final}</td>
            </tr>`;
        });
        table = table + "</table>";
        document.getElementById("result").innerHTML = table;

    } catch (error) {
        document.getElementById("result").innerHTML = "<p>Error</p>";
    }
});