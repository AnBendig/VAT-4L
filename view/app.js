let container = "";
let tbl_header = "";
let api_request = "http://practice.test7.bmsoft.de:8000/vat4l-api";

function vat4lApp() {

    this.init = function () {
        container = document.querySelector("#container")
        this.getJobList();
    }

    this.getJobList = function () {
        fetch(api_request + '/jobs')
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                let job_column_names=["Auswahl","Start","Ende","verarbeite Verzeichnisse","verarbeitete Dateien"];
                this.printJobList(job_column_names, data)
            })
            .catch((error) => {
                console.error(error);
            })
    }

    this.getResultList = function(source,target) {
        fetch(api_request + '/getdelta/' + source + '/' + target)
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                let column_names=["ID","Job ID","Pfad","Größe","Hash-Wert","Benutzer","Gruppe","Dateirechte","erstellt am", "letzte Änderung am"];
                this.printResultList(column_names, data)
            })
            .catch((error) => {
                console.error(error);
            })
    }

    this.printJobList = function (cols, data) {
         this.tableHeader()
               cols.forEach(this.printHeader);
                let html=``;

               for (let i=0;i<data.length;i++){
                   let job= data[i];
                     html =`
                         <div class="row" id="job-element-${job.id_job}">${
                            this.printCol("checkbox", "text-start", job.id_job) +
                            this.printCol("date", "text-end", job.dt_start_job) +
                            this.printCol("date", "text-end", job.dt_end_job) +
                            this.printCol("text", "text-center", job.int_processed_dir) +
                            this.printCol("text", "text-center", job.int_processed_file)}
                         </div>
                        `;
                    container.insertAdjacentHTML('beforeend', html)
                }
    }

     this.printResultList = function (cols, data) {
         this.tableHeader()
               cols.forEach(this.printHeader);
                let html=``;

               for (let i=0;i<data.length;i++){
                   let element= data[i];

                     html =`
                         <div class="row" id="job-element-${element.id_job}">${
                            this.printCol("text", "text-start", element.id) +
                            this.printCol("checkbox", "text-start", element.job_id) +
                            this.printCol("text", "text-start", element.path) +
                            this.printCol("text", "text-end", element.size) +
                            this.printCol("text", "text-end", element.hash) +
                            this.printCol("text", "text-end", element.user_name) + 
                            this.printCol("text", "text-center", element.group_name)+ 
                            this.printCol("text", "text-center", element.filemode)+ 
                            this.printCol("date", "text-end", element.created_date)+ 
                            this.printCol("date", "text-end", element.modified_date)
                   }
                         </div>
                        `;
                    container.insertAdjacentHTML('beforeend', html)
                }
    }

    this.printHeader= function(column_name){
        html= `<div class="col">
                <div class="text-center">
                    ${column_name}
                </div>
            </div>
        `;
        document.querySelector("#tbl-header").insertAdjacentHTML('beforeend', html)
    }

    this.tableHeader= function(){
        html = `
            <div class="row bg-body-secondary" id="tbl-header">            
            </div>
        `;
        container.insertAdjacentHTML('beforeend', html)
        tbl_header=document.querySelector("#tbl-header");
    }

    this.printCol = function(type,align,field) {
       let html=``;

        switch (type) {
            case "checkbox":
               html= `<div class="col">
                        <div class="input-group mb-3">
                          <div class="input-group-text">
                            <input class="form-check-input mt-0" type="checkbox" id="selectID${field}" name="selectID" ="${field}" value="${field}">
                            <label for="selectID${field}">&nbsp;${field}</label> 
                          </div>
                       </div>
                      </div>`
                break;
            case "text":
                html=` <div class="col">
                    <div class="${align}">
                         ${field}
                    </div>
                </div>`
                break;

            case "date":
                html= `<div class="col">
                    <div class="${align}">
                        ${field.replace("T"," - ")}
                    </div>
                </div>`
        }

        return html;
    }



}
function getSelectedJobs(){
    let selectedJobs= [-1,-1];


    let element= document.getElementsByName("selectID");
    for (var i=0; i<= element.length;i++ ){
        if(element[i].checked){
            if (selectedJobs[0] === -1) selectedJobs[0]=element[i].value;
            else {
                selectedJobs[1]=element[i].value;
                return (selectedJobs);
            }
        }
    }
    return null;
}

function showSelectedJobs() {
    selection = getSelectedJobs();
    alert("Die folgenden Jobs wurden ausgewählt: " + getSelectedJobs().join(", "))
    clearContent();
    app.getResultList(selection[0],selection[1])
}

function clearContent() {
        document.querySelector("#container").innerHTML="";
    }

document.addEventListener("DOMContentLoaded", () => {
    app = new vat4lApp();
    app.init();
});