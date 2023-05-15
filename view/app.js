let container = "";
let api_request = "http://practice.test7.bmsoft.de:8000/vat4l-api";

function Vat4lApp() {
    /* **********************************************************************
    Klasse zur Steuerung und Bereitstellung der Funktionalität der Anwendung

    Stand: 08.05.2023
    Author: Andreas Bendig
    Version 0.1
    ********************************************************************** */

    this.init = function () {
        // Initialisiert ein Objekt der Klasse, legt den Anwendungsbereich
        // auf den Container fest und lädt den ersten Inhalt beim Laden der Seite.

        container = document.querySelector("#container");
        //this.getByPath();
        this.getJobList();
    }

    //--------------------------------------------------------------------
    this.getJobList = async function () {
        // Lädt mithilfe der REST-API eine Übersicht der verfügbaren Jobs
        // @return: Promise

        let resultlist1 = await this.callAPI(api_request + '/jobs');

        // Festlegung der Spalten-Werte unf Überschriften:
        let col_size = ["2", "3", "3", "2", "2"];
        let job_column_names = ["Auswahl", "Start", "Ende", "verarbeite Verzeichnisse", "verarbeitete Dateien"];

        // Schreiben der Daten:
        container.insertAdjacentHTML('beforeend', this.printJobList(job_column_names, col_size, resultlist1));

        let boxes = document.querySelectorAll('input[type="checkbox"]');
        boxes.forEach(this.addCheckboxListener)
    }

    this.addCheckboxListener = function (currentValue) {
        document.addEventListener('change', function () {
            checkboxSelected(currentValue);
        })
    }

    //--------------------------------------------------------------------
    this.callAPI = async function (str_api_call) {
        // Führt einen API-Aufruf aus und liefert das Ergebnis zurück
        // @param:  str_api_call    - String. Fertige URL des gewünschten API-Aufrufs mit
        // @return: Promise

        try {
            let res = await fetch(str_api_call);
            return await res.json();
        } catch (err) {
            console.error(err);
        }
    }

    //--------------------------------------------------------------------
    this.getResultList = async function (source, target) {
        // Führt einen API-Aufruf aus und liefert die Unterschiede von
        // zwei Jobs zurück und gibt diese auf dem Bildschirm aus.
        // @param:  source - String. ID des ersten Jobs, mit dem verglichen wird
        //          target - String. ID des zweiten Jobs, mit dem die Quelle verglichen wird

        // Festlegung der Spalten-Werte unf Überschriften:
        let col_size = ["4", "1", "1", "1", "1", "2", "2"];
        let column_names = ["Pfad", "Größe [Byte]", "Benutzer", "Gruppe", "Dateirechte", "erstellt am", "letzte Änderung am"];

        // Durchführung der API-Aufrufe
        let resultlist1 = await this.callAPI(api_request + '/getdelta/' + source + '/' + target);
        let resultlist2 = await this.callAPI(api_request + '/comparejobs/' + source + '/' + target);
        let job_source = await this.callAPI(api_request + '/getjob/' + source);
        let job_target = await this.callAPI(api_request + '/getjob/' +target);

        let deleted_data = [];
        let created_data = [];
        let changed_data = [];

        // Trennung von neuen und gelöschten Elementen in separate
        // Ausgabeblöcke auf dem Bildschirm.

        for (let i = 0; i <= resultlist1.length - 1; i++) {

            let data_source= new ResultlistRow();
            let data_target = new ResultlistRow();

            data_source.id = i;
            data_source.path = resultlist1[i].path;
            data_target.id = i;

            let datablock =[];

            if (resultlist1[i].job_id.toString() === source) {
                // Datensatz wurde gelöscht
                data_source.init(resultlist1[i]);
                datablock = {data_source, data_target}

                deleted_data.push(datablock)
            } else {
                data_target.init(resultlist1[i])
                datablock = {data_source, data_target}

                created_data.push(datablock)
            }
        }

        for (let i = 0; i <= resultlist2.length - 1; i++) {

            let datablock =[];
            let data_source= new ResultlistRow();
            let data_target = new ResultlistRow();

            data_source.id = i;
            data_target.id = i;

            data_target.init(resultlist2[i]);

            data_source.path= resultlist2[i].path;
            data_source.size= resultlist2[i].s_size;
            data_source.username= resultlist2[i].s_user_name;
            data_source.groupname= resultlist2[i].s_group_name;
            data_source.filemode= resultlist2[i].s_filemode;
            data_source.set_created_date(resultlist2[i].s_created_date);
            data_source.set_modified_date(resultlist2[i].s_modified_date);

            datablock = {data_source, data_target}
            changed_data.push(datablock)
        }

         // Es wurden keine Unterschiede gefunden
        if((created_data.length === 0) && (deleted_data.length === 0) && (resultlist2.length === 0)) {
            let html_no_result =
                `<div>
                <p>Es wurden keine Unterschiede zwischen den Jobs mit den ID's ${job_source[0].id_job} von ${new DateFormatter(job_source[0].dt_end_job).date_formatted} und ${job_target[0].id_job} vom ${new DateFormatter(job_target[0].dt_end_job).date_formatted} gefunden.</p>
             </div>`

            document.querySelector("#container").insertAdjacentHTML('beforeend', html_no_result);
        } else {
            let html_compinfo =
                `<div>
                <p>Es wurden die Jobs mit den ID's ${job_source[0].id_job} von ${new DateFormatter(job_source[0].dt_end_job).date_formatted} und ${job_target[0].id_job} vom ${new DateFormatter(job_target[0].dt_end_job).date_formatted} miteinander verglichen. Dabei wurden folgende Unterschiede vom System erkannt:</p>
                <ul>
                    <li>Es wurden ` + created_data.length + ` neue Dateien gefunden <a href="#pos_createdData"><ion-icon name="arrow-down-outline" /></a></li>
                    <li>` + deleted_data.length + ` Dateien wurden aus den Verzeichnissen entfernt <a href="#pos_deletedData"><ion-icon name="arrow-down-outline" /></a></li>
                    <li>Es sind ` + changed_data.length + ` Anpassungen in Dateien vorgenommen worden <a href="#pos_changedData"><ion-icon name="arrow-down-outline" /></a></li>   
                </ul> 
                <p style="font-size: xx-small">(Unterschiedliche Werte werden als Quelle/Ziel im Vergleich dargestellt.)</p>
             </div>`

            document.querySelector("#container").insertAdjacentHTML('beforeend', html_compinfo);

            //Ausgabe der Ergebnisse auf dem Bildschirm:
            // Neue Inhalte:
            if (created_data.length > 0) {
                this.addHeadLine("createdData", "Neue Elemente:", "#container");
                let html1 = this.printResultList(column_names, col_size, "tbl_created", "#createdData", created_data);
                document.querySelector("#createdData").insertAdjacentHTML('beforeend', html1);
            }
            // Gelöschte Inhalte:
            if (deleted_data.length > 0) {
                this.addHeadLine("deletedData", "Gelöschte Elemente:", "#container");
                let html2 = this.printResultList(column_names, col_size, "tbl_deleted", "#deletedData", deleted_data);
                document.querySelector("#deletedData").insertAdjacentHTML('beforeend', html2);
            }
            // Unterschiedliche Inhalte
            if (resultlist2.length > 0) {
                this.addHeadLine("changedData", "Geänderte Elemente:", "#container");
                let html = this.printResultList(column_names, col_size, "tbl_changed", "#changedData", changed_data);
                document.querySelector("#changedData").insertAdjacentHTML('beforeend', html);
            }
        }


    }

    //--------------------------------------------------------------------
    this.printJobList = function (cols, col_size, data) {
        // Funktion generiert die tabellarische Ausgabe der Inhalte
        // für die Darstellung der Jobs
        // @param:  cols - String[]. Spaltenüberschriften von links nach rechts
        //          col-size - String[]. Breite der einzelnen Spalten im Bootstrap
        //          data - Object[]. Array der ermittelten Daten
        // @return: String - HTML der generierten Tabelle

        // Überschriften schreiben
        let html_head_txt = `
            <div>
                <p>Bitte wählen Sie zwei Jobs für einen Vergleich aus der Liste aus:</p><br>
            </div> 
        `
        document.querySelector("#container").insertAdjacentHTML('beforeend', html_head_txt);

        this.tableHeader("job_header", "#container");

        // SpaltenÜberschriften schreiben
        for (let i = 0; i <= cols.length - 1; i++) {
            this.printHeader(cols[i], col_size[i], "#job_header")
        }
        let html = ``;

        // Sammeln der einzelnen Spaltenwerte je Datenzeile
        for (let i = 0; i < data.length; i++) {
            let job = data[i];

             let html_style;
            if ( i % 2 === 0 ) {
                html_style="background-color: #eeeeee;"
            } else {
                html_style=""
            }

            // Füge für jeden Datensatz eine Zeile mit den Informationen hinzu
            html += `
                 <div class="row" style="${html_style}" id="job-element-${job.id_job}">${
                this.printCol("checkbox", "text-center", job.id_job, null, col_size[0]) +
                this.printCol("date", "text-center", new DateFormatter(job.dt_start_job).date_formatted, null, col_size[1]) +
                this.printCol("date", "text-center", new DateFormatter(job.dt_end_job).date_formatted, null, col_size[2]) +
                this.printCol("text", "text-center", job.int_processed_dir, null, col_size[3]) +
                this.printCol("text", "text-center", job.int_processed_file, null, col_size[4])}
                 </div>
                `;
        }
        return html;
    }

    //--------------------------------------------------------------------
    this.addHeadLine = function (id_headline, txt_headline, dom_element) {
        // Generiert eine Überschriftszeile für neue Inhaltsbereiche auf der Seite hinzu.
        // @param:  id_headline - String. Name des bereitzustellenden Containers für die weitere Verwendung
        //          txt_headline - String. Text der Überschrift
        //          dom_element - DOM-Element. Der Bereich, dem das zu generierende Element hinzugefügt wird.

        let html = `
            <div class="row"><h2 id="pos_${id_headline}">${txt_headline}</h2></div>
            <div id="${id_headline}"></div> 
        `;
        document.querySelector(dom_element).insertAdjacentHTML('beforeend', html);
    }

    //--------------------------------------------------------------------
    this.printResultList = function (cols, col_size, str_headerID, str_parentID, datablock) {
        // Generiert den HTML-Code der ermittelten Dateiinformationen
        // @param:  cols - String[]. Spaltenüberschriften von links nach rechts
        //          col-size - String[]. Breite der einzelnen Spalten im Bootstrap
        //          str_headerID - String. Der bereitgestellte Bereich, in dem die Überschriften geschrieben werden
        //          str_parentID - String. Das übergeordnete Element, in welchem diese Informationen angezeigt werden
        //          data - Object[]. Array der ermittelten Daten
        // @return: String. Liefert den HTML-Code der Daten in tabellarischer Form

        // Schreibe den Tabellenkopf:
        this.tableHeader(str_headerID, str_parentID)

        // Schreibe Spalten und Überschriften:
        for (let i = 0; i <= cols.length - 1; i++) {
            this.printHeader(cols[i], col_size[i], "#" + str_headerID)
        }

        let html = ``;

        // Ermittle den HTML-Code je Datenzeile:
        for (let i = 0; i <= datablock.length - 1; i++) {
            let element = datablock[i];
            let html_style;
            if ( i % 2 === 0 ) {
                html_style="background-color: #eeeeee;"
            } else {
                html_style=""
            }

            html += `
                         <div class="row" style="${html_style}" id="job-element-${element.data_source.id}">${
                // this.printCol("text", "text-center", element.id, col_size[0]) +
                // this.printCol("text", "text-center", element.job_id, col_size[1]) +
                this.printCol("text", "text-start", element.data_source.path, null, col_size[0]) +
                this.printCol("text", "text-center", element.data_source.size, element.data_target.size, col_size[1]) +
                //this.printCol("text", "text-center", element.hash, col_size[4]) +
                this.printCol("text", "text-center", element.data_source.username, element.data_target.username, col_size[2]) +
                this.printCol("text", "text-center", element.data_source.groupname, element.data_target.groupname, col_size[3]) +
                this.printCol("text", "text-center", element.data_source.filemode, element.data_target.filemode, col_size[4]) +
                this.printCol("date", "text-center", element.data_source.created_date, element.data_target.created_date, col_size[5]) +
                this.printCol("date", "text-center", element.data_source.modified_date, element.data_target.modified_date, col_size[6])
            }
                         </div>
                        `;
        }
        return html;
    }

    //--------------------------------------------------------------------
    this.printHeader = function (column_name, column_size, str_parent) {
        // Schreibt den Spaltentitel
        // @param:  column_name -   String. Titel der Spalte
        //          column_size -   String. Breite der Spalte für Bootstrap
        //          str_parent -    String. Name des Übergeordneten Elements
        //                          in welches dieser Inhalt geschrieben werden soll

        let html = `<div class="col-sm-${column_size}">
                <div class="text-center">
                    <strong>${column_name}</strong>
                </div>
            </div>
        `;
        document.querySelector(str_parent).insertAdjacentHTML('beforeend', html)
    }

    //--------------------------------------------------------------------
    this.tableHeader = function (str_headerID, str_parentID) {
        // Erstellt die Kopfzeile für die nachfolgende Datentabelle
        //@param:   str_headerID - String. Name des bereitzustellenden Bereiches
        //          str_parent -   String. Name des Übergeordneten Elements

        let html = `
            <div class="row" style="background-color: lightblue; padding-top: 5px; padding-bottom: 5px;" id="${str_headerID}">            
            </div>
        `;
        document.querySelector(str_parentID).insertAdjacentHTML('beforeend', html)
        //tbl_header = document.querySelector("#tbl-header");
    }

    //--------------------------------------------------------------------
    this.printCol = function (type, align, s_field, t_field, size) {
        // Schreibt Daten in eine Zelle der Tabellenstruktur
        // @param:  type - String. darf einen der nachfolgenden Werte enthalten:
        //                      - checkbox, date, text (default)
        //          align - String. Darf einen der nachfolgenden Werte enthalten:
        //                      - text-start, text-center, text-end
        //          field - String. Die Bezeichnung des Datenfeldes aus JSON
        //          size -  String. Zahlenwert zwischen 1 und 12. Definiert im Bootstrap,
        //                      wieviele Spalten optisch zu einer zusammengefasst werden.

        let html;
        let content = ""
        switch (type) {

            case "checkbox":
                // Zeichnet eine Checkbox:
                html = `<div class="col-sm-${size}" style="padding-top: 5px; font-size: small;">
                            <span class="${align}">
                                <input class="form-check-input mt-0" style="vertical-align: baseline" type="checkbox" id="selectID${s_field}" name="selectID" ="${s_field}" value="${s_field}">
                                <label for="selectID${s_field}" style="vertical-align: baseline">&nbsp;${s_field}</label> 
                            </span>
                      </div>`;
                break;

            case "date":
                if (t_field !== null) {
                    content = (s_field !== t_field) ? `<span>/ ${(t_field.replace("T", " - "))}</span>` : ``
                } else {
                    content = ``
                }

                //schreibt einen Datums-/Zeitwert:
                html = `<div class="col-sm-${size}">
                    <div class="${align} small">
                        <span>${(s_field.replace("T", " - "))}</span> ` + content + `
                    </div>
                </div>`;
                break;

            default:
                // Schreibt einen Text:
                if (t_field !== null) {
                    content = (s_field !== t_field) ? `<span>/ ${t_field}</span>` : ``
                } else {
                    content = ``
                }


                html = `<div class="col-sm-${size}">
                     <div class="${align} small"> 
                         <span>${s_field}</span> ` + content + `
                    </div>
                </div>`;

                break;
        }

        return html;
    }

    //--------------------------------------------------------------------
    this.getByPath = async function () {
        // Erstellt eine Oberfläche zur Auswahl eines Dateipfades

        // Liste aller Dateipfade laden:
        let pathlist;
        pathlist = await this.callAPI(api_request + '/getpathlist');

        // Optionsliste für das Selektionsfeld erstellen:
        let optionlist = [];
        for (i = 0; i < pathlist.length - 1; i++) {
            optionlist.push(`<option value="${pathlist[i].id}">${pathlist[i].path}</option>`)
        }

        // Auswahlfeld generieren und im Container einbinden:
        let html = `
            <div>
                <p>Bitte wählen Sie einen Pfad aus der Liste aus:</p>
                    <select id="path">
                        ${optionlist.toString()}"
                    </select>
                    <button type="button" class="btn-primary" onclick="getFileList()">Ausführen</button>
            </div>
        `

        container.insertAdjacentHTML('beforeend', html);
    }

    class DateFormatter {
        constructor(date_value) {
            this.date_formatted = this._prepareDate(date_value);
        }

        _prepareDate (datetime_value) {
            var elements= datetime_value.split("T");
            var date_elements= elements[0].split("-");
            var time_elements= elements[1].split(":");

            let date= new Date(date_elements[0], date_elements[1]-1, date_elements[2],time_elements[0], time_elements[1], time_elements[2]);
            return date.toLocaleDateString() + " "+ date.toLocaleTimeString();
        }
    }
    class ResultlistRow {
        constructor() {
            this.id=0
            this.path="";
            this.size=0;
            this.username="-";
            this.groupname="-";
            this.filemode="-";
            this.created_date="-";
            this.modified_date="-";
        }

        init (dataset) {
            this.path= dataset.path;
            this.size= dataset.size;
            this.username= dataset.user_name;
            this.groupname= dataset.group_name;
            this.filemode= dataset.filemode;
            this.created_date = new DateFormatter(dataset.created_date).date_formatted;
            this.modified_date = new DateFormatter(dataset.modified_date).date_formatted;
            /*
            if (dataset.created_date !== "-") {
                this.created_date= this._prepareDate(dataset.created_date);
            }
            if (dataset.modified_date !== "-") {
                this.modified_date= this._prepareDate(dataset.modified_date);
            }
             */
        }

        set_created_date(value) {
            if (value !== "-") {
                this.created_date= this._prepareDate(value);
            } else {
                this.created_date = "-"
            }
        }

        set_modified_date(value) {
            if (value !== "-") {

                this.modified_date= this._prepareDate(value);
            }else {
                this.modified_date = "-"
            }
        }
        _prepareDate (datetime_value) {
            var elements= datetime_value.split("T");
            var date_elements= elements[0].split("-");
            var time_elements= elements[1].split(":");

            let date= new Date(date_elements[0], date_elements[1]-1, date_elements[2],time_elements[0], time_elements[1], time_elements[2]);
            return date.toLocaleDateString() + " "+ date.toLocaleTimeString();
        }


    }
}

//--------------------------------------------------------------------
function getSelectedJobs() {
    // Liefert eine Liste der ersten zwei ausgewählten Einträge aus der
    // Datenliste zur weiteren Verarbeitung zurück

    let selectedJobs = [];

    let element = document.querySelectorAll('input[type="checkbox"]:checked');

    // Durchlaufe alle Einträge und merke die ausgewählten IDs:
    element.forEach(function (currentValue) {
        selectedJobs.push(currentValue.value)
    })
    return (selectedJobs);
}

//--------------------------------------------------------------------
function showSelectedJobs() {
    // Ermittelt die ausgewählten Jobs und generiert eine Ergebnisliste

    selection = getSelectedJobs();
    // Oberfläche zurücksetzen:
    clearContent();

    app.getResultList(selection[0], selection[1])
    document.querySelector('#btn_selectedJobs').classList.add('disabled')
}

//--------------------------------------------------------------------
function showJobList() {
    // Zeigt die Liste aller verfügbaren Jobs an.

    // Oberfläche zurücksetzen:
    clearContent();
    app.getJobList();
}

//--------------------------------------------------------------------
function clearContent() {
    // Löscht den Inhalt de Container-Elements
    document.querySelector("#container").innerHTML = "";
}

//--------------------------------------------------------------------
function showByPath() {
    clearContent();
    this.getByPath();
}

//--------------------------------------------------------------------
async function getFileList() {

    let selectedPathID = document.getElementById('path').value;

    let col_size = ["1", "1", "2", "1", "1", "1", "1", "1", "1", "2"];
    let column_names = ["ID", "Job ID", "Pfad", "Größe", "Hash-Wert", "Benutzer", "Gruppe", "Dateirechte", "erstellt am", "letzte Änderung am"];

    let resultlist = await this.callAPI(api_request + '/getfilebypath/' + selectedPathID);

}

function checkboxSelected(source) {
    let selectedBoxes = document.querySelectorAll('input[type="checkbox"]:checked').length;

    if (selectedBoxes === 2) {
        document.querySelector('#btn_selectedJobs').classList.remove('disabled')
    } else if (selectedBoxes > 2) {
        source.checked = false;
        document.querySelector('#btn_selectedJobs').classList.add('disabled')
    } else {
        document.querySelector('#btn_selectedJobs').classList.add('disabled')
    }

}

//--------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    app = new Vat4lApp();
    app.init();
})
