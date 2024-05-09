var scrollX = true;
buttons=true;
targets=false;
function initailize_datatables() {
    $(table_id).DataTable({

        scrollX: scrollX, 

        dom:'Bfrtip',
        buttons:['pageLength','csv', 'excel', 'pdf', 'print'],

        columnDefs: [
            { 
                orderable: false,
                targets:targets
            },
            {
                targets: to_center,
                className: "text-center",
            },

        ],
        language: {
            processing: '<i class="fa fa-spinner fa-spin fa-3x fa-fw"></i><span class="sr-only">Loading...</span>',
            "emptyTable": "No matching records found",
        },

        // Ajax for pagination
        processing: true,
        serverSide: true,
        ajax: {
            url: url,
            type: 'get',
            data: set_filters(),
        },
        columns: columns,
        // rowCallback: function(nRow, aData, iDisplayIndex) {
        //     var oSettings = this.fnSettings();
        //     $("td:first", nRow).html(oSettings._iDisplayStart + iDisplayIndex + 1);
        //     return nRow;
        // },
    });
};

$(document).ready(function(){
    filter_id.on("change", function() {
        $(table_id).DataTable().destroy();
        initailize_datatables()
    });
})