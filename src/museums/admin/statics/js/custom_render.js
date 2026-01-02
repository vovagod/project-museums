Object.assign(render, {
  mycustomkey: function render(data, type, full, meta) {
    console.log("We are in mycustomkey...")
    $("#actions-dropdown").show();
  },
  col_0: function (data, type, full, meta) {
    console.log("We are in col_0...")
    $("#actions-dropdown").show();
    return '<input class="form-check-input dt-checkboxes" type="checkbox" checked>';
  },
});
$("#actions-dropdown").show();