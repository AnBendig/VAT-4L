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
        this.getByPath();
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

        let boxes= document.querySelectorAll('input[type="checkbox"]');
        boxes.forEach(this.addCheckboxListener)
    }

    this.addCheckboxListener= function(currentValue) {
        document.addEventListener('change', function() {
               checkboxSelected(currentValue);
           })
    }

    //--------------------------------------------------------------------
    this.callAPI = async function (str_api_call) {
        // Führt einen API-Aufruf aus und liefert das Ergebnis zurück
        // @param:  str_api_call    - String. Fertige URL des gewünschten API-Aufrufes mit
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
        let col_size = ["1", "1", "2", "1", "1", "1", "1", "1", "1", "2"];
        let column_names = ["ID", "Job ID", "Pfad", "Größe", "Hash-Wert", "Benutzer", "Gruppe", "Dateirechte", "erstellt am", "letzte Änderung am"];

        // Durchführung der API-Aufrufe
        let resultlist1 = await this.callAPI(api_request + '/getdelta/' + source + '/' + target);
        let resultlist2 = await this.callAPI(api_request + '/comparejobs/' + source + '/' + target);

        let deleted_data = [];
        let created_data = [];

        // Trennung von neuen und gelöschten Elementen in separate
        // Ausgabeblöcke auf dem Bildschirm.

        for (let i = 0; i <= resultlist1.length - 1; i++) {
            if (resultlist1[i].job_id.toString() === source) {
                deleted_data.push(resultlist1[i])
            } else {
                created_data.push(resultlist1[i])
            }
        }

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
            let html = this.printResultList(column_names, col_size, "tbl_changed", "#changedData", resultlist2);
            document.querySelector("#changedData").insertAdjacentHTML('beforeend', html);
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
        this.tableHeader("job_header", "#container");

        // SpaltenÜberschriften schreiben
        for (let i = 0; i <= cols.length - 1; i++) {
            this.printHeader(cols[i], col_size[i], "#job_header")
        }
        let html = ``;

        // Sammeln der einzelnen Spaltenwerte je Datenzeile
        for (let i = 0; i < data.length; i++) {
            let job = data[i];

            // Füge für jeden Datensatz eine Zeile mit den Informationen hinzu
            html += `
                 <div class="row" id="job-element-${job.id_job}">${
                this.printCol("checkbox", "text-center", job.id_job, col_size[0]) +
                this.printCol("date", "text-center", job.dt_start_job, col_size[1]) +
                this.printCol("date", "text-center", job.dt_end_job, col_size[2]) +
                this.printCol("text", "text-center", job.int_processed_dir, col_size[3]) +
                this.printCol("text", "text-center", job.int_processed_file, col_size[4])}
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
            <div class="row"><h2>${txt_headline}</h2></div>
            <div id="${id_headline}"></div> 
        `;
        document.querySelector(dom_element).insertAdjacentHTML('beforeend', html);
    }

    //--------------------------------------------------------------------
    this.printResultList = function (cols, col_size, str_headerID, str_parentID, data) {
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
        for (let i = 0; i <= data.length - 1; i++) {
            let element = data[i];

            html += `
                         <div class="row" id="job-element-${element.id_job}">${
                this.printCol("text", "text-center", element.id, col_size[0]) +
                this.printCol("text", "text-center", element.job_id, col_size[1]) +
                this.printCol("text", "text-start", element.path, col_size[2]) +
                this.printCol("text", "text-center", element.size, col_size[3]) +
                this.printCol("text", "text-center", element.hash, col_size[4]) +
                this.printCol("text", "text-center", element.user_name, col_size[5]) +
                this.printCol("text", "text-center", element.group_name, col_size[6]) +
                this.printCol("text", "text-center", element.filemode, col_size[7]) +
                this.printCol("date", "text-center", element.created_date, col_size[8]) +
                this.printCol("date", "text-center", element.modified_date, col_size[9])
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
            <div class="row bg-body-secondary" id="${str_headerID}">            
            </div>
        `;
        document.querySelector(str_parentID).insertAdjacentHTML('beforeend', html)
        //tbl_header = document.querySelector("#tbl-header");
    }

    //--------------------------------------------------------------------
    this.printCol = function (type, align, field, size) {
        // Schreibt Daten in eine Zelle der Tabellenstruktur
        // @param:  type - String. darf einen der nachfolgenden Werte enthalten:
        //                      - checkbox, date, text (default)
        //          align - String. Darf einen der nachfolgenden Werte enthalten:
        //                      - text-start, text-center, text-end
        //          field - String. Die Bezeichnung des Datenfeldes aus JSON
        //          size -  String. Zahlenwert zwischen 1 und 12. Definiert im Bootstrap,
        //                      wieviele Spalten optisch zu einer zusammengefasst werden.

        let html;

        switch (type) {

            case "checkbox":
                // Zeichnet eine Checkbox:
                html = `<div class="col-sm-${size}">
                        <div class="input-group mb-3">
                          <div class="input-group-text small">
                            <span class="${align}">
                                <input class="form-check-input mt-0" type="checkbox" id="selectID${field}" name="selectID" ="${field}" value="${field}">
                                <label for="selectID${field}">&nbsp;${field}</label> 
                            </span>
                          </div>
                       </div>
                      </div>`;
                break;

            case "date":
                //schreibt einen Datums-/Zeitwert:
                html = `<div class="col-sm-${size}">
                    <div class="${align} small">
                        ${field.replace("T", " - ")}
                    </div>
                </div>`;
                break;

            default:
                // Schreibt einen Text:
                html = ` <div class="col-sm-${size}">
                    <div class="${align} small">
                         ${field}
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
        for (i = 0 ; i < pathlist.length-1 ; i++) {
            optionlist.push(`<option value="${pathlist[i].id}">${pathlist[i].path}</option>`)
        }

        // Auswahlfeld generieren und im Container einbinden:
        let html= `
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
}

//--------------------------------------------------------------------
function getSelectedJobs() {
    // Liefert eine Liste der ersten zwei ausgewählten Einträge aus der
    // Datenliste zur weiteren Verarbeitung zurück

    let selectedJobs=[];

    let element=  document.querySelectorAll('input[type="checkbox"]:checked');

    // Durchlaufe alle Einträge und merke die ausgewählten IDs:
    element.forEach(function (currentValue){
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

}

//--------------------------------------------------------------------
async function getFileList() {

    let selectedPathID= document.getElementById('path').value;

    let col_size = ["1", "1", "2", "1", "1", "1", "1", "1", "1", "2"];
    let column_names = ["ID", "Job ID", "Pfad", "Größe", "Hash-Wert", "Benutzer", "Gruppe", "Dateirechte", "erstellt am", "letzte Änderung am"];

    let resultlist = await this.callAPI(api_request + '/getfilebypath/' + selectedPathID);

}

function checkboxSelected(source) {
    let selectedBoxes= document.querySelectorAll('input[type="checkbox"]:checked').length;

    if (selectedBoxes == 2) {
        document.querySelector('#btn_selectedJobs').classList.remove('disabled')
    } else if (selectedBoxes >2 ) {
        source.checked=false;
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
