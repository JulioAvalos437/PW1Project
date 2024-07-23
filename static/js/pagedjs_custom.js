class MyHandler extends Paged.Handler {
    constructor(chunker, polisher, caller) {
        super(chunker, polisher, caller);
    }

    beforeParsed(content) {
        // Crear el contenido del primer encabezado
        let header = document.createElement('p');
        header.className = 'header';
        content.prepend(header);
        console.log(codCarrera)
        // Crear el contenido del segundo encabezado como un párrafo con dos spans
        let header2 = document.createElement('p');
        let span1 = document.createElement('span');
        switch (codCarrera) {
        case "KTII":
            span1.innerHTML = 'Carrera de Ingeniería en Informática';
            header.innerHTML = 'UNIVERSIDAD NACIONAL DE CAAGUAZU<br>Con sede en Coronel Oviedo<br><b>FACULTAD DE CIENCIAS Y TECNOLOGÍAS</b><br>CARRERA DE INGENIERIA EN INFORMÁTICA<br>PLAN CURRICULAR 2010<br><b>PROGRAMA DE ESTUDIOS</b>';
        break;
        case "KTIC":
            span1.innerHTML = 'Carrera de Ingeniería Civil';
            header.innerHTML = 'UNIVERSIDAD NACIONAL DE CAAGUAZU<br>Con sede en Coronel Oviedo<br><b>FACULTAD DE CIENCIAS Y TECNOLOGÍAS</b><br>CARRERA DE INGENIERIA CIVIL<br>PLAN CURRICULAR 2013<br><b>PROGRAMA DE ESTUDIOS</b>';
        break;
        case "KTIE":
            span1.innerHTML = 'Carrera de Ingeniería en Electricidad';
            header.innerHTML = 'UNIVERSIDAD NACIONAL DE CAAGUAZU<br>Con sede en Coronel Oviedo<br><b>FACULTAD DE CIENCIAS Y TECNOLOGÍAS</b><br>CARRERA DE INGENIERIA EN ELECTRICIDAD<br>PLAN CURRICULAR 2010<br><b>PROGRAMA DE ESTUDIOS</b>';
        break;
        case "KTIL":
            span1.innerHTML = 'Carrera de Ingeniería en Electrónica';
            header.innerHTML = 'UNIVERSIDAD NACIONAL DE CAAGUAZU<br>Con sede en Coronel Oviedo<br><b>FACULTAD DE CIENCIAS Y TECNOLOGÍAS</b><br>CARRERA DE INGENIERIA EN ELECTRÓNICA<br>PLAN CURRICULAR 2010<br><b>PROGRAMA DE ESTUDIOS</b>';
        break;

        default:
        // Código a ejecutar si la expresión no coincide con ninguno de los valores anteriores
        break;
}

        span1.className = 'left-span';
        let span2 = document.createElement('span');
        span2.innerHTML = 'Facultad de Ciencias Tecnológicas – UNCA';
        span2.className = 'right-span';
        header2.appendChild(span1);
        header2.appendChild(span2);
        header2.className = 'header2';
        content.prepend(header2);
    }
}

Paged.registerHandlers(MyHandler);
