(function($, templateData, pad) {
  // Export invoicePO function
  window.invoicePO = function(element) {
    var poId = element.value;
    $.ajax({
      type: "GET",
      url: "/api/v1/purchase/invoice/" + poId + "/"
    })
      .done(function() {
        // pass
      })
      .fail(function() {
        alert("There was a problem, try again in a few minutes");
        $("#invoice-done").prop("checked", false);
      });
  };

  $(function() {
    $("#poTable").DataTable({
      ajax: "/goapi/v1/po/list/?length=500&email=" + templateData.userEmail,
      columns: [
        {
          data: "pretty_po_id",
          render: function(data, type) {
            return type === "display" ? pad(data, 4) : data;
          }
        },
        { data: "purchaser" },
        { data: "supplier" },
        { data: "product" },
        {
          data: "price",
          render: function(data, type) {
            if (data == null) return "";
            return type === "display"
              ? "$" + data.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, "$&,")
              : data;
          }
        },
        {
          data: "account_code",
          defaultContent: "None"
        },
        {
          data: "is_invoiced",
          defaultContent: false,
          render: function(data, type, full) {
            if (type === "display") {
              var checkbox = '<input type="checkbox"';
              checkbox +=
                templateData.userIsFinanceAdmin !== true ? ' disabled=""' : "";
              checkbox += full.is_invoiced === true ? "checked" : "";
              checkbox +=
                ' value="' + full.po_id + '" onclick="invoicePO(this)">';
              return checkbox;
            }
            return data;
          }
        },
        { data: "created_date" },
        {
          data: "is_addressed",
          defaultContent: false,
          render: function(data, type, full) {
            if (type === "display") {
              var display =
                "<a href='/purchase/" +
                full.po_id +
                "/'><button type='button' class='btn btn-default'><span class='glyphicon glyphicon-";
              if (full.is_approved === true) {
                display += "ok text-success";
              } else if (full.is_denied === true) {
                display += "remove text-danger";
              } else if (full.is_addressed !== true) {
                display += "bullhorn";
              } else if (full.is_cancelled === true) {
                display += "ban-circle";
              }
              display += "'></span></button></a>";
              return display;
            }
            return data;
          }
        }
      ],
      createdRow: function(row, data) {
        if (data["is_cancelled"] === true) {
          $(row).addClass("bg-cancelled");
        }
      },
      sorting: [[0, "desc"]]
    });
  });
})(window.jQuery, window.templateData, window.pad);
