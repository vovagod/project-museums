console.log("NEW RENDER CALL ...")
//$("#actions-dropdown").show();
$(document).ready(function () {
  console.log("WE ARE READY..."); 
  if ($(".dt-checkboxes").not(":disabled") == true) {
    console.log($(this).text()); 
    //if ($(".form-check-input dt-checkboxes")[0].checked = true) {
      //console.log("NOT CHECKED...");
    //}
  };
})
$(document).on("click.dtCheckboxes", "thead th.dt-checkboxes-select-all label, tbody td.dt-checkboxes-cell label", function(e) {
               //e.preventDefault()
               console.log("WE ARE HERE...");
})
//var c = this.s.dt;
if ($("input.dt-checkboxes").prop('checked')) {
  // ($(".dt-checkboxes").is(':checked')) {
  // действия, которые будут выполнены при наступлении события... 
  // k("input.dt-checkboxes", o).not(":disabled").prop("checked", c)
  console.log("IS CHECKED...."); 
} else {
  console.log("NOT CHECKED...");
};
