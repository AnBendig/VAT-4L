let container = "";
let api_request = "http://practice.test7.bmsoft.de:8000/vat4l-api";

function Vat4lApp() {

    this.init = function () {
        container = document.querySelector("#container")
        // this.getJobList();
        this.getByPath();
    }

    this.getJobList = async function () {
        let resultlist1 = await this.callAPI(api_request + '/jobs');

        let col_size = ["2", "3", "3", "2", "2"];
        let job_column_names = ["Auswahl", "Start", "Ende", "verarbeite Verzeichnisse", "verarbeitete Dateien"];

        container.insertAdjacentHTML('beforeend', this.printJobList(job_column_names, col_size, resultlist1));
    }

    this.callAPI = async function (str_api_call) {
        try {
            let res = await fetch(str_api_call);
            return await res.json();
        } catch (err) {
            console.error(err);
        }
    }

    this.getResultList = async function (source, target) {

        let col_size = ["1", "1", "2", "1", "1", "1", "1", "1", "1", "2"];
        let column_names = ["ID", "Job ID", "Pfad", "Größe", "Hash-Wert", "Benutzer", "Gruppe", "Dateirechte", "erstellt am", "letzte Änderung am"];

        let resultlist1 = await this.callAPI(api_request + '/getdelta/' + source + '/' + target);
        let resultlist2 = await this.callAPI(api_request + '/comparejobs/' + source + '/' + target);

        let deleted_data = [];
        let created_data = [];

        for (let i = 0; i <= resultlist1.length - 1; i++) {
            if (resultlist1[i].job_id.toString() === source) {
                deleted_data.push(resultlist1[i])
            } else {
                created_data.push(resultlist1[i])
            }
        }

        if (created_data.length > 0) {
            this.addHeadLine("createdData", "Neue Elemente:", "#container");
            let html1 = this.printResultList(column_names, col_size, "tbl_created", "#createdData", created_data);
            document.querySelector("#createdData").insertAdjacentHTML('beforeend', html1);
        }
        if (deleted_data.length > 0) {
            this.addHeadLine("deletedData", "Gelöschte Elemente:", "#container");
            let html2 = this.printResultList(column_names, col_size, "tbl_deleted", "#deletedData", deleted_data);
            document.querySelector("#deletedData").insertAdjacentHTML('beforeend', html2);
        }

        if (resultlist2.length > 0) {
            this.addHeadLine("changedData", "Geänderte Elemente:", "#container");
            let html = this.printResultList(column_names, col_size, "tbl_changed", "#changedData", resultlist2);
            document.querySelector("#changedData").insertAdjacentHTML('beforeend', html);
        }
    }

    this.printJobList = function (cols, col_size, data) {
        this.tableHeader("job_header", "#container");

        for (let i = 0; i <= cols.length - 1; i++) {
            this.printHeader(cols[i], col_size[i], "#job_header")
        }
        let html = ``;

        for (let i = 0; i < data.length; i++) {
            let job = data[i];
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

    this.addHeadLine = function (id_headline, txt_headline, dom_element) {
        let html = `
            <div class="row"><h2>${txt_headline}</h2></div>
            <div id="${id_headline}"></div> 
        `;
        document.querySelector(dom_element).insertAdjacentHTML('beforeend', html);
    }

    this.printResultList = function (cols, col_size, str_headerID, str_parentID, data) {
        this.tableHeader(str_headerID, str_parentID)

        for (let i = 0; i <= cols.length - 1; i++) {
            this.printHeader(cols[i], col_size[i], "#" + str_headerID)
        }

        let html = ``;

        for (let i = 0; i <= data.length - 1; i++) {
            let element = data[i];

            html += `
                         <div class="row" id="job-element-${element.id_job}">${
                this.printCol("text", "text-center", element.id, col_size[0]) +
                this.printCol("checkbox", "text-center", element.job_id, col_size[1]) +
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

    this.printHeader = function (column_name, column_size, str_parent) {
        let html = `<div class="col-sm-${column_size}">
                <div class="text-center">
                    <strong>${column_name}</strong>
                </div>
            </div>
        `;
        document.querySelector(str_parent).insertAdjacentHTML('beforeend', html)
    }

    this.tableHeader = function (str_headerID, str_parentID) {
        let html = `
            <div class="row bg-body-secondary" id="${str_headerID}">            
            </div>
        `;
        document.querySelector(str_parentID).insertAdjacentHTML('beforeend', html)
        //tbl_header = document.querySelector("#tbl-header");
    }

    this.printCol = function (type, align, field, size) {
        let html = ``;

        switch (type) {
            case "checkbox":
                html = `<div class="col-sm-${size}">
                        <div class="input-group mb-3">
                          <div class="input-group-text small">
                            <span class="${align}">
                                <input class="form-check-input mt-0" type="checkbox" id="selectID${field}" name="selectID" ="${field}" value="${field}">
                                <label for="selectID${field}">&nbsp;${field}</label> 
                            </span>
                          </div>
                       </div>
                      </div>`
                break;
            case "text":
                html = ` <div class="col-sm-${size}">
                    <div class="${align} small">
                         ${field}
                    </div>
                </div>`
                break;

            case "date":
                html = `<div class="col-sm-${size}">
                    <div class="${align} small">
                        ${field.replace("T", " - ")}
                    </div>
                </div>`
        }

        return html;
    }

    this.getByPath = async function () {
        let pathlist =[];
        pathlist = await this.callAPI(api_request + '/getpathlist');

        let optionlist = [];
        for (i = 0 ; i < pathlist.length-1 ; i++) {
            optionlist.push(`<option value="${pathlist[i].id}">${pathlist[i].path}</option>`)
        }

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

function getSelectedJobs() {
    let selectedJobs = [-1, -1];


    let element = document.getElementsByName("selectID");
    for (var i = 0; i <= element.length; i++) {
        if (element[i].checked) {
            if (selectedJobs[0] === -1) selectedJobs[0] = element[i].value;
            else {
                selectedJobs[1] = element[i].value;
                return (selectedJobs);
            }
        }
    }
    return null;
}

function showSelectedJobs() {
    selection = getSelectedJobs();
    clearContent();
    app.getResultList(selection[0], selection[1])
}

function showJobList() {
    clearContent();
    app.getJobList();
}

function clearContent() {
    document.querySelector("#container").innerHTML = "";
}

function showByPath() {
     clearContent();

}

async function getFileList() {

    let selectedPathID= document.getElementById('path').value;
    alert (selectedPathID);
    let col_size = ["1", "1", "2", "1", "1", "1", "1", "1", "1", "2"];
    let column_names = ["ID", "Job ID", "Pfad", "Größe", "Hash-Wert", "Benutzer", "Gruppe", "Dateirechte", "erstellt am", "letzte Änderung am"];

    let resultlist = await this.callAPI(api_request + '/getfilebypath/' + selectedPathID);

}

document.addEventListener("DOMContentLoaded", () => {
    app = new Vat4lApp();
    app.init();
})
