let container = "";
let tbl_header = "";

function vat4lApp() {

    this.init = function () {
        container = document.querySelector("#container")
        this.getJobList();
    }
    this.getJobList = function () {
        fetch('http://practice.test7.bmsoft.de:8000/vat4l-api/jobs')
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                this.tableHeader()
               job_column_names=["Auswahl","ID","Start","Ende","verarbeite Verzeichnisse","verarbeitete Dateien"];
               job_column_names.forEach(this.printHeader);

               for (let i=0;i<data.length;i++){
                    this.printJobs(data[i]);
                }
            })
            .catch((error) => {
                console.error(error);
            })
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

    this.printJobs = function (job) {
        let html = `
            <div class="row" id="job-element-${job.id_job}">
                <div class="col">
                    <div class="input-group mb-3">
                      <div class="input-group-text">
                        <input class="form-check-input mt-0" type="checkbox" value="${job.id_job}">
                      </div>
                    </div>
                </div>
                <div class="col">
                    <div class="text-center">
                        ${job.id_job}
                    </div>
                </div>
                <div class="col">
                    <div class="text-end">
                        ${job.dt_start_job.replace("T"," - ")}
                    </div>
                </div>
                <div class="col">
                    <div class="text-end">
                        ${job.dt_end_job.replace("T"," - ")}
                    </div>
                </div>
                <div class="col">
                    <div class="text-center">
                        ${job.int_processed_dir}
                    </div>
                </div>
                <div class="col">
                    <div class="text-center">
                        ${job.int_processed_file}
                    </div>
                </div>
            </div>
            
        `;

        container.insertAdjacentHTML('beforeend', html)
    }
}

document.addEventListener("DOMContentLoaded", () => {
    let app = new vat4lApp();
    app.init();
});